from datetime import datetime
from app.ext.database import db

class Estabelecimento(db.Model):
    __tablename__ = 'estabelecimento'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    orgao_id = db.Column(db.Integer, db.ForeignKey('organizacao.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_atualizacao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    id_responsavel = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    ativo = db.Column(db.Boolean, default=True)

    responsavel = db.relationship('Usuario', backref='estabelecimentos_responsaveis', foreign_keys=[id_responsavel])
    departamentos = db.relationship('Departamento', backref='estabelecimento', cascade="all, delete-orphan")
