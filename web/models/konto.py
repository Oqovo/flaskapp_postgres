from .. import db


class Konto(db.Model):
    __tablename__ = 'konta'
    __abstract__ = True

    #id = db.Column(db.Integer, primary_key=True)
    pesel = db.Column(db.Integer, unique=True, nullable=False)
    imie = db.Column(db.String(128), nullable=False)
    nazwisko = db.Column(db.String(128), nullable=False) 
    login = db.Column(db.String(128), unique=True, nullable=False)
    haslo = db.Column(db.String(128),  nullable=False)
    #data_rejestracji = db.Column(db.Date, nullable=False)
   
    numer_telefonu = db.Column(db.Integer, nullable=False)
    wizyty = db.relationship("Wizyta")

    
    #stanowisko = db.Column(db.String(128),  nullable=False)
    #data_zatrudnienia = db.Column(db.Date, nullable=False)
    #data_zwolnienia = db.Column(db.Date,  nullable=True)
    

    __mapper_args__ = {
        'polymorphic_identity':'konta',
        'polymorphic_on':type
    }