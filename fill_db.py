'''Пробный файл с кодом для заполнения данных в созданной БД
и вообще для всяких экспериментов с кодом. В проекте не участвует.'''
#import app
from app import app, db, Recipy, Products

class Recipy(db.Model):
    id = db.Column(db.Integer, primary_key = True) #primary key column, automatically generated IDs
    title = db.Column(db.String(100), index = True, unique = False) 
    author = db.Column(db.String(40), index = True, unique = False) 
    ingredients = db.Column(db.String(500), index = True, unique = False) # this could be removed
    instructions = db.Column(db.String(4000), index = True, unique = False) 
    calories = db.Column(db.Float(), index = True, unique = False)
    proteins = db.Column(db.Float(), index = True, unique = False)
    ingredients_out = db.relationship('Ingreds', backref='recipe', lazy='dynamic')

class Ingreds(db.Model):
    id = db.Column(db.Integer, primary_key = True) #primary key column, automatically generated IDs
    name = db.Column(db.String(100), unique = False)
    weight = db.Column(db.Integer, unique = False) 
    recipy_id = db.Column(db.Integer, db.ForeignKey('recipe.id')) 

# in add function:
dic_ing_name={}
# in if:

dic_ing_name[ing] = wei

# in elif:
for ele in dic_ing_name:
    new_in = Ingreds(name=ing, weight=dic_ing_name[ing], recipy_id= new_recipe.id)
'''
with app.app_context():

    
    # Create  new line in the db
    r3=Recipy(title='Poridge', author='Serge',
    ingredients='rolled oats 100 g, \n cherry juice 20 g,\n raisins 20 g', 
    instructions='Mix it and wait for 2 hours')
    db.session.add(r3)
    db.session.commit()
    
    # change an existed line in the db
    a=Recipy.query.get(4)
    a.instructions='Mix it and wait for 4 hours'
    db.session.commit()
    '''
