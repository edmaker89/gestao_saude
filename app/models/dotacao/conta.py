from app.ext.database import db

class Conta(db.Model):
    __tablename__ = "conta"
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return self.descricao
    
    def __str__(self) -> str:
        return f"<Conta {self.codigo}>"