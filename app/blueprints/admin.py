from socket import BTPROTO_RFCOMM
from flask import Blueprint, jsonify, render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func
from app.controllers.usuario_controller import UsuarioController
from app.forms.role_form import RoleForm
from app.forms.login_form import FormLogin
from werkzeug.security import check_password_hash
from app.models.role_permissions import Role

from app.models.users import Usuario
from app.utils.dict_layout import button_layout

bp_admin = Blueprint("admin", __name__, url_prefix='/master')

@bp_admin.route('/roles', methods=['GET', 'POST'])
def roles():
    if request.method == 'POST':
        form = RoleForm(request.form)
        role = form.role.data
        descripton = form.description.data
        id_role = request.form.get('id_role')
        print('id_role', id_role)
        if id_role and id_role != 'undefined':
            try:
                Role.update_perfil(id_role, role, descripton)
                flash('Perfil editado com sucesso!', 'success')
                return redirect(url_for('admin.roles'))
            except Exception as e:
                flash(f'[ERRO]: Não foi possivel atualizar o perfil! {e}', 'danger')
            return redirect(url_for('admin.roles'))
        try:
            Role.novo_perfil(role, descripton)
            flash('Perfil cadastrado com sucesso!', 'success')
            return redirect(url_for('admin.roles'))
        except Exception as e:
            flash(f'[ERRO]: Não foi possivel cadastrar novo perfil! {e}', 'danger')
            return redirect(url_for('admin.roles'))

    page = request.args.get('page', 1, type=int)
    ordem = request.args.get('ordem', '', type=str)
    if ordem == '':
        ordem = 'asc'
    title = 'Gestão de perfil e permissão'
    form = RoleForm()

    roles = Role.list_perfis(ordem=ordem, page=page, per_page=20)

    return render_template('/pages/roles/index.html', title=title, page=page, ordem=ordem, form=form, roles=roles)

@bp_admin.route('/api/perfil/<int:id_perfil>', methods=['GET'])
def api_obter_perfil(id_perfil):
    perfil = Role.get_perfil(id_perfil)
    return jsonify({'id':id_perfil, 'nome': perfil.nome, 'descricao': perfil.descricao}) #type: ignore

@bp_admin.route('/role/delete/<id_role>')
def delete_role(id_role):
    try:
        role = Role.get_perfil(id_role)
        role.delete_perfil() #type: ignore
        flash(f'Perfil apagado com sucesso', 'success')
        return redirect(url_for('admin.roles'))
    except Exception as e:
        flash(f'[ERRO]: Não foi possivel apagar o perfil! {e}', 'danger')
        return redirect(url_for('admin.roles'))
    
