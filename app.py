'''Код приложения для записи и хранения кулинарных рецептов - версия 2
Будет добавлена возможность формировать рецепт из списка базовых продуктов, 
возможность составлять такой список продуктов,
и указывать калорийность продуктов'''

import datetime
import requests
import json
#import sqlalchemy
from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import AddRecipe, Search, RegistrationForm, LoginForm, AddProduct, AddToRecipe, AddMeal
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "green"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
#app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(os.getcwd(), 'myDB.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)

lst_ing=[]
tot_cal=[]
tot_prot=[]
lst_rec=[]
tot_cal_menu=[]
tot_prot_menu=[]
lst_meals=[]

with app.app_context():
    # Создаем таблицы для рецептов и для пользователей в базе данных
    db = SQLAlchemy(app)

    class Recipy(db.Model):
        id = db.Column(db.Integer, primary_key = True) #primary key column, automatically generated IDs
        title = db.Column(db.String(100), index = True, unique = False) 
        author = db.Column(db.String(40), index = True, unique = False) 
        ingredients = db.Column(db.String(500), index = True, unique = False) 
        instructions = db.Column(db.String(4000), index = True, unique = False) 
        calories = db.Column(db.Float(), index = True, unique = False)
        proteins = db.Column(db.Float(), index = True, unique = False)

    class Products(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        product=db.Column(db.String(100), index = True, unique = False)
        calories=db.Column(db.Integer(), index = True, unique = False)
        proteins=db.Column(db.Float(), index = True, unique = False)
        author = db.Column(db.String(), index = True, unique = False)

    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), index=True, unique=True)
        email = db.Column(db.String(120), index=True, unique=True)
        password_hash = db.Column(db.String(128))
        joined_at_date = db.Column(db.DateTime(), index=True, default=datetime.datetime.utcnow())

        def __repr__(self):
            return '<User {}>'.format(self.username)

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password_hash, password)

    db.create_all()

@app.route('/')
def index():
    return redirect (url_for('login'))#, form=LoginForm)

@app.route("/add_products", methods=["GET", "POST"])
def add_products():
    rows_pr=Products.query.order_by(Products.product) # Filter by Alephbeth
    recipe_form = AddProduct(csrf_enabled=False)
    if request.method == "POST":
        # Block for API request:
        if recipe_form.check():
            query = recipe_form.title.data
            api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)

            response = requests.get(api_url, headers={'X-Api-Key': '6tG3kaTKqFRQVmZQPWvQ0A==HIukQbANUV7z8dmr'})
            if response.status_code == requests.codes.ok:
                json = response.json()
                clr = json[0]['calories']
                prt = json[0]['protein_g']
                txt = "Calories: {} Kcal, proteins: {} g ".format(clr, prt)
                return render_template("add_product.html", form=recipe_form, rows = rows_pr, txt=txt)
            else:
                txt = 'Cannot give you recommended value, sorry'
                return redirect(url_for("add_products", form=recipe_form, rows = rows_pr, txt=txt))
            # End of block
        elif recipe_form.submit() and recipe_form.validate_on_submit():
            try:
                title = recipe_form.title.data.capitalize()
                calories = recipe_form.calories.data
                proteins = recipe_form.proteins.data
                author = current_user.username
                new_product=Products(product=title, calories=calories, proteins=proteins, author= author)
        
                db.session.add(new_product)
                db.session.commit()
                rows_pr=Products.query.all() # update the list of existing ingredients
                txt=''
            except IntegrityError: 
                pass
            return redirect(url_for("add_products", form=recipe_form, rows = rows_pr, txt='')) # redirect to clear the form
    else: 
        return render_template("add_product.html", form=recipe_form, rows = rows_pr, txt='')

@app.route("/recipe/<int:id>")
def recipe(id):
  return render_template("recipe.html", recipe_name=Recipy.query.get(id).title,
   ingredients = Recipy.query.get(id).ingredients.split('\n'),
   instructions = Recipy.query.get(id).instructions.split('\n'),
   calories = Recipy.query.get(id).calories,
   proteins = Recipy.query.get(id).proteins,
   id=Recipy.query.get(id).id)

# Adds a new recipe
@app.route("/add", methods=["GET", "POST"])
def add():
    rows_pr=Products.query.all()
    lst_unsorted=[ele.product for ele in rows_pr]
    lst=sorted(lst_unsorted)
    form1=AddToRecipe()
    form1.ingredient.choices=lst
    form2=AddRecipe()
    
    if request.method == "POST" and form1.add.data:# and form1.validate():
        ing=form1.ingredient.data
        wei=form1.weight.data
        ful= ing + '   ' + str(wei) + ' gr.'
        cal=Products.query.filter(Products.product == ing).first().calories / 100 * wei
        tot_cal.append(cal) # total calories in the recipe
        prot = Products.query.filter(Products.product == ing).first().proteins / 100 * wei
        tot_prot.append(prot)
        lst_ing.append(ful) # Список потом выдается на страницу рецепта построчно
        return render_template("form_add.html", template_form=form1, template_form2=form2, lst_ing=lst_ing)
    
    elif request.method == "POST" and form2.submit.data and form2.validate_on_submit():
        title = form2.title.data
        ingredients = '\n'.join(lst_ing) # Перечень ингредиентов одним элементом добавится в базу
        instructions = form2.instructions.data
        calories = round(sum(tot_cal) ,1) # округляем результат до 1 знака после запятой
        proteins = round(sum(tot_prot), 1)
        author = current_user.username
        new_recipe=Recipy(title=title, ingredients=ingredients, instructions=instructions, author= author, calories =calories, proteins =proteins)
        
        db.session.add(new_recipe)
        db.session.commit()
        lst_ing.clear()
        tot_cal.clear()
        tot_prot.clear()

        return redirect(url_for("index"))
    else: 
        return render_template("form_add.html", template_form=form1, template_form2=form2, lst_ing=lst_ing)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        recipe_form = AddRecipe(csrf_enabled=False)
        
        if recipe_form.validate_on_submit():
            edited = Recipy.query.get(id)
            edited.title = recipe_form.title.data
            #edited.ingredients = recipe_form.ingredients.data
            edited.instructions = recipe_form.instructions.data
            db.session.commit() 
        #return redirect("/recipe/<id>") # Это почему-то не работает - не находит страницу
        return redirect(url_for("index"))

    else:
        recipe_form = AddRecipe(csrf_enabled=False)
        recipe_form.title.data=Recipy.query.get(id).title
        ingredients =Recipy.query.get(id).ingredients
        ingredients_list= ingredients.split('\n')
        #recipe_form.ingredients.data=Recipy.query.get(id).ingredients
        recipe_form.instructions.data=Recipy.query.get(id).instructions
        
        return render_template("edit.html", id=id, template_form=recipe_form,
        title = recipe_form.title.data, 
        ingredients = ingredients_list, 
        instructions = recipe_form.instructions.data)

