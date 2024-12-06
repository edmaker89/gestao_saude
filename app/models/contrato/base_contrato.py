from datetime import datetime
from app.ext.database import db
from uuid import uuid4

class BaseContrato(db.Model):
    __tablename__ = 'base_contrato'
    id = db.Column(db.String(255), primary_key=True, default=uuid4)
    tipo_contrato_id = db.Column(db.Integer, db.ForeignKey('tipo_contrato.id'), nullable=False)
    numero = db.Column(db.Integer)
    ano = db.Column(db.String(100))
    numero_ano = db.Column(db.String(100))
    edital_credenciamento = db.Column(db.String(255))
    tipo_documento = db.Column(db.String(255))
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=True)
    lotacao_id = db.Column(db.Integer, db.ForeignKey('lotacao.id'), nullable=True)
    rubrica_orcamentaria_id = db.Column(db.Integer, db.ForeignKey('rubrica_orcamentaria.id'), nullable=True)
    status_contrato = db.Column(db.String(255)) # Status do contrato: Ativo, Inativo, Cancelado, Autorizado, Solicitado
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.now)
    atualizado_em = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    fornecedor = db.relationship('Fornecedor', foreign_keys=[fornecedor_id])
    lotacao = db.relationship('Lotacao', foreign_keys=[lotacao_id])
    rubrica_orcamentaria = db.relationship('RubricaOrcamentaria', foreign_keys=[rubrica_orcamentaria_id])
    tipo_contrato = db.relationship('TipoContrato', foreign_keys=[tipo_contrato_id])
    
    def __repr__(self):
        return f"Base Contrato (id={self.id}, tipo={self.tipo_contrato_id}"