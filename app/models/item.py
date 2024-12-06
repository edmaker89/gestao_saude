from app.ext.database import db

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    preco_unitario = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"Tipo Contrato (id={self.id}, descricao={self.descricao}"