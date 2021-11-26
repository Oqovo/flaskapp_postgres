from flask import Blueprint, Flask, jsonify, render_template, json, request, url_for, redirect, session
from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import lazyload, joinedload, subqueryload, selectinload, raiseload
import random
from flask_modus import Modus
from werkzeug.security import generate_password_hash
from datetime import datetime

from .models.pacjent import Pacjent
from .models.pracownik import Pracownik
from .models.usluga_wizyta import Usluga_Wizyta
from .models.usluga import Usluga
from .models.wizyta import Wizyta

from . import db

views = Blueprint('views', __name__)

#-----------------------------------------TUTAJ EXAMPLE
# widoki i html z 1 są nieaktualne

@views.route('/pacjenci/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show1(id):
    # find a toy based on its id
    found_pacjent = db.session.query(Pacjent).filter(Pacjent.id == id).first()
    #https://stackoverflow.com/questions/6750017/how-to-query-database-by-id-using-sqlalchemy

    # Refactor the code above using a list comprehension!
    print(found_pacjent)
    if request.method == b"PATCH":

        db.session.query(Pacjent).filter(Pacjent.id == id).update({'imie' : request.form['imie']})
        db.session.commit()
        return redirect(url_for('views.index'))
        
    if request.method == b"DELETE":
        #found_car.delete(synchronize_session=False)
        db.session.delete(found_pacjent)
        db.session.commit()
        return redirect(url_for('views.index'))
    return render_template('show1.html', c=found_pacjent)
  
@views.route('/pacjenci/<int:id>/edit')
def edit1(id):
    # Refactored using a list comprehension!
    found_pacjent = db.session.query(Pacjent).filter(Pacjent.id == id).first()
    # Refactor the code above to use a generator so that we do not need to do [0]!
    return render_template('edit1.html', c=found_pacjent)
   
@views.route('/pacjenci/new')
def new1():
    return render_template('new1.html')   
    
#---------------------------------------------------------------TUTAJ DOPIERO GIT :
    
@views.route('/', methods=['GET', 'POST'])
def index():
  # for c in Car.query.all():   
  # if request.method == "POST":
   #     pacjent_pesel = random.randint(100,200)
    #    
     #   db.session.add(Pacjent(imie=request.form['imie'], pesel = pacjent_pesel, data_rejestracji = '04/06/2028'))
      #  db.session.commit()
       # return redirect(url_for('views.index'))  

    return render_template('index.html')#json.dumps([c.serialize() for c in db.session.query(Car).all()], indent=2)
#https://pythonbasics.org/flask-rest-api/

@views.route('/wizyty_pacj')
def index_pacjent():
    user = session.get("user_id")
    pacjent = db.session.query(Pacjent).filter(Pacjent.id == user ).first()
    print("****", pacjent)

    if request.method == "POST":       
        #db.session.add(Pacjent(imie=request.form['imie'], pesel = pacjent_pesel, data_rejestracji = '04/06/2028', login='anna@example.com', haslo=generate_password_hash('xxx')))
        db.session.add(Wizyta(data='1988-01-17', godzina_rozpoczecia=datetime(2015, 6, 5, 8, 10, 10, 10),godzina_zakonczenia=datetime(2015, 6, 5, 8, 10, 10, 10), czy_sie_odbyla=0, dentysta=1, pacjent=pacjent.id))

        db.session.commit()
        return redirect(url_for('views.index_pacjent'))


    return render_template('index_pacjent.html', wizyty = db.session.query(Wizyta).filter(Wizyta.pacjent == pacjent.id ).all())

@views.route('/wizyty_prac')
def index_pracownik():
    user = session.get("user_id")
    dentysta = db.session.query(Pracownik).filter(Pracownik.id == user ).first()
    return render_template('index_pracownik.html', wizyty = db.session.query(Wizyta).filter(Wizyta.dentysta == dentysta.id ).all())

@views.route('/wizyty_pacj/<int:id>')
#tak naprawde to widok wizyty przez pacjenta
def show_pacjent(id):

    wizyta = db.session.query(Wizyta).filter(Wizyta.pacjent == id ).first()

    if request.method == b"DELETE":
        #found_car.delete(synchronize_session=False)
        db.session.delete(wizyta)
        db.session.commit()
        return redirect(url_for('views.index_pacjent'))

    return render_template('show_pacjent.html', c = wizyta)

@views.route('/wizyty_prac/<int:id>')
def show_pracownik(id):

    wizyta = db.session.query(Wizyta).filter(Wizyta.pacjent == id ).first()

    if request.method == b"PATCH":
        db.session.query(Wizyta).filter(Wizyta.id == id).update({'data' : request.form['data']})
        db.session.commit()
        return redirect(url_for('views.index_pracownik'))

    return render_template('show_pracownik.html', c = wizyta)

@views.route('/wizyty_pacj/new')
def new():
    user = session.get("user_id")

    return render_template('new.html', p =  db.session.query(Pacjent).filter(Pacjent.id == user).first())   


#TO DO - dodać rozróżnienie pacjenta i pracownika, np. za pomocą zmiennej u
@views.route('/account')
def account(u):
    user = session.get("user_id")


    return render_template('account.html')