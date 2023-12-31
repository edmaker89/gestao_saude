from flask import abort, flash, redirect, render_template, jsonify, request, url_for
from flask_login import login_required
from app.blueprints.mail import bp_mail
from app.blueprints.auth import bp_auth
from app.blueprints.user import bp_user
from app.blueprints.departmento import bp_depart
from app.blueprints.admin import bp_admin
from app.controllers.usuario_controller import UsuarioController
from app.ext.auth import login_manager
from werkzeug.exceptions import Forbidden
from app.models.token import Token

from app.models.users import Usuario
from app.utils.comunications.email import novo_cadastro, solicitação_de_recuperacao

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
   
   @app.route('/redefinir_senha/solicitacao', methods=['POST'])
   def redefinir_senha_solicitacao():
      form = request.form
      email = form.get('email')
      user = Usuario.query.filter(Usuario.email == email).first()
      if user:
         solicitacao = solicitação_de_recuperacao(nome_completo=user.nome_completo, username=user.username, email=user.email, user_id=user.id)
         print(solicitacao)
         flash('Em breve chegará um link de para recuperação de senha no email informado', 'success')
         return redirect(url_for('auth.login'))
      else:
         flash('Não foi encontrado nenhum usuario com esse e-mail', 'danger')
         return redirect(url_for('auth.login'))

   
   @app.route('/redefinir-senha/<username>', methods=['GET', 'POST'])
   def redefinir_senha(username):

      if request.method == "POST":
         form = request.form
         username = form.get('username')
         token = form.get('token')
         senha = form.get('senha')
         confirmar_senha = form.get('confirmar_senha')

         if senha == confirmar_senha:
            print(
               {
                  'username': username,
                  'token': token,
                  'senha': senha,
                  'confirmar_senha': confirmar_senha,
                  }
               )
            if token != '':
               print('O token não é nulo')
               token_validado = Token.token_valido(token)
               print(token_validado.user_id)
               if token_validado:
                  user = Usuario.query.filter(Usuario.id==token_validado.user_id).first()
                  print(user)
                  if user and user.username == username:
                     print(user, user.username, username)
                     try:
                        UsuarioController.change_password(user.id, senha)
                        flash('Senha redefinida com sucesso!', 'success')
                        return redirect(url_for('auth.login'))
                     except Exception as e:
                        flash('Algo inesperado aconteceu, tente novamente', 'danger')
                        return redirect(url_for('auth.login'))
                  print('if user, and user.name username')
                  return redirect(abort(404))
               print('problema no token')
               return redirect(abort(404))
            else:
               print('primeiro if')
               return redirect(abort(404))
         else:
            flash('A senha e confirmar senha precisam ser iguais', 'danger')


      username = username
      token = request.args.get('token', '', type=str)
      if token != '':
         print('O token não é nulo')
         token_validado = Token.token_valido(token)
         print(token_validado.user_id)
         if token_validado:
            user = Usuario.query.filter(Usuario.id==token_validado.user_id).first()
            print(user)
            if user and user.username == username:
               print(user, user.username, username)
               return render_template('/pages/recuperacao_senha.html', token=token, username=username)
            print('if user, and user.name username')
            return redirect(abort(404))
         print('problema no token')
         return redirect(abort(404))
      else:
         print('primeiro if')
         return redirect(abort(404))


   @app.route("/")
   @login_required
   def index():
      title = 'Avisos'
      subtitle = 'Leia com regularidade esses avisos'

      return render_template('/pages/index.html', title=title, subtitle=subtitle)
   
      