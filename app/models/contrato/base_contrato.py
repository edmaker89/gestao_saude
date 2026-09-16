from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import declared_attr

from app.ext.database import db


class BaseContrato:
    id = db.Column(db.String(255), primary_key=True, default=lambda: str(uuid4()))
    tipo_contrato_id = db.Column(db.Integer, db.ForeignKey('tipo_contrato.id'), nullable=False)
    numero = db.Column(db.Integer)
    ano = db.Column(db.String(100))
    numero_ano = db.Column(db.String(100))
    edital_credenciamento = db.Column(db.String(255))
    tipo_documento = db.Column(db.String(255))
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=True)
    lotacao_id = db.Column(db.Integer, db.ForeignKey('lotacao_contrato.id'), nullable=True)
    rubrica_orcamentaria_id = db.Column(db.Integer, db.ForeignKey('rubrica_orcamentaria.id'), nullable=True)
    status_contrato = db.Column(db.String(255))  # Status do contrato: Ativo, Inativo, Cancelado, Autorizado, Solicitado
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.now)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    @declared_attr
    def fornecedor(cls):
        return db.relationship('Fornecedor', foreign_keys=[cls.fornecedor_id])

    @declared_attr
    def lotacao(cls):
        return db.relationship('LotacaoContrato', foreign_keys=[cls.lotacao_id])

    @declared_attr
    def rubrica_orcamentaria(cls):
        return db.relationship('RubricaOrcamentaria', foreign_keys=[cls.rubrica_orcamentaria_id])

    @declared_attr
    def tipo_contrato(cls):
        return db.relationship('TipoContrato', foreign_keys=[cls.tipo_contrato_id])
