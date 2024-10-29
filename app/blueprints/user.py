from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.models import estabelecimento
from app.models.organizacao import Organizacao
from app.services.estabelecimento_service import EstabelecimentoService
from app.services.organizacao_service import OrganizacaoService
from app.services.usuario_service import UsuarioService
from app.forms.depart_form import DepartForm
from app.forms.edit_perfil_form import EditPerfilForm
from app.forms.edit_user_form import EditUserForm
from app.forms.new_user_form import NewUserForm
from app.ext.database import db
from werkzeug.security import check_password_hash, generate_password_hash

from app.forms.reset_senha_form import ResetSenhaForm
from app.forms.role_user_form import RoleUserForm
from app.models.departamento import Departamento
from app.models.users import Usuario
from app.utils.breadcrumbItem import BreadcrumbManager
from app.utils.comunications.email import novo_cadastro
from app.utils.dict_layout import button_layout
from app.utils.verify_permission import permission_required, verify_permission

bp_user = Blueprint('user', __name__, url_prefix='/user' )


@bp_user.route('/reset-password', methods=["GET", "POST"])
@login_required
def reset_password():

    if request.method == 'POST':
        form = ResetSenhaForm(request.form)
        senha_atual = form.senha_atual.data
        nova_senha = form.nova_senha.data
        confirmar_senha = form.confirmar_senha.data

        if nova_senha == confirmar_senha:
            user = Usuario.get_user(current_user.id)
            
            if check_password_hash(pwhash=user.senha, password=nova_senha): #type: ignore
                flash('A senha atual não confere com a senha salva', 'danger')
                return redirect(url_for('user.reset_password'))

            change_password = UsuarioService.change_password(current_user.id, nova_senha)
            if change_password:
                flash('Senha alterada com sucesso', 'success')
                return redirect(url_for('index'))
        else: 
            flash('A nova senha e o confirmar senha precisam ser iguais!', 'danger')     
        return redirect(url_for('user.reset_password'))

    title = "Alterar senha"
    subtitle = "Para sua segurança utilize senhas fortes"
    form = ResetSenhaForm()
    rotas = [('Início', {}), (title, {})]
    bread_manager=BreadcrumbManager()
    breads = bread_manager.gerar_breads(rotas)
    ctx_breads = {'breads': breads, 'bread_ativo':title}
    return render_template('/pages/user/password.html',
                           title=title,
                           subtitle=subtitle,
                           form=form,
                           **ctx_breads
                           )

@bp_user.route('/edit-perfil', methods=["GET", "POST"])
@login_required
def edit_perfil():

    if request.method == 'POST':
        form = EditPerfilForm(request.form)
        nome_completo = form.nome_completo.data
        departamento = form.departamento.data
        email = form.email.data

        update_user = UsuarioService.update_user(current_user.id, nome_completo, departamento, email)
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
    rotas = [('Início', {}), (title, {})]
    bread_manager=BreadcrumbManager()
    breads = bread_manager.gerar_breads(rotas)
    ctx_breads = {'breads': breads, 'bread_ativo':title}
    return render_template('/pages/user/edit_perfil.html',
                           title=title, 
                           subtitle=subtitle, 
                           form=form, 
                           user=current_user, **ctx_breads)

@bp_user.route('/create-user', methods=["GET", "POST"])
@login_required
@permission_required('acesso restrito')
def create_user():

    if request.method == "POST":
        form = NewUserForm(request.form)
        username = form.username.data
        nome_completo = form.nome_completo.data
        departamento_id = request.form.get('departamento')
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
        
        senha = str(senha)
        try:
            new_user = Usuario()
            new_user.nome_completo=nome_completo
            new_user.username=username
            new_user.senha= generate_password_hash(senha)
            new_user.departamento_id=departamento_id
            new_user.email=email
            new_user.tentativas_login = 0
            new_user.bloqueado = 0
            new_user.role = 1
            new_user.criado_em = datetime.utcnow()
            db.session.add(new_user)
            db.session.commit()

            flash(f'Usuário criado com sucesso: login {new_user.username}', 'success')
            # implementar envio de email aqui
            novo_cadastro(nome_completo=nome_completo, username=username, senha=senha, email=email)
            return redirect(url_for('user.manager_user'))
        except Exception as e:
            flash(f'Algo inesperado aconteceu, tente novamente mais tarde!', 'danger')
            return redirect(url_for('user.create_user'))

    title = "Cadastrar novo usuário"
    subtitle = ''
    form = NewUserForm()
    rotas = [('Início', {}), ('Gestão de usuários', {}), ('Novo usuário', {})]
    bread_manager=BreadcrumbManager()
    breads = bread_manager.gerar_breads(rotas)
    ctx_breads = {'breads': breads, 'bread_ativo':'Novo usuário'}
    
    organizacoes = []
    estabelecimentos = []
    
    if not verify_permission('gerenciamento master'):
        organizacao = current_user.departamento.estabelecimento.organizacao.id
        lista_estabelecimentos = EstabelecimentoService.list_all(orgao_id=organizacao)
        for estab in lista_estabelecimentos:
            estabelecimentos.append((estab.id, estab.nome))
    else:
        lista_organizacoes = OrganizacaoService.list_all()
        for org in lista_organizacoes:
            organizacoes.append((org.id, org.nome))
            
    listaDepartamentos = Departamento.query.all()
    departamentos = []
    for l in listaDepartamentos:
        departamentos.append((l.id, l.nome))
    
    return render_template('/pages/user/create_user.html', title=title, subtitle=subtitle, form=form, **ctx_breads, organizacoes=organizacoes,
                           estabelecimento=estabelecimentos)

