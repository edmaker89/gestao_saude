from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app.controllers.usuario_controller import UsuarioController
from app.forms.login_form import FormLogin
from werkzeug.security import check_password_hash

from app.models.users import Usuario

bp_auth = Blueprint("auth", __name__)

@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    proxima = request.args.get('proxima')
    form = FormLogin()
    if proxima == None:
        proxima = url_for('index')
    return render_template('/pages/login.html', form=form, proxima=proxima)

@bp_auth.route('/autenticar', methods=['GET', 'POST'])
def autenticar():
    form = FormLogin(request.form)
    usuario = Usuario.query.filter_by(username=form.username.data).first()
    if usuario == None:
        flash('Usuario ou senha Invalida, tente novamente!', 'danger')
        return redirect(url_for('auth.login'))
    if usuario.bloqueado == 1:
        flash('Usuário bloqueado! Entre em contato com suporte ao sistema', 'danger')
        return redirect(url_for('auth.login'))
    # if usuario and bcrypt.check_password_hash(usuario.no_senha, form.no_senha.data):
    senha = form.password.data

    if usuario and senha:
        if usuario.senha == senha:
        # if check_password_hash(usuario.no_senha, senha):
            login_user(usuario)
            # session['usuario_logado'] = usuario.id_usuario
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        
    # usuario valido porém a senha não coincide
    tentativa_login = UsuarioController.tentativa_login_falhou(usuario.id)
    if tentativa_login['bloqueado'] == 1:
        flash('Usuário bloqueado! Entre em contato com suporte ao sistema', 'danger')
        return redirect(url_for('auth.login'))
    
    flash(f'Usuario ou senha Invalida, {10 - tentativa_login['tentativa']} tentativas para bloquear', 'danger')
    return redirect(url_for('auth.login'))

@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))