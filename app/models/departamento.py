from app.ext.database import db

class Departamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    
    # users = db.relationship('Usuarios', backref='departamento')

    def __repr__(self):
        return f"<Departamento {self.nome}>"