@app.route("/delete/<id>")
def delete(id):
    deleted = Recipy.query.get(id)
    db.session.delete(deleted)
    db.session.commit() 
    return redirect(url_for("index"))

@app.route("/daily_menu", methods=['GET', 'POST'])
def daily_menu():
    form = AddMeal()

    rows_prod=Products.query.all()
    lst_prod=[ele.product for ele in rows_prod]
    lst_prod1=sorted(lst_prod)
    form.ingredient.choices=lst_prod1

    rows_rec = Recipy.query.all()

    lst_rec=[ele.title for ele in rows_rec if ele.author == current_user.username] # Для выпадающего меню рецептов
    lst_rec1=sorted(lst_rec)
    form.recipe.choices=lst_rec1

    if request.method == "POST":
        if form.add_rec.data: # a meal from the list of recipes is added
            rec=form.recipe.data
            cal= Recipy.query.filter(Recipy.title == rec).first().calories
            prot=Recipy.query.filter(Recipy.title == rec).first().proteins
            ful1= rec + '   ' + str(cal) + ' Kcal.'
            lst_meals.append(ful1)
            tot_cal_menu.append(cal)
            tot_prot_menu.append(prot)
            return render_template("add_menu.html", meal=form, menu=lst_meals, calories=sum(tot_cal_menu), proteins=sum(tot_prot_menu))
        
        elif form.add_prod.data: # a snack from the list of ingredients is added
            prod=form.ingredient.data # I can add here Kcal or gr like in the previous block
            wei=form.weight.data
            cal=Products.query.filter(Products.product == prod).first().calories / 100 * wei
            prot = Products.query.filter(Products.product == prod).first().proteins / 100 * wei
            lst_meals.append(prod)
            tot_cal_menu.append(cal)
            tot_prot_menu.append(prot)
            return render_template("add_menu.html", meal=form, menu=lst_meals, calories=sum(tot_cal_menu), proteins=sum(tot_prot_menu))

        elif form.clean.data:
            lst_meals.clear()
            tot_cal_menu.clear()
            tot_prot_menu.clear()
            return render_template("add_menu.html", meal=form, menu=lst_meals, calories=tot_cal_menu, proteins=tot_prot_menu)
    
    elif request.method == "GET": # Изменить, чтобы не отображал пустой список!! []

        return render_template("add_menu.html", meal=form, menu=lst_meals, calories=sum(tot_cal_menu), proteins=sum(tot_prot_menu))

@app.route("/search", methods=['GET', 'POST'])
def search():
    search_form = Search(csrf_enabled=False)
    word = request.form['word']
    rows=Recipy.query.filter(Recipy.title.like('%'+word+'%')).all()
    user= current_user.username
    return render_template("search.html", rows=rows, search_form=search_form, username = user)

# Зарегистрировать нового пользователя и добавить в БД
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data, 
            password_hash = generate_password_hash(form.password.data))

            db.session.add(user)
            db.session.commit()
            return redirect (url_for('login'))
        except IntegrityError:
            text = 'Sorry, this name or email are already registered in the database. Please choose another username'
            return render_template('register.html', template_form =form, txt=text)
    return render_template('register.html', template_form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 

# Залогинить и перенаправлять на следующие страницы
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for('user', username = current_user.username))
        else:
            form = LoginForm(csrf_enabled=False)	
            return render_template('login.html', form=form, txt="")
    elif request.method == "POST":
        form = LoginForm(csrf_enabled=False)	# Заявляем форму
        if form.validate_on_submit():			# При нажатии на Сабмит
            user = User.query.filter_by(email=form.email.data).first()	# Создается юзер
            if user and user.check_password(form.password.data):		# Проверяется пароль
                login_user(user, remember=form.remember.data)		
                #next_page = request.args.get('next')
                username=user.username
                return redirect(url_for('user', username=username))	# то ему рендерится следующая страница по его запросу или домашняя
            else:			# если же email не находится или пароль неправильный
                text = 'Sorry, this email is not in the database or the password does not match'
                return render_template('login.html', form=form, txt=text)
    return render_template('login.html', form=form, txt="") # а до нажатия Сабмит - рендерить форму логина
# но эта строка дублирует строку в разделе "GET", так что ее нужно убрать после всех проверок

@app.route('/user/<username>')
@login_required
def user(username):
    rows=Recipy.query.order_by(Recipy.title)
    search_form = Search(csrf_enabled=False)
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user, username=username, rows=rows, search_form=search_form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='favicon.ico')

if __name__ == '__main__':
    app.run()