@bp_user.route('/manager-user', methods=["GET", "POST"])
@login_required
@permission_required('acesso restrito')
def manager_user():
    page = request.args.get('page', 1, type=int)
    ordem = request.args.get('ordem', '', type=str)
    nome = request.args.get('nome', '', type=str)
    mostrar_inativo = request.args.get('mostrar_inativo', None, int)
    departamento = request.args.get('departamento', '', type=int)
    organizacao = request.args.get('organizacao', '', type=int)
    estabelecimento = request.args.get('estabelecimento', '', type=int)
    
    organizacoes = []
    estabelecimentos = []
    
    if not verify_permission('gerenciamento master'):
        organizacao = current_user.departamento.estabelecimento.organizacao.id
        lista_estabelecimentos = EstabelecimentoService.list_all(orgao_id=organizacao)
        for estab in lista_estabelecimentos:
            estabelecimentos.append((estab.id, estab.nome))
    else:
        lista_organizacoes = OrganizacaoService.list_all()
        for org in lista_organizacoes:
            organizacoes.append((org.id, org.nome))
        
    button = button_layout(url='user.create_user', label='Novo Usuario', icon='fa-solid fa-user-plus', classname='button is-primary')

    listaDepartamentos = Departamento.query.all()
    departamentos = []
    for l in listaDepartamentos:
        departamentos.append((l.id, l.nome))

    form = RoleUserForm()

    listaUsuarios = UsuarioService.get_users_with_filters(page=page, ordem=ordem, nome=nome, organizacao_id=organizacao, estabelecimento_id=estabelecimento, departamento_id=departamento, mostrar_inativo=mostrar_inativo)
    title = 'Gestão de usuários'
    
    ctx = {
        'form': form, 
        'title': title, 
        'departamentos': departamentos,
        'organizacoes': organizacoes,
        'estabelecimentos': estabelecimentos,
        'ordem':ordem, 
        'usuarios': listaUsuarios, 
        'button_layout': button, 
        'page': page, 
        'nome': nome, 
        'departamento': departamento,
        'mostrar_inativo': mostrar_inativo,
        'menu_ativo': 'Gestão de usuários',
        'organizacao': organizacao
    }
    
    rotas = [('Início', {}), (title, {})]
    bread_manager=BreadcrumbManager()
    breads = bread_manager.gerar_breads(rotas)
    ctx_breads = {'breads': breads, 'bread_ativo':title}
    ctx.update(**ctx_breads)
    
    return render_template('/pages/user/manager_user.html', **ctx)

