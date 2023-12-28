from flask import render_template
from flask_login import login_required
from app.blueprints.mail import bp_mail
from app.blueprints.auth import bp_auth
from app.blueprints.user import bp_user
from app.blueprints.departmento import bp_depart
from app.blueprints.admin import bp_admin

def init_app(app):
   # registre seus blueprints ex.: app.register_blueprint(modulo)
    app.register_blueprint(bp_mail)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_depart)
    app.register_blueprint(bp_admin)

   # exemplo de uso das permissões no contexto do template
   #  {% if 'editar_recurso' in user_permissions %}
   #  {# Exibir algum conteúdo para usuários com a permissão 'editar_recurso' #}
   #  {% endif %}

    @app.route("/")
    @login_required
    def index():
       title = 'Avisos'
       subtitle = 'Leia com regularidade esses avisos'

       return render_template('/pages/index.html', title=title, subtitle=subtitle)