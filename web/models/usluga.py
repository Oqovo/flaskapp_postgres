from .. import db

class Usluga(db.Model):
    __tablename__ = 'uslugi'
    
    id = db.Column(db.Integer, primary_key=True)
    nazwa= db.Column(db.String(128), unique=True, nullable=False)
    opis = db.Column(db.String(128), nullable=False)
    cena = db.Column(db.Integer, nullable=False)
    
    uslugi_wizyty = db.relationship("Usluga_Wizyta")
    
    def __init__(self, nazwa, opis, cena):
        self.nazwa = nazwa
        self.opis = opis
        self.cena = cena 
	
    
    def serialize(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}