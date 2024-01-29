from app.ext.database import db
from datetime import datetime

class Avisos(db.Model):
    __tablename__ = 'avisos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    autor = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relacionamento com a tabela Usuario
    autor_relacionamento = db.relationship('Usuario', foreign_keys=[autor])

    def __repr__(self):
        return f"Aviso(id={self.id}, descricao={self.descricao}, autor={self.autor})"