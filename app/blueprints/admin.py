from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func
from app.controllers.usuario_controller import UsuarioController
from app.forms.role_form import RoleForm
from app.forms.login_form import FormLogin
from werkzeug.security import check_password_hash

from app.models.users import Usuario
from app.utils.dict_layout import button_layout

bp_admin = Blueprint("admin", __name__, '/master')

@bp_admin.route('/roles')
def roles():
    page = request.args.get('page', 1, type=int)
    ordem = request.args.get('ordem', '', type=str)
    title = 'Gestão de perfil e permissão'
    form = RoleForm()

    return render_template('/pages/roles/index.html', title=title, page=page, ordem=ordem, form=form)