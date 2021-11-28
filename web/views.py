from flask import Blueprint, Flask, jsonify, render_template, json, request, url_for, redirect, session
from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import lazyload, joinedload, subqueryload, selectinload, raiseload
import random
from flask_modus import Modus
from werkzeug.security import generate_password_hash
from datetime import datetime
from datetime import timedelta
# import datetime


from .models.pacjent import Pacjent
from .models.pracownik import Pracownik
from .models.usluga_wizyta import Usluga_Wizyta
from .models.usluga import Usluga
from .models.wizyta import Wizyta

from . import db

views = Blueprint('views', __name__)

#---------------------------------------------------------------TUTAJ GIT :
    
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

@views.route('/wizyty_pacj', methods=['GET', 'POST'])
def index_pacjent():
    user = session.get("user_id")
    pacjent = db.session.query(Pacjent).filter(Pacjent.id == user ).first()
    print("****", pacjent)

    if request.method == "POST":  
        #TO DO     
        godzina_rozpoczecia = datetime.strptime(request.form["datetime"], '%Y-%m-%dT%H:%M')
      #  usluga = request.form["usluga"]
        uslugi = request.form.getlist("check")
        
        print(godzina_rozpoczecia)
        print(uslugi)
        #datetime(2015, 6, 5, 8, 10, 10),
        db.session.add(Wizyta( godzina_rozpoczecia=godzina_rozpoczecia, godzina_zakonczenia=godzina_rozpoczecia + timedelta(minutes=30),  czy_sie_odbyla=0, dentysta=1, pacjent=pacjent.id))


        for u in uslugi:            
            db.session.add(Usluga_Wizyta(usluga_id= u,wizyta_id= db.session.query(Wizyta).order_by(Wizyta.id.desc()).first().id))

        db.session.commit()
        return redirect(url_for('views.index_pacjent'))


    return render_template('index_pacjent.html', wizyty = db.session.query(Wizyta).filter(Wizyta.pacjent == pacjent.id ).all())

@views.route('/wizyty_prac')
def index_pracownik():
    user = session.get("user_id")
    dentysta = db.session.query(Pracownik).filter(Pracownik.id == user ).first()
    return render_template('index_pracownik.html', wizyty = db.session.query(Wizyta).filter(Wizyta.dentysta == dentysta.id ).all())

@views.route('/wizyty_pacj/<int:id>', methods=['GET', 'DELETE'])
#tak naprawde to widok wizyty przez pacjenta
def show_pacjent(id):

    wizyta = db.session.query(Wizyta).filter(Wizyta.id == id).first()

    if request.method == b"DELETE":
        #found_car.delete(synchronize_session=False)
        db.session.delete(wizyta)
        db.session.commit()
        return redirect(url_for('views.index_pacjent'))

    return render_template('show_pacjent.html', c = wizyta)

@views.route('/wizyty_prac/<int:id>', methods=['GET', 'PATCH'])
def show_pracownik(id):

    wizyta = db.session.query(Wizyta).filter(Wizyta.id == id ).first()

    if request.method == b"PATCH":
        #TO DO
       # db.session.query(Wizyta).filter(Wizyta.id == id).update({'data' : request.form['data']})
        db.session.commit()
        return redirect(url_for('views.index_pracownik'))

    return render_template('show_pracownik.html', c = wizyta)

@views.route('/wizyty_pacj/new')
def new():
    user = session.get("user_id")

    return render_template('new.html', p =  db.session.query(Pacjent).filter(Pacjent.id == user).first(), uslugi = db.session.query(Usluga).all())   


@views.route('/account')
def account():
    tablename = session.get("tablename")
    if tablename == 'pacjenci':
        user =  db.session.query(Pacjent).filter(Pacjent.id == session.get("user_id")).first()
    else:
        user =  db.session.query(Pracownik).filter(Pracownik.id == session.get("user_id")).first()

    return render_template('account.html', tablename = tablename, user = user)