from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required

from app.forms.reset_senha_form import ResetSenhaForm

bp_user = Blueprint('user', __name__, url_prefix='/user' )


@bp_user.route('/reset-password', methods=["GET", "POST"])
@login_required
def reset_password():

    if request.method == 'POST':
        form = ResetSenhaForm(request.form)
        senha_atual = form.senha_atual.data
        nova_senha = form.nova_senha.data
        confirmar_senha = form.confirmar_senha.data

        return redirect(url_for('user.reset_password'))

    title = "Alterar senha"
    subtitle = "Para sua segurança utilize senhas fortes"
    form = ResetSenhaForm()

    return render_template('/pages/user/password.html',
                           title=title,
                           subtitle=subtitle,
                           form=form
                           )