from flask import jsonify, render_template
from app.controllers.usuario_controller import UsuarioController
from app.models.departamento import Departamento
from app.blueprints.mail import bp_mail
from app.blueprints.auth import bp_auth

def serialize_usuario(usuario):
    return {
        'id': usuario.id,
        'nome_completo': usuario.nome_completo,
        'departamento_id': usuario.departamento_id,
        'departamento': usuario.departamento.nome,
        'username': usuario.username,
        'senha': usuario.senha,
        'email': usuario.email,
        'tentativas_login': usuario.tentativas_login,
        'bloqueado': usuario.bloqueado,
        'role': usuario.role,
        'criado_em': usuario.criado_em.isoformat() if usuario.criado_em else None
        # Adicione outros campos conforme necessário
    }

def init_app(app):
   # registre seus blueprints ex.: app.register_blueprint(modulo)
    app.register_blueprint(bp_mail)
    app.register_blueprint(bp_auth)

    @app.route("/")
    def index():
       return {"Hello":"World"}, 200