'''Пробный файл с кодом для заполнения данных в созданной БД
и вообще для всяких экспериментов с кодом. В проекте не участвует.'''
#import app
from app import app, db, Recipy, Products
'''
from werkzeug.security import generate_password_hash, check_password_hash
a='simanw73'
print(generate_password_hash(a))
'''
'''
with app.app_context():
    try:
        cal=float(Products.query.filter(Products.product == 'Apple').first().calories)
    except TypeError:
        cal=100
    print(cal)
'''
lst=[]
res=sum(lst)
print(res)
'''
    #a.title='Неправильный салат с яйцом'
    #db.session.commit()
    #print(a)
    #for ele in a:
        #print(ele.title)
    #for ele in a:
    #    print(ele.instructions)
    #for ele in Recipy.query.all():
        #lst_names.append(ele.title)
        #print(ele)
'''
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
