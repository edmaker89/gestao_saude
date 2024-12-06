from datetime import datetime
from app.ext.database import db
from app.models.contrato.base_contrato import BaseContrato

class SolicitacaoContrato(BaseContrato):
    __tablename__ = 'contrato'
    id = db.Column(db.String(255), primary_key=True, ForeignKey='base_contrato.id')
    solicitante_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data_solicitacao = db.Column(db.DateTime, nullable=False, default=datetime.now)
    autorizado_por_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    autorizado_em = db.Column(db.DateTime, nullable=True)
    
    solicitante = db.relationship('Usuario', foreign_keys=[solicitante_id])
    autorizado_por = db.relationship('Usuario', foreign_keys=[autorizado_por_id])
    
    def __repr__(self):
        return f"Base Contrato (id={self.id}, tipo={self.tipo_contrato_id}"