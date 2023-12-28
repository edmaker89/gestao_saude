from flask import Blueprint, jsonify, render_template, request, redirect, flash, url_for
from app.forms.permission_form import PermissionForm
from app.forms.role_form import RoleForm
from app.models.role_permissions import Permission, Role, RolePermissions

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
    
@bp_admin.route('/role_permission/<id_role>', methods=["GET", "POST"])
def role_permission(id_role):
    page = request.args.get('page', 1, type=int)
    ordem = request.args.get('ordem', '', type=str)
    if ordem == '':
        ordem = 'asc'
    title='Gerenciar permissões'
    subtitle='Atribua e remova permissões dos perfis'

    role = Role.get_perfil(id_role)
    form = PermissionForm()

    role_permissions = RolePermissions.query.filter_by(role_id=id_role).all()
    permission_ids = [rp.permission_id for rp in role_permissions]
    print(role)
    print(role_permissions)
    all_permissions = Permission.query.all()
    unlinked_permissions = [p for p in all_permissions if p.permission_id not in permission_ids]
    permission_linked = [rp.permission_id for rp in role_permissions]
    categorias = []

    
    return render_template('/pages/roles/role_permission.html', 
                           title=title, 
                           subtitle=subtitle, 
                           role=role, 
                           page=page, 
                           ordem=ordem, 
                           form=form,
                           unlinked_permissions=unlinked_permissions,
                           permission_linked=permission_linked)