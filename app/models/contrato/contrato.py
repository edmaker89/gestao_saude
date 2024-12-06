from datetime import datetime
from app.ext.database import db
from app.models.contrato.base_contrato import BaseContrato

class Contrato(BaseContrato):
    __tablename__ = 'contrato'
    id = db.Column(db.String(255), primary_key=True, ForeignKey='base_contrato.id')
    solicitacao_contrato_id = db.Column(db.String(255), db.ForeignKey('solicitacao_contrato.id'), nullable=False)
    data_inicio_contrato = db.Column(db.DateTime, nullable=False)
    data_fim_contrato = db.Column(db.DateTime, nullable=False)
    valor_global = db.Column(db.Float, nullable=False)
    responsavel_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    solicitacao = db.relationship('SolicitacaoContrato', foreign_keys=[solicitacao_contrato_id])
    responsavel = db.relationship('Usuario', foreign_keys=[responsavel_id])
    
    def __repr__(self):
        return f"Base Contrato (id={self.id}, tipo={self.tipo_contrato_id}"