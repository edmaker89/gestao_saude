from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.controllers.usuario_controller import UsuarioController

from app.forms.reset_senha_form import ResetSenhaForm
from app.models.users import Usuario

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