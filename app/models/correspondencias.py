from sqlalchemy import Enum
from app.ext.database import db

class Correspondencias(db.Model):
    __tablename__ = 'correspondencias'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Integer, db.ForeignKey('tipo_correspondencias.id'))
    numero = db.Column(db.Integer)
    ano = db.Column(db.String(100))
    numero_ano = db.Column(db.String(100))
    assunto = db.Column(db.String(255))
    usuario = db.Column(db.Integer, db.ForeignKey('users.id'))
    data = db.Column(db.Date)
    visibilidade = db.Column(Enum('publica', 'privada', 'sigilosa'), default='publica', nullable=False)  
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=True)

    # Relacionamentos  
    tipo_correspondencia = db.relationship('TipoCorrespondencias', backref='correspondencias') 
    usuario_relacionado = db.relationship('Usuario', backref='correspondencias')   
    departamento = db.relationship('Departamento', backref='correspondencias')

    def __repr__(self):
        return f"<Correspondencia {self.assunto}>"