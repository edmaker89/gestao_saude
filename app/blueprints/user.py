from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.controllers.usuario_controller import UsuarioController
from app.forms.edit_perfil_form import EditPerfilForm
from app.forms.new_user_form import NewUserForm
from app.ext.database import db

from app.forms.reset_senha_form import ResetSenhaForm
from app.models.departamento import Departamento
from app.models.users import Usuario
from app.utils.dict_layout import button_layout

bp_user = Blueprint('user', __name__, url_prefix='/user' )


@bp_user.route('/reset-password', methods=["GET", "POST"])
@login_required
def reset_password():
# implementar hash
    if request.method == 'POST':
        form = ResetSenhaForm(request.form)
        senha_atual = form.senha_atual.data
        nova_senha = form.nova_senha.data
        confirmar_senha = form.confirmar_senha.data

        if nova_senha == confirmar_senha:
            user = Usuario.get_user(current_user.id)

            if user.senha != senha_atual:
                flash('A senha atual não confere com a senha salva', 'danger')
                return redirect(url_for('user.reset_password'))

            change_password = UsuarioController.change_password(current_user.id, nova_senha)
            if change_password:
                flash('Senha alterada com sucesso', 'success')
                return redirect(url_for('index'))
        else: 
            flash('A nova senha e o confirmar senha precisam ser iguais!', 'danger')
        print('não trocou a senha')       
        return redirect(url_for('user.reset_password'))

    title = "Alterar senha"
    subtitle = "Para sua segurança utilize senhas fortes"
    form = ResetSenhaForm()

    return render_template('/pages/user/password.html',
                           title=title,
                           subtitle=subtitle,
                           form=form
                           )

@bp_user.route('/edit-perfil', methods=["GET", "POST"])
@login_required
def edit_perfil():

    if request.method == 'POST':
        form = EditPerfilForm(request.form)
        nome_completo = form.nome_completo.data
        departamento = form.departamento.data
        email = form.email.data

        update_user = UsuarioController.update_user(current_user.id, nome_completo, departamento, email)
        if update_user:
            flash("Perfil alterado com sucesso", 'success')
            return redirect(url_for('index'))
        else:
            flash("Aconteceu um erro inesperado, tente nomente mais tarde!", "danger")
            return redirect(url_for('/user.edit_perfil'))

    title = "Editar perfil"
    subtitle = "Complete as informações sobre você"
    form = EditPerfilForm()

    form.nome_completo.data = current_user.nome_completo
    form.departamento.data = current_user.departamento_id
    form.email.data = current_user.email

    return render_template('/pages/user/edit_perfil.html',
                           title=title, 
                           subtitle=subtitle, 
                           form=form, 
                           user=current_user)

@bp_user.route('/create-user', methods=["GET", "POST"])
@login_required
def create_user():

    if request.method == "POST":
        form = NewUserForm(request.form)
        username = form.username.data
        nome_completo = form.nome_completo.data
        departamento_id = form.departamento.data
        email = form.email.data
        senha = form.senha.data
        confirmar_senha = form.confirmar_senha.data

        if senha != confirmar_senha:
            flash('Os campos senha e confirmar senha não estão iguais', 'danger')
            return redirect(url_for('user.create_user'))
        
        exist_user = Usuario.exist_user(username)
        if exist_user:
            flash('O nome de usuário já existe, tente outro!')
            return redirect(url_for('user.create_user'))
        exist_email = Usuario.exist_email(email)
        if exist_email:
            flash('O esse email ja esta cadastrado no banco de dados, tente outro email!', 'danger')
            return redirect(url_for('user.create_user'))
        try:
            new_user = Usuario()
            new_user.nome_completo=nome_completo
            new_user.username=username
            new_user.senha=senha
            new_user.departamento_id=departamento_id
            new_user.email=email
            new_user.tentativas_login = 0
            new_user.bloqueado = 0
            new_user.role = 'user'
            new_user.criado_em = datetime.utcnow()
            db.session.add(new_user)
            db.session.commit()

            flash(f'Usuario criado com sucesso: login {new_user.username}', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            flash(f'Algo inesperado aconteceu, tente novamente mais tarde!', 'danger')
            return redirect(url_for('user.create_user'))

    title = "Cadastrar novo usuário"
    subtitle = ''
    form = NewUserForm()

    return render_template('/pages/user/create_user.html', title=title, subtitle=subtitle, form=form)

@bp_user.route('/manager-user', methods=["GET", "POST"])
@login_required
def manager_user():
    ordem = 'asc'

    button = button_layout(url='user.create_user', label='Novo Usuario', icon='fa-solid fa-user-plus', classname='button is-primary')

    listaDepartamentos = Departamento.query.all()
    departamentos = []
    for l in listaDepartamentos:
        departamentos.append((l.id, l.nome))

    listaUsuarios = Usuario.query.all()
    title = 'Gestão de Usuarios'
    return render_template('/pages/user/manager_user.html', title=title, departamentos=departamentos, ordem=ordem, usuarios=listaUsuarios, button_layout=button)