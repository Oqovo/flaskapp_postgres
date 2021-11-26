from .. import db

class Pacjent(db.Model):
    __tablename__ = 'pacjenci'
    
    id = db.Column(db.Integer, primary_key=True)
    pesel = db.Column(db.Integer, unique=True, nullable=False)
    imie = db.Column(db.String(128), nullable=False)
    login = db.Column(db.String(128), unique=True, nullable=False)
    haslo = db.Column(db.String(128),  nullable=False)
    data_rejestracji = db.Column(db.Date, nullable=False)
    
    wizyty = db.relationship("Wizyta")
    
    def __init__(self, pesel, imie, data_rejestracji, login, haslo):
        self.pesel = pesel
        self.imie = imie
        self.data_rejestracji = data_rejestracji
        self.login = login
        self.haslo = haslo
    
    def serialize(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}