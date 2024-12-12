from app.ext.database import db

class Fonte(db.Model):
    __tablename__ = 'fonte'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return self.codigo