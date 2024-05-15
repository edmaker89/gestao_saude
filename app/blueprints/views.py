from flask import abort, flash, redirect, render_template, jsonify, request, url_for
from flask_login import current_user, login_required
from app.blueprints.mail import bp_mail
from app.blueprints.auth import bp_auth
from app.blueprints.user import bp_user
from app.blueprints.departmento import bp_depart
from app.blueprints.admin import bp_admin
from app.controllers.usuario_controller import UsuarioController
from app.ext.auth import login_manager
from werkzeug.exceptions import Forbidden
from app.forms.avisos_form import AvisosForm
from app.models.avisos import Avisos
from app.models.token import Token
from app.ext.database import db
from app.blueprints.regulacao import bp_regulacao
from app.blueprints.survey import bp_survey

from app.models.users import Usuario
from app.utils.comunications.email import novo_cadastro, solicitação_de_recuperacao

import markdown

def init_app(app):
   # registre seus blueprints ex.: app.register_blueprint(modulo)
   app.register_blueprint(bp_mail)
   app.register_blueprint(bp_auth)
   app.register_blueprint(bp_user)
   app.register_blueprint(bp_depart)
   app.register_blueprint(bp_admin)
   app.register_blueprint(bp_regulacao)
   app.register_blueprint(bp_survey)

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
      avisos = Avisos.query.order_by(Avisos.create_at.desc()).all()
      avisos_html = [markdown.markdown(aviso.descricao.replace(r'\n', '<br>')) for aviso in avisos]

      return render_template('/pages/index.html', title=title, subtitle=subtitle, avisos=zip(avisos, avisos_html))
   
   @app.route('/aviso/edit/<id_aviso>', methods=['GET', 'POST'])
   @login_required
   def aviso_edit(id_aviso):
      aviso = Avisos.query.filter(Avisos.id == id_aviso).first()
      if request.method == 'POST':
         form = AvisosForm(request.form)
         aviso.descricao = form.descricao.data 
         aviso.titulo = form.titulo.data

         try:
            db.session.commit()
            flash('Aviso editado com sucesso', 'success')
            return redirect(url_for('index'))
         except:
            flash('Ocorreu um erro inesperado, tente novamente', 'danger')
            return redirect(url_for('aviso_edit', id_aviso=id_aviso))

      title = 'Editar Aviso'
      form = AvisosForm()
      form.descricao.data = aviso.descricao
      form.titulo.data = aviso.titulo

      return render_template ('/pages/avisos/form.html', form=form, aviso=aviso, title=title, id_aviso=id_aviso)
   
   @app.route('/aviso/new/', methods=['GET', 'POST'])
   @login_required
   def aviso_new():
      if request.method == 'POST':
         new_aviso = Avisos()
         form = AvisosForm(request.form)
         titulo = form.titulo.data
         descricao = form.descricao.data
         new_aviso.autor = current_user.id
         new_aviso.titulo = titulo
         new_aviso.descricao = descricao

         try:
            db.session.add(new_aviso)
            db.session.commit()
            flash('Aviso criado com sucesso', 'success')
            return redirect(url_for('index'))
         except:
            flash('Ocorreu um erro inesperado, tente novamente', 'danger')
            return redirect(url_for('aviso_new'))
         
      title = 'Criar aviso'
      form = AvisosForm()
      return render_template ('/pages/avisos/form.html', form=form, title=title)
   
   @app.route('/aviso/delete/<id_aviso>')
   @login_required
   def delete_aviso(id_aviso):
      aviso = Avisos.query.filter(Avisos.id == id_aviso).first()
      
      try:
         db.session.delete(aviso)
         db.session.commit()
         flash('Aviso apagado com sucesso', 'success')
         return redirect(url_for('index'))
      except:
         flash('Erro ao tentar apagar o aviso, tente novamente mais tarde!', 'danger')
         return redirect(url_for('index'))
