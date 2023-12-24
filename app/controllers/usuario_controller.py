from app.models.users import Usuario
from app.ext.database import db

class UsuarioController:
    
    @staticmethod
    def update_user(id_user, nome_completo, departamento_id, email, username=''):
        try:
            user = Usuario.query.filter(Usuario.id == id_user).first()
            user.nome_completo = nome_completo
            user.departamento_id = departamento_id
            user.email = email

            if username != '':
                user.username = username

            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    
    
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

    @staticmethod
    def tentativa_login_falhou(id_user):
        usuario = Usuario.query.filter(Usuario.id == id_user).first()
        tentativa_passada = usuario.tentativas_login
        
        tentativa_atual = tentativa_passada + 1
        usuario.tentativas_login = tentativa_atual
        bloqueado = 0
        if tentativa_atual >= 3:
            bloqueado = 1 
            usuario.bloqueado = bloqueado

        db.session.commit()

        return {'tentativa': tentativa_atual, 'bloqueado': bloqueado}