@bp_user.route('/edit-user/<id_user>', methods=['GET', 'POST'])
@login_required
@permission_required('acesso restrito')
def edit_user(id_user):
    user = Usuario.get_user(id_user)
    
    if request.method == 'POST':
        id_depart = request.form.get('id_departamento', None, int)
        form = EditUserForm(request.form)
        id = id_user
        username = form.username.data
        nome_completo = form.nome_completo.data
        departamento_id = form.departamento.data
        email = form.email.data
        
        update_user = UsuarioService.update_user(id, nome_completo, departamento_id, email, username=username) #type: ignore

        if update_user:
            flash('Usuario editado com sucesso!', 'success')
            if id_depart:
                return redirect(url_for('organization.manager_departamento', id_departamento=id_depart))
            return redirect(url_for('user.manager_user'))
        else:
            flash('Um erro inesperado aconteceu, tente novamente mais tarde', 'danger')
            if id_depart:
                return redirect(url_for('user.edit_user', id_user=id_user, id_departamento=id_depart))
            return redirect(url_for('user.edit_user', id_user=id_user))
    
    title='Editar Usuário'
    subtitle = ''
    form = EditUserForm()
    form.username.data = user.username #type: ignore
    form.nome_completo.data = user.nome_completo #type: ignore
    form.email.data = user.email #type: ignore
    
    id_organizacao = user.departamento.estabelecimento.organizacao.id
    id_estabelecimento = user.departamento.estabelecimento.id
    id_departamento = user.departamento.id

    rotas = [('Início', {}), ('Gestão de usuários', {}), ('Editar usuário', {'id_user': id_user})]
    bread_manager=BreadcrumbManager()
    breads = bread_manager.gerar_breads(rotas)
    ctx_breads = {'breads': breads, 'bread_ativo':'Editar usuário'}
    
    organizacoes = []
    estabelecimentos = []
    
    if not verify_permission('gerenciamento master'):
        organizacao = current_user.departamento.estabelecimento.organizacao.id
        lista_estabelecimentos = EstabelecimentoService.list_all(orgao_id=organizacao)
        for estab in lista_estabelecimentos:
            estabelecimentos.append((estab.id, estab.nome))
    else:
        lista_organizacoes = OrganizacaoService.list_all()
        for org in lista_organizacoes:
            organizacoes.append((org.id, org.nome))
            
    listaDepartamentos = Departamento.query.all()
    departamentos = []
    for l in listaDepartamentos:
        departamentos.append((l.id, l.nome))
    
    return render_template('/pages/user/create_user.html', 
                           **ctx_breads,id_departamento=id_departamento, id_organizacao=id_organizacao, id_estabelecimento=id_estabelecimento,
                           title=title, subtitle=subtitle, form=form, id_user=id_user, organizacoes=organizacoes,
                           estabelecimento=estabelecimentos)

@bp_user.route('/lock/<id_user>')
@login_required
@permission_required('acesso restrito')
def lock(id_user):
    id_departamento = request.args.get('id_departamento', None, int)
    lock = Usuario.lock_user(id_user)
    if lock:
        flash(f'O usuário {lock.nome_completo} foi bloqueado', 'success')
        
    else:
        flash(f'Algo inesperado aconteceu, tente novamente mais tarde', 'danger')
    if id_departamento:
        return redirect(url_for('organization.manager_departamento', id_departamento=id_departamento))
    return redirect(url_for('user.manager_user'))   
    
@bp_user.route('/unlock/<id_user>')
@login_required
@permission_required('acesso restrito')
def unlock(id_user):
    id_departamento = request.args.get('id_departamento', None, int)
    lock = Usuario.unlock_user(id_user)
    if lock:
        flash(f'O usuário {lock.nome_completo} foi desbloqueado', 'success')
    
    else:
        flash(f'Algo inesperado aconteceu, tente novamente mais tarde', 'danger')
    if id_departamento:
        return redirect(url_for('organization.manager_departamento', id_departamento=id_departamento))
    return redirect(url_for('user.manager_user'))
    
@bp_user.route('/disable/<id_user>')
@login_required
@permission_required('acesso restrito')
def disable(id_user):
    id_departamento = request.args.get('id_departamento', None, int)
    
    try:
        user = UsuarioService.disable_user(id_user)
        flash(f'O usuário {user.nome_completo} foi desativado', 'success')   
    except Exception as e:
        flash(f'Algo inesperado aconteceu, tente novamente mais tarde', 'danger')
    
    if id_departamento:
        return redirect(url_for('organization.manager_departamento', id_departamento=id_departamento))
    return redirect(url_for('user.manager_user'))
    
@bp_user.route('/enable/<id_user>')
@login_required
@permission_required('acesso restrito')
def enable(id_user):
    id_departamento = request.args.get('id_departamento', None, int)
    
    try:
        user = UsuarioService.enable_user(id_user)
        flash(f'O usuário {user.nome_completo} foi ativado', 'success')   
    except Exception:
        flash(f'Algo inesperado aconteceu, tente novamente mais tarde', 'danger')
    
    if id_departamento:
        return redirect(url_for('organization.manager_departamento', id_departamento=id_departamento))
    return redirect(url_for('user.manager_user'))

@bp_user.route('reset_pass', methods=['GET', 'POST'])
@login_required
@permission_required('acesso restrito')
def reset_pass():
    id_departamento = request.form.get('departamento_id')
    if request.method == 'POST':
        form = request.form
        nova_senha = form.get('nova_senha')
        confirmar_senha = form.get('confirmar_senha')
        user_id = form.get('user_id')

        if nova_senha == confirmar_senha:
            reset_senha = UsuarioService.change_password(user_id, nova_senha)

            if reset_senha:
                flash('Senha Alterada com sucesso', 'success')
            else:
                flash('Houve um erro inesperado, tente novamente mais tarde!', 'danger')
        else:
            flash('A nova senha e a confirmar senha não coicidem, tente novamente', 'danger')
    else:
        flash('O metodo de requisição da rota não pode ser aceito', 'info')
    
    if id_departamento:
        return redirect(url_for('organization.manager_departamento', id_departamento=id_departamento))
    return redirect(url_for('user.manager_user'))