from flask import redirect, render_template, jsonify, url_for
from flask_login import login_required
from app.blueprints.mail import bp_mail
from app.blueprints.auth import bp_auth
from app.blueprints.user import bp_user
from app.blueprints.departmento import bp_depart
from app.blueprints.admin import bp_admin
from app.ext.auth import login_manager
from werkzeug.exceptions import Forbidden

def init_app(app):
   # registre seus blueprints ex.: app.register_blueprint(modulo)
   app.register_blueprint(bp_mail)
   app.register_blueprint(bp_auth)
   app.register_blueprint(bp_user)
   app.register_blueprint(bp_depart)
   app.register_blueprint(bp_admin)

   @app.errorhandler(Forbidden)
   def handle_forbidden_error(e):
      return render_template('403.html'), 403
   
   @app.errorhandler(404)
   def page_not_found(e):
      return render_template('404.html'), 404

   @app.route("/")
   @login_required
   def index():
      title = 'Avisos'
      subtitle = 'Leia com regularidade esses avisos'

      return render_template('/pages/index.html', title=title, subtitle=subtitle)
      