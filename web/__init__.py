#!/usr/bin/env python
# encoding: utf-8

# DO WPROWADZANIA ZMIAN W KONTENERZE:
# docker-compose -d --build
# docker-compose up

from flask import Flask, jsonify, render_template, json, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import lazyload, joinedload, subqueryload, selectinload, raiseload
import random
from flask_modus import Modus
from datetime import datetime


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

#-----------USŁUGI-------------------
db.session.add(Usluga(nazwa='Wyrywanie zęba', opis='Standardowe wyrywanie zęba - 1 szt.; bez znieczulenia', cena=100))
db.session.add(Usluga(nazwa='Znieczulenie', opis='Znieczulenie miejscowe', cena=50))
db.session.add(Usluga(nazwa='Usuwanie kamienia nazębnego', opis='Usuwanie kamienia nazębnego - całe', cena=120))
db.session.add(Usluga(nazwa='Przegląd', opis='Standardowa wizyta kontrolna - analiza jamy ustnej; Refundacja NFZ', cena=0))
db.session.add(Usluga(nazwa='Wybielanie', opis='Wybielanie zębów', cena=1000))
db.session.add(Usluga(nazwa='Leczenie kanałowe', opis='Leczenie kanałowe - 1 kanał', cena=150))
db.session.add(Usluga(nazwa='Plombowanie', opis='Plombowanie zęba - 1 szt.', cena=150))
db.session.add(Usluga(nazwa='Implant', opis='Implant - szt.', cena=1900))
db.session.add(Usluga(nazwa='RTG', opis='RTG jamy ustnej', cena=10))

#-------------PRACOWNICY-------------
db.session.add(Pracownik(imie='Anna', pesel=98, stanowisko='dentysta', data_zatrudnienia='10/10/2014', data_zwolnienia= None , login='ad@example.com', haslo=generate_password_hash( 'xxx')))
db.session.add(Pracownik(imie='Hanna', pesel=80, stanowisko='chirurg', data_zatrudnienia='06/17/2014', data_zwolnienia= None , login='hd@example.com', haslo=generate_password_hash( 'xxx')))
db.session.add(Pracownik(imie='Paweł', pesel=38, stanowisko='dentysta', data_zatrudnienia='10/10/2017', data_zwolnienia= None , login='pc@example.com', haslo=generate_password_hash( 'xxx')))
db.session.add(Pracownik(imie='Robert', pesel=48, stanowisko='chirurg', data_zatrudnienia='03/12/2018', data_zwolnienia= None , login='rg@example.com', haslo=generate_password_hash( 'xxx')))

#------------Próby-----TMP--------------

db.session.add(Pacjent(imie='Anna', pesel=78, data_rejestracji='10/10/2014', login='anna@example.com', haslo=generate_password_hash('xxx')))
db.session.add(Pacjent(imie='Pawel', pesel=89, data_rejestracji='05/02/2019', login='pawel@example.com', haslo=generate_password_hash('xxx')))
db.session.add(Pacjent(imie='Karolina', pesel=97, data_rejestracji='10/11/2017', login='karolina@example.com', haslo=generate_password_hash('xxx')))
db.session.commit()

#db.session.add(Pracownik(imie='Anna', pesel=98, stanowisko='dentysta', data_zatrudnienia='10/10/2014', data_zwolnienia= None , login='bd@example.com', haslo=generate_password_hash( 'xxx')))
db.session.add(Wizyta(data='1988-01-17', godzina_rozpoczecia=datetime(2015, 6, 5, 8, 10, 10, 10),godzina_zakonczenia=datetime(2015, 6, 5, 8, 10, 10, 10), czy_sie_odbyla=0, dentysta=1, pacjent=1))
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