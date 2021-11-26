from .. import db

class Usluga_Wizyta(db.Model):
    __tablename__ = 'uslugi_wizyty'
    
    id = db.Column(db.Integer, primary_key=True)
    
    usluga_id = db.Column(db.ForeignKey('uslugi.id'), nullable=False)
    wizyta_id = db.Column(db.ForeignKey('wizyty.id'), nullable=False)
    
    def __init__(self, usluga_id, wizyta_id):
        self.usluga_id = usluga_id
        self.wizyta_id = wizyta_id

    
    def serialize(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}