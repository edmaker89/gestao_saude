from app.ext.database import db
from app.ext.auth import login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)

class Usuario(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(255), nullable=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(255), nullable=True, unique=True)
    tentativas_login = db.Column(db.Integer)
    bloqueado = db.Column(db.Boolean)
    role = db.Column(db.String(255), db.ForeignKey('role.id'), nullable=False)
    criado_em = db.Column(db.TIMESTAMP)
    
    departamento = db.relationship('Departamento', backref='users', lazy=True)
    perfil = db.relationship('Role', backref='users', lazy=True)
    
    def get_id(self):
        return str(self.id)
    
    @classmethod
    def get_user(cls, id_usuario):
        user = cls.query.filter(cls.id == id_usuario).first()
        return user
    
    @classmethod
    def create_user(cls, nome_completo, departamento_id, username, senha, email):

        new_user = cls(
            nome_completo=nome_completo,
            username=username,
            senha=senha,
            departamento_id=departamento_id,
            email=email,
            tentativas_login = 0,
            bloqueado = 0,
            role = 'user',
            criado_em = datetime.utcnow()
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            return f"[ERRO]: {e}"
    
    @classmethod
    def exist_user(cls, username):
        username_exist = cls.query.filter(cls.username == username).first()
        
        if username_exist:

            return True
        return False
    
    @classmethod
    def exist_email(cls, email):
        email_exist = cls.query.filter(cls.email == email).first()
        
        if email_exist:

            return True
        return False
    
    @classmethod
    def lock_user(cls, id_user):
        try:
            user = cls.get_user(id_user)
            user.bloqueado = 1 #type: ignore
            db.session.commit()

            return user
        except Exception as e:
            return False

    @classmethod
    def unlock_user(cls, id_user):
        try:
            user = cls.get_user(id_user)
            user.bloqueado = 0 #type: ignore
            user.tentativas_login = 0 #type: ignore
            db.session.commit()

            return user
        except Exception as e:
            return False
    
    def choice_role(self, role_id):
        self.role = role_id
        db.session.commit()

    def resetar_tentativas(self):
        self.tentativas_login = 0
        db.session.commit()
    
    
    def __repr__(self):
        return f"<Usuario {self.nome_completo}>"