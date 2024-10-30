from flask import Blueprint, jsonify, render_template, request, redirect, flash, url_for
from flask_login import login_required
from app.forms.permission_form import PermissionForm
from app.forms.role_form import RoleForm
from app.forms.role_user_form import RoleUserForm
from app.models.role_permissions import Permission, Role, RolePermissions
from app.models.users import Usuario
from app.utils.breadcrumbItem import BreadcrumbManager
from app.utils.dict_layout import button_layout
from app.utils.verify_permission import permission_required

bp_admin = Blueprint("admin", __name__, url_prefix='/master')

@bp_admin.route('/roles', methods=['GET', 'POST'])
@login_required
@permission_required('gerenciamento master')
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

            except Exception as e:
                flash(f'[ERRO]: Não foi possivel atualizar o perfil! {e}', 'danger')
        try:
            Role.novo_perfil(role, descripton)
            flash('Perfil cadastrado com sucesso!', 'success')
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
    button_new_perfil = button_layout(url="openNewRole()", classname="button is-link", label="+ novo perfil", icon='', onclick=True)
    menu_ativo = "Gestão Perfis e Permissões"
    rotas = [('Início', {}), ('Gestão Perfis e Permissões', {})]
    bread_manager=BreadcrumbManager()
    breads = bread_manager.gerar_breads(rotas)
    ctx_breads = {'breads': breads, 'bread_ativo':'Gestão Perfis e Permissões'}
    return render_template('/pages/roles/index.html', **ctx_breads, menu_ativo=menu_ativo,title=title, page=page, ordem=ordem, form=form, roles=roles, button_layout=button_new_perfil)

@bp_admin.route('/api/perfil/<int:id_perfil>', methods=['GET'])
@login_required
@permission_required('acesso restrito')
def api_obter_perfil(id_perfil):
    perfil = Role.get_perfil(id_perfil)
    return jsonify({'id':id_perfil, 'nome': perfil.nome, 'descricao': perfil.descricao}) #type: ignore

@bp_admin.route('/role/delete/<id_role>')
@login_required
@permission_required('gerenciamento master')
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
@login_required
@permission_required('gerenciamento master')
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
    unlinked_permissions = [p for p in all_permissions if p.id not in permission_ids]
    permission_linked = [p for p in all_permissions if p.id in permission_ids]
    categorias = []

    print(permission_linked)
    rotas = [('Início', {}), ('Gestão Perfis e Permissões', {}), ('Gerenciar permissões', {'id_role':id_role})]
    bread_manager=BreadcrumbManager()
    breads = bread_manager.gerar_breads(rotas)
    ctx_breads = {'breads': breads, 'bread_ativo':'Gerenciar permissões'}
    
    return render_template('/pages/roles/role_permission.html',
                           **ctx_breads, 
                           title=title, 
                           subtitle=subtitle, 
                           role=role, 
                           page=page, 
                           ordem=ordem, 
                           form=form,
                           unlinked_permissions=unlinked_permissions,
                           permission_linked=permission_linked)


@bp_admin.route('/permission/new', methods=['GET', 'POST'])
@login_required
@permission_required('gerenciamento master')
def new_permission():

    if request.method == 'POST':
        form = PermissionForm(request.form)
        descricao = form.descricao.data
        nome = form.nome.data
        id_role = request.form.get('id_role')
        id_permission = request.form.get('id_permission')
        if id_permission and id_permission != 'undefined':
            try:
                permission = Permission.get_permission(id_permission)
                permission.update_permission(nome, descricao) #type: ignore
                flash('O parametro da permissão foi editado com sucesso', 'success')
            except:
                flash('Um erro inesperado aconteceu, verifique e tente novamente', 'danger')
            finally:
                return redirect(url_for('admin.role_permission', id_role=id_role))
        try:
            Permission.new_permission(nome, descricao)
            flash(f'Permissão criada com sucesso', 'success')
            return redirect(url_for('admin.role_permission', id_role=id_role))
        except Exception as e:
            flash(f'[ERRO]: Não foi possivel cadastrar nova permissão! {e}', 'danger')
            return redirect(url_for('admin.role_permission', id_role=id_role))

    return redirect(url_for('admin.roles'))

@bp_admin.route('/add_permission/<role_id>/<permission_id>')
@login_required
@permission_required('gerenciamento master')
def add_permission(role_id, permission_id):

    try:
        RolePermissions.add_permission(role_id, permission_id)
        flash(f'Permissão adicionada ao perfil', 'success')
        return redirect(url_for('admin.role_permission', id_role=role_id))
    except Exception as e:
        flash(f'[ERRO]: Não foi possivel adicionar a permissão do perfil {e}', 'danger')
        return redirect(url_for('admin.role_permission', id_role=role_id))

@bp_admin.route('/remove_permission/<role_id>/<permission_id>')
@login_required
@permission_required('gerenciamento master')
def remove_permission(role_id, permission_id):
    try:
        RolePermissions.remove_permission(role_id, permission_id)
        flash(f'Permissão removida do perfil', 'success')
        return redirect(url_for('admin.role_permission', id_role=role_id))
    except Exception as e:
        flash(f'[ERRO]: Não foi possivel remover a permissão do perfil {e}', 'danger')
        return redirect(url_for('admin.role_permission', id_role=role_id))

@bp_admin.route('/api/permission/<int:id_permission>', methods=['GET'])
@login_required
def api_obter_permission(id_permission):
    permission = Permission.get_permission(id_permission)
    return jsonify({'id':id_permission, 'nome': permission.nome, 'descricao': permission.descricao}) #type: ignore

@bp_admin.route('permission/delete/<int:id_permission>/<int:id_role>')  # type: ignore
@login_required
@permission_required('gerencimento master')
def permission_delete(id_permission: int, id_role):
    try:
        permission: Permission = Permission.get_permission(int(id_permission)) # type: ignore
        if permission is not None:
            permission.delete_permission()
        flash('A permissão foi deletada', 'success')
    except:
        flash('Não foi possivel apagar a permissão', 'danger')
    finally:
        return redirect(url_for('admin.role_permission', id_role=id_role))

@bp_admin.route('/role_user/', methods=['POST'])
@login_required
@permission_required('acesso restrito')
def role_user():
    id_departamento = request.form.get('departamento_id')
    form: RoleUserForm = RoleUserForm(request.form)
    role_id = form.role.data
    user_id = request.form.get('id_user')
    try:
        user: Usuario = Usuario.get_user(user_id) #type: ignore
        user.choice_role(role_id)
        flash('O perfil do usuario foi alterado', 'success')
    except Exception as e:
        print(e)
        flash(f'Não foi possivel altear o perfil, tente novamente {[e]}', 'danger')
    finally:
        if id_departamento:
            return redirect(url_for('organization.manager_departamento', id_departamento=id_departamento))
        return redirect(url_for('user.manager_user'))
    
