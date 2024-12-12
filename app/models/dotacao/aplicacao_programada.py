from app.ext.database import db

class AplicacaoProgramada(db.Model):
    __tablename__ = 'aplicacao_programada'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(255), nullable=False, default='vigente') # vigente, arquivada
    
    def __repr__(self):
        return f"AplicativoProgramada (id={self.id}, tipo={self.numero}"