from datetime import datetime
from app.ext.database import db

class Organizacao(db.Model):
    __tablename__ = 'organizacao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    sigla = db.Column(db.String(50))
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    id_responsavel = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    ativo = db.Column(db.Boolean, default=True)

    responsavel = db.relationship('Usuario', backref='organizacoes_responsaveis', foreign_keys=[id_responsavel])
    # estabelecimentos = db.relationship('Estabelecimento', backref='organizacao', cascade="all, delete-orphan")