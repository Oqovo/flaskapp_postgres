#!/usr/bin/env python
# encoding: utf-8

# DO WPROWADZANIA ZMIAN W KONTENERZE:
# docker-compose -d --build
# docker-compose up

from flask import Flask, jsonify, render_template, json, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import lazyload, joinedload, subqueryload, selectinload, raiseload
import random
from flask_modus import Modus


app = Flask(__name__, template_folder='templates')
app.config.from_object("app.config.Config")    # 'app', a nie 'web' (jak folder) ponieważ w dockerze umieściliśmy projekt pod folderem 'app'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

modus = Modus(app)


### MODELS

'''
Aby stworzyć bazę danych:
   / docker-compose exec web flask shell

A w konsoli:

    from app import db

    db.drop_all()
    db.create_all()
    db.session.commit()
'''

from .models.pacjent import Pacjent
from .models.pracownik import Pracownik
from .models.usluga_wizyta import Usluga_Wizyta
from .models.usluga import Usluga
from .models.wizyta import Wizyta


'''
Aby stworzyć swojego użytkownika:
    db.session.add(User(email='abc@example.com'))
    db.session.commit()
'''
    

db.drop_all()
db.create_all()
db.session.commit()
db.session.commit()


db.session.add(Pacjent(imie='Anna', pesel=98, data_rejestracji='10/10/2014', login='anna@example.com', haslo='xxx'))
db.session.add(Pacjent(imie='Pawel', pesel=89, data_rejestracji='05/02/2019', login='pawel@example.com', haslo='xxx'))
db.session.add(Pacjent(imie='Karolina', pesel=97, data_rejestracji='10/11/2017', login='karolina@example.com', haslo='xxx'))
db.session.commit()





### CONTROLLERS
from .views import views
from .auth import auth
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/auth')

  
    
if __name__ == "__main__":
   import logging
   logging.basicConfig(filename='error.log',level=logging.INFO) 
   app.run(host='0.0.0.0', port=5000, debug=True)
   
   #cars = db.session.query(Owner).options(lazyload(Owner.cars)).all()