from app.ext.database import db

class Usuario(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(255), nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    tentativas_login = db.Column(db.Integer)
    bloqueado = db.Column(db.Boolean)
    role = db.Column(db.String(255))
    criado_em = db.Column(db.TIMESTAMP)
    
   
    departamento = db.relationship('Departamento', backref='users', lazy=True)
    
    
    def __repr__(self):
        return f"<Usuario {self.nome_completo}>"