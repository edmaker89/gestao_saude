from math import exp
from app.models.users import Usuario
from app.ext.database import db

class UsuarioController:
    
    @staticmethod
    def lista_usuarios():
        usuarios = Usuario.query.all()
        return usuarios
    
    @staticmethod
    def detalhes_usuario():
        usuario = Usuario.query.get_or_404(id)
        return usuario
    
    @staticmethod
    def change_password(id_user, nova_senha):
        try:
            user = Usuario.get_user(id_user)
            user.senha = nova_senha
        
            db.session.commit()
            print('retornou true')
            return True
        except Exception as e:
            print(e)
            return False
    