from datetime import datetime

from app.ext.database import db
from app.models.contrato.base_contrato import BaseContrato


class SolicitacaoContrato(BaseContrato, db.Model):
    __tablename__ = 'solicitacao_contrato'
    solicitante_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data_solicitacao = db.Column(db.DateTime, nullable=False, default=datetime.now)
    autorizado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    autorizado_em = db.Column(db.DateTime, nullable=True)

    solicitante = db.relationship('Usuario', foreign_keys=[solicitante_id])
    autorizado_por = db.relationship('Usuario', foreign_keys=[autorizado_por_id])

    def __repr__(self):
        return f"SolicitacaoContrato (id={self.id}, tipo={self.tipo_contrato_id})"
