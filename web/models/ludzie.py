from .. import db
from sqlalchemy.ext.declarative import declarative_base, ConcreteBase

Base = declarative_base()

class Konto(ConcreteBase, Base):
    __tablename__ = 'konta'

    id = db.Column(db.Integer, primary_key=True)   
    
    pesel = db.Column(db.Integer, unique=True, nullable=False)
    imie = db.Column(db.String(128), nullable=False)
    nazwisko = db.Column(db.String(128), nullable=False) 
    login = db.Column(db.String(128), unique=True, nullable=False)
    haslo = db.Column(db.String(128),  nullable=False)
    numer_telefonu = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'konta',
        'concrete':True
    }

class Pracownik(db.Model, Konto):
    __tablename__ = 'pracownicy'

    id = db.Column(db.Integer, primary_key=True)   
    
    pesel = db.Column(db.Integer, unique=True, nullable=False)
    imie = db.Column(db.String(128), nullable=False)
    nazwisko = db.Column(db.String(128), nullable=False) 
    login = db.Column(db.String(128), unique=True, nullable=False)
    haslo = db.Column(db.String(128),  nullable=False)
    stanowisko = db.Column(db.String(128),  nullable=False)
    data_zatrudnienia = db.Column(db.Date, nullable=False)
    data_zwolnienia = db.Column(db.Date,  nullable=True)
    numer_telefonu = db.Column(db.Integer, nullable=False)
    wizyty = db.relationship("Wizyta")

    __mapper_args__ = {
        'polymorphic_identity':'pracownicy',
        'concrete':True
    }
    
    def __init__(self, pesel, imie, nazwisko, stanowisko, numer_telefonu, data_zatrudnienia, data_zwolnienia, login, haslo):
        self.pesel = pesel
        self.imie = imie 
        self.nazwisko = nazwisko
        self.stanowisko = stanowisko
        self.numer_telefonu = numer_telefonu
        self.data_zatrudnienia = data_zatrudnienia
        self.data_zwolnienia = data_zwolnienia
        self.login = login
        self.haslo = haslo
    
    def serialize(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Pacjent(db.Model, Konto):
    __tablename__ = 'pacjenci'
    
    id = db.Column(db.Integer, primary_key=True)
    pesel = db.Column(db.Integer, unique=True, nullable=False)
    imie = db.Column(db.String(128), nullable=False)
    nazwisko = db.Column(db.String(128), nullable=False) 
    login = db.Column(db.String(128), unique=True, nullable=False)
    haslo = db.Column(db.String(128),  nullable=False)
    data_rejestracji = db.Column(db.Date, nullable=False)
   
    numer_telefonu = db.Column(db.Integer, nullable=False)
    
    wizyty = db.relationship("Wizyta")

    __mapper_args__ = {
        'polymorphic_identity':'pacjenci',
        'concrete':True
    }
    
    def __init__(self, pesel, imie, nazwisko, numer_telefonu, data_rejestracji, login, haslo):
        
        self.pesel = pesel
        self.imie = imie
        self.nazwisko = nazwisko
        self.numer_telefonu = numer_telefonu
        self.data_rejestracji = data_rejestracji
        self.login = login
        self.haslo = haslo
        
    
    def serialize(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}