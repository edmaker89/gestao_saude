from app.ext.database import db

class RubricaOrcamentaria(db.Model):
    __tablename__ = 'rubrica_orcamentaria'
    id = db.Column(db.Integer, primary_key=True)
    ficha_fonte_id = db.Column(db.Integer, db.ForeignKey('ficha_fonte.id'))
    conta_id = db.Column(db.Integer, db.ForeignKey('conta.id'))
    
    ficha_fonte = db.relationship('FichaFonte', foreign_keys=[ficha_fonte_id])
    conta = db.relationship('Conta', foreign_keys=[conta_id])
    
    def __repr__(self):
        return '<RubricaOrcamentaria %r>' % self.id