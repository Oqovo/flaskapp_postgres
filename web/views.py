from flask import Blueprint, Flask, jsonify, render_template, json, request, url_for, redirect, session
from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import lazyload, joinedload, subqueryload, selectinload, raiseload
import random
from flask_modus import Modus

from .models.pacjent import Pacjent
from .models.pracownik import Pracownik
from .models.usluga_wizyta import Usluga_Wizyta
from .models.usluga import Usluga
from .models.wizyta import Wizyta

from . import db

views = Blueprint('views', __name__)

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
    
@views.route('/', methods=['GET', 'POST'])
def index():
  # for c in Car.query.all():   
   if request.method == "POST":
        pacjent_pesel = random.randint(100,200)
        
        db.session.add(Pacjent(imie=request.form['imie'], pesel = pacjent_pesel, data_rejestracji = '04/06/2028'))
        db.session.commit()
        return redirect(url_for('views.index'))
   return render_template('index.html', pacjenci = db.session.query(Pacjent).all())#json.dumps([c.serialize() for c in db.session.query(Car).all()], indent=2)
#https://pythonbasics.org/flask-rest-api/

@views.route('/wizyty_pacj')
def index_pacjent():
    user = session.get("user_id")

    return render_template('index_pacjent.html', wizyty = db.session.query(Wizyta).filter(Wizyta.pacjent[id] == user ))

@views.route('/wizyty_prac')
def index_pracownik():
    user = session.get("user_id")

    return render_template('index_pracownik.html', wizyty = db.session.query(Wizyta).filter(Wizyta.dentysta[id] == user ))

@views.route('/wizyty_pacj/<int:id>')
def show_pacjent(id):

    return render_template('show_pacjent.html', wizyty = db.session.query(Wizyta).filter(Wizyta.id == id ).first())

@views.route('/wizyty_prac/<int:id>')
def show_pracownik(id):

    return render_template('show_pacjent.html', wizyty = db.session.query(Wizyta).filter(Wizyta.id == id ).first())

@views.route('/wizyty_pacj/new')
def new1():
    user = session.get("user_id")

    return render_template('new.html', p =  db.session.query(Pacjent).filter(Pacjent.id == user).first())   

@views.route('/account')
def account():
    user = session.get("user_id")

    return render_template('account.html')