from .. import db

class Wizyta(db.Model):
    __tablename__ = 'wizyty'
    
    id = db.Column(db.Integer, primary_key=True)
    ####
    data = db.Column(db.Date, nullable=False)
    #UWAGA daty chyba nie będzie, zostawimy tylko godzina_rozp i godzina_zakonczenia
    godzina_rozpoczecia = db.Column(db.DateTime, nullable=False)
    godzina_zakonczenia = db.Column(db.DateTime, nullable=False)
    czy_sie_odbyla = db.Column(db.Boolean, nullable=False)
    
    dentysta = db.Column(db.ForeignKey('pracownicy.id'), nullable=False)
    pacjent = db.Column(db.ForeignKey('pacjenci.id'), nullable=False)

    uslugi_wizyty = db.relationship("Usluga_Wizyta")
    
    def __init__(self, data, godzina_rozpoczecia, godzina_zakonczenia, czy_sie_odbyla, dentysta, pacjent):
        self.data = data
        self.godzina_rozpoczecia = godzina_rozpoczecia
        self.godzina_zakonczenia = godzina_zakonczenia
        self.czy_sie_odbyla = czy_sie_odbyla
        self.dentysta = dentysta
        self.pacjent = pacjent
    
    def serialize(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}