from app.models.users import Usuario


class UsuarioController:
    
    @staticmethod
    def lista_usuarios():
        usuarios = Usuario.query.all()
        return usuarios
    
    @staticmethod
    def detalhes_usuario():
        usuario = Usuario.query.get_or_404(id)
        return usuario
    
    