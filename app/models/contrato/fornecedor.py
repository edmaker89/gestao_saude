from app.ext.database import db

class Fornecedor(db.Model):
    __tablename__ = 'fornecedor'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    tipo_pessoa = db.Column(db.String(255), nullable=False)
    cpf_cnpj = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"Tipo Contrato (id={self.id}, nome={self.nome}"