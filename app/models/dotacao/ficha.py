from app.ext.database import db
from app.models.dotacao import elemento_despesa

class Ficha(db.Model):
    __tablename__ = "ficha"

    id = db.Column(db.Integer, primary_key=True)
    numero_ficha = db.Column(db.String(255), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    aplicacao_programada_id = db.Column(db.Integer, db.ForeignKey('aplicacao_programada.id'), nullable=False)
    elemento_despesa_id = db.Column(db.Integer, db.ForeignKey('elemento_despesa.id'), nullable=False)
    
    aplicacao_programada = db.relationship('AplicacaoProgramada', foreign_keys=[aplicacao_programada_id])
    elemento_despesa = db.relationship('ElementoDespesa', foreign_keys=[elemento_despesa_id])
    
    def __repr__(self):
        return f"<Ficha {self.id}>"