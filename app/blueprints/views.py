from flask import jsonify, render_template
from app.controllers.usuario_controller import UsuarioController
from app.models.departamento import Departamento
from app.blueprints.mail import bp_mail

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

    @app.route("/")
    def index():
       return {"Hello":"World"}, 200

    @app.route('/lista_usuarios')
    def lista_usuarios():
       lista = UsuarioController.lista_usuarios()
       lista_serializada = [serialize_usuario(usuario) for usuario in lista]
    
       return jsonify(lista_serializada)

    @app.route('/departamento')
    def departamento():
      depart = Departamento.query.all()
      return "departamento"
  
    @app.route('/base')
    def base():
        return render_template('base.html')