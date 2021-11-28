from .. import db

class Pracownik(db.Model):
    __tablename__ = 'pracownicy'
    
    id = db.Column(db.Integer, primary_key=True)
    pesel = db.Column(db.Integer, unique=True, nullable=False)
    imie = db.Column(db.String(128), nullable=False)
    nazwisko = db.Column(db.String(128), nullable=False) 
    numer_telefonu = db.Column(db.Integer,  nullable=False)
    stanowisko = db.Column(db.String(128),  nullable=False)
    data_zatrudnienia = db.Column(db.Date, nullable=False)
    data_zwolnienia = db.Column(db.Date,  nullable=True)
    login = db.Column(db.String(128), unique=True, nullable=False)
    haslo = db.Column(db.String(128),  nullable=False)
    
    wizyty = db.relationship("Wizyta")
    
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