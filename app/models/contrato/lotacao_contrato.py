from app.ext.database import db

class LotacaoContrato(db.Model):
    __tablename__ = 'lotacao_contrato'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"Tipo Contrato (id={self.id}, nome={self.nome}"