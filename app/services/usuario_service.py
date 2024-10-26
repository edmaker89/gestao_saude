from sqlalchemy import or_
from app.models.departamento import Departamento
from app.models.role_permissions import Role
from app.models.users import Usuario
from app.ext.database import db
from werkzeug.security import generate_password_hash

class UsuarioService:
    
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
            return False
    
    
    @staticmethod
    def detalhes_usuario():
        usuario = Usuario.query.get_or_404(id)
        return usuario
    
    @staticmethod
    def change_password(id_user, nova_senha):
        try:
            user = Usuario.get_user(id_user)
            hash_nova_senha = generate_password_hash(password=nova_senha)
            user.senha = hash_nova_senha
            user.tentativa = 0
        
            db.session.commit()
            return True
        except Exception as e:
            return False

    @staticmethod
    def tentativa_login_falhou(id_user):
        usuario = Usuario.query.filter(Usuario.id == id_user).first()
        tentativa_passada = usuario.tentativas_login
        
        tentativa_atual = tentativa_passada + 1
        usuario.tentativas_login = tentativa_atual
        bloqueado = 0
        if tentativa_atual >= 10:
            bloqueado = 1 
            usuario.bloqueado = bloqueado

        db.session.commit()

        return {'tentativa': tentativa_atual, 'bloqueado': bloqueado}
    
    @staticmethod
    def get_users_with_filters(nome=None, departamento_id=None, ordem='desc', page=1, per_page=20):
        query = db.session.query(
            Usuario,
            Departamento,
            Role,
        ).join(
            Departamento,
            Usuario.departamento_id == Departamento.id
        ).join(
            Role,
            Usuario.role == Role.id
        )

        if nome:
            query = query.filter(or_(Usuario.nome_completo.like(f"%{nome}%"), Usuario.username.like(f'%{nome}%')))
        if departamento_id:
            query = query.filter(Usuario.departamento_id == departamento_id)

        # Adicione a ordenação pela data ou outro campo apropriado
        if ordem == 'asc':
            query = query.order_by(Usuario.nome_completo.asc())
        else:
            query = query.order_by(Usuario.nome_completo.desc())
        
        mails = query.paginate(page=page, per_page=per_page) # type: ignore
        return mails
    
    @staticmethod
    def departamento_vazio(id_depart):

        pessoas = Usuario.query.filter(Usuario.departamento_id==id_depart).all()
        if pessoas:
            return True
        return False
    
    @staticmethod
    def departamento_list_of_users(id_depart):
        pessoas = Usuario.query.filter(Usuario.departamento_id==id_depart).order_by(Usuario.nome_completo, Usuario.ativo).all()
        if pessoas:
            return pessoas
        return False
    
    @staticmethod
    def list_of_users():
        users = Usuario.query.filter(Usuario.ativo == 1).order_by(Usuario.nome_completo).all()
        return users
    
    @staticmethod
    def enable_user(id_user):
        user = Usuario.query.filter(Usuario.id == id_user).first()
        if not user:
            raise Exception("Usuário não existe, tente novamente.")
        user.ativo = True
        db.session.commit()
        return user
        
    @staticmethod
    def disable_user(id_user):
        user = Usuario.query.filter(Usuario.id == id_user).first()
        print(user)
        if not user:
            raise Exception("Usuário não existe, tente novamente.")
        user.ativo = False
        db.session.commit()
        return user
        

