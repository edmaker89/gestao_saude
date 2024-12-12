from app.ext.database import db

class FichaFonte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ficha_id = db.Column(db.Integer, db.ForeignKey('ficha.id'), nullable=False)
    fonte_id = db.Column(db.Integer, db.ForeignKey('fonte.id'), nullable=False)
    
    ficha = db.relationship('Ficha', foreign_keys=[ficha_id])
    fonte = db.relationship('Fonte', foreign_keys=[fonte_id])
    
    def __repr__(self):
        return f'<FichaFonte(id={self.id}, ficha_id={self.ficha_id}, fonte_id={self.fonte_id})>'