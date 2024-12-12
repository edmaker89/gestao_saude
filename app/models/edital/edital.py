from app.ext.database import db

class Edital(db.Model):
    __tablename__ = 'edital'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo_id = db.Column(db.Integer, foreignKey='tipo_contrato.id', nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    data_abertura = db.Column(db.DateTime, nullable=False)
    data_encerramento = db.Column(db.DateTime, nullable=False)
    
    tipo_edital = db.relationship('TipoContrato', foreign_keys=[tipo_id])
    
    def __repr__(self):
        return '<Edital %r>' % self.id