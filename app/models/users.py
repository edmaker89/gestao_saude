from app.ext.database import db
from app.ext.auth import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)

class Usuario(db.Model, UserMixin):
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
    
    def get_id(self):
        return str(self.id)
    
    @classmethod
    def get_user(cls, id_usuario):
        user = cls.query.filter(cls.id == id_usuario).first()
        return user
    
    def __repr__(self):
        return f"<Usuario {self.nome_completo}>"