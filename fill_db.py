'''Пробный файл с кодом для заполнения данных в созданной БД
и вообще для всяких экспериментов с кодом. В проекте не участвует.'''
#import app
from app import app, db, Ingredients, Recipe
'''Предположим, есть несколько строчек из БД. Превратим их в список со списками,
чтобы затем передать в javascript на html странице'''
with app.app_context():
    id=1
    ingredients = Recipe.query.get(id).ingredients.all()
    print(len(ingredients))

    a=[[ingredients[i].ingredient, ingredients[i].weight, ingredients[i].calories, ingredients[i].proteins] for i in range(len(ingredients))]
    #print(a)
    sum=0
    for j in range(len(a)):
        sum += a[j][2]
    print(sum)
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
