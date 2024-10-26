from flask import Blueprint, flash, jsonify, make_response, redirect, render_template, request, url_for
from flask_login import login_required
from app.forms.role_user_form import RoleUserForm
from app.models import estabelecimento
from app.services.departamento_service import DepartamentoService
from app.services.estabelecimento_service import EstabelecimentoService
from app.services.organizacao_service import OrganizacaoService
from app.services.usuario_service import UsuarioService


bp_org = Blueprint('organization', __name__, url_prefix='/organization' )


@bp_org.route('/manager/new_org')
@login_required
def manager_new_org():
    title = 'Gestão Organizacional'
    subtitle = "Organização / Estabelecimentos / Departamentos"
    page = request.args.get('page', 1, type=int)
    ordem = request.args.get('ordem', 'asc', type=str)
    menu_ativo = "Gestão Organizacional"

    usuarios = UsuarioService.list_of_users()
    organizacoes = OrganizacaoService.list_all()
    
    ctx ={
        'menu_ativo':menu_ativo, 
        'page':page, 
        'ordem':ordem, 
        'title':title,
        'subtitle':subtitle,
        'usuarios':usuarios,
        'organizacoes': organizacoes
    }

    return render_template('/pages/organizacional/manager.html', **ctx)

@bp_org.route('/manager/org/create', methods=['POST']) # type: ignore
@login_required
def create_new_org():
    form = request.form
    nome = form.get('nome', '', str)
    sigla = form.get('sigla', '', str)
    responsavel  = form.get('responsavel', None, int)
    
    try:
        OrganizacaoService.create(nome=nome, sigla=sigla, id_responsavel=responsavel)
        flash('Organização criada com sucesso', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(str(e), 'danger')
    
    return redirect(url_for('organization.manager_new_org'))

@bp_org.route('/manager/org/edit', methods=['POST']) # type: ignore
@login_required
def edit_org():
    form = request.form
    id = form.get('id_org', 0, int)
    nome = form.get('nome', '', str)
    sigla = form.get('sigla', '', str)
    responsavel  = form.get('responsavel', None, int)
    
    try:
        OrganizacaoService.update(id=id, nome=nome, sigla=sigla, id_responsavel=responsavel)
        flash('Dados da organização foram editados com sucesso', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(str(e), 'danger')
    
    return redirect(url_for('organization.manager_org', id_org=id))

@bp_org.route('/manager/org/<int:id_org>/')
def manager_org(id_org):
    usuarios = UsuarioService.list_of_users()
    org = OrganizacaoService.get_by_id(id=id_org)
    if not org:
        flash('A organização solicitada não pode ser encontrada ou não existe', 'danger')
        return redirect(url_for('organization.manager_new_org'))
    
    estabelecimentos = EstabelecimentoService.list_all(id_org)
    
    ctx = {
        'org': org,
        'menu_ativo': "Gestão Organizacional",
        'title': org.nome,
        'subtitle': 'Gerenciamento da organização',
        'usuarios': usuarios,
        'estabelecimentos': estabelecimentos
    }
    
    return render_template('/pages/organizacional/manager_org.html', **ctx)

@bp_org.route('/manager/new/estabelecimento', methods=['POST']) # type: ignore
def new_estabelecimento():
    id_org = request.form.get('id_org', 0, int)
    nome = request.form.get('nome')
    responsavel_id = request.form.get('responsavel', 0, int)
    
    if not nome:
        flash('Erro: Nome é obrigatórios.', 'danger')
        return redirect(url_for('organization.manager_org', id_org=id_org))
    
    try:
        EstabelecimentoService.create(orgao_id=id_org, nome=nome, id_responsavel=responsavel_id)
    except ValueError as ve:
        flash(f'Erro: {ve}', 'danger')
        return redirect(url_for('organization.manager_org', id_org=id_org))
    except Exception as e:
        flash(f'Erro: Aconteceu um erro inesperado. str{e}', 'danger')
        return redirect(url_for('organization.manager_org', id_org=id_org))
        
    flash('Estabelecimento criado com sucesso!', 'success')
    return redirect(url_for('organization.manager_org', id_org=id_org))

@bp_org.route('/manager/estabelecimento/edit', methods=['POST']) # type: ignore
@login_required
def edit_estab():
    form = request.form
    estabelecimento_id = form.get('estabelecimento_id', 0, int)
    nome = form.get('nome', '', str)
    responsavel  = form.get('responsavel', None, int)
    
    try:
        EstabelecimentoService.update(id=estabelecimento_id, nome=nome, id_responsavel=responsavel)
        flash('Dados do estabelecimento foram editados com sucesso', 'success')
    except ValueError as e:
        flash(str(e), 'danger')
    except Exception as e:
        flash(str(e), 'danger')
    
    return redirect(url_for('organization.manager_estab', id_estab=estabelecimento_id))

@bp_org.route('/manager/estabelecimento/<int:id_estab>/')
def manager_estab(id_estab):
    usuarios = UsuarioService.list_of_users()
    estab = EstabelecimentoService.get_by_id(id=id_estab)
    org = OrganizacaoService.get_by_id(estab.orgao_id) #type:ignore
    if not estab:
        flash('O estabelecimento solicitado não pode ser encontrado ou não existe', 'danger')
        return redirect(url_for('organization.manager_new_org'))
    
    departamentos = DepartamentoService.list_all_by_estab(id_estab)
    
    ctx = {
        'org': org,
        'estab': estab,
        'menu_ativo': "Gestão Organizacional",
        'title': estab.nome,
        'subtitle': org.nome, #type:ignore
        'usuarios': usuarios,
        'departamentos': departamentos
    }
    
    return render_template('/pages/organizacional/manager_estab.html', **ctx)

@bp_org.route('/manager/new/departamento', methods=['POST']) # type: ignore
def new_departamento():
    estabelecimento_id = request.form.get('estabelecimento_id', 0, int)
    nome = request.form.get('nome', '', str)
    responsavel_id = request.form.get('responsavel', 0, int)
    
    if not nome:
        flash('Erro: Nome é obrigatórios.', 'danger')
        return redirect(url_for('organization.manager_estab', id_estab=estabelecimento_id))
    
    try:
        DepartamentoService.create(estabelecimento_id=estabelecimento_id, nome=nome, id_responsavel=responsavel_id)
    except ValueError as ve:
        flash(f'Erro: {ve}', 'danger')
        return redirect(url_for('organization.manager_estab', id_estab=estabelecimento_id))
    except Exception as e:
        flash(f'Erro: Aconteceu um erro inesperado. {e}', 'danger')
        return redirect(url_for('organization.manager_estab', id_estab=estabelecimento_id))
        
    flash('Departamento criado com sucesso!', 'success')
    return redirect(url_for('organization.manager_estab', id_estab=estabelecimento_id))

@bp_org.route('/manager/departamento/<int:id_departamento>/')
def manager_departamento(id_departamento):
    usuarios = UsuarioService.list_of_users()
    departamento = DepartamentoService.get_by_id(id_departamento)
    usuarios_departamento = UsuarioService.departamento_list_of_users(id_departamento)
    form = RoleUserForm()
    # estab = EstabelecimentoService.get_by_id(id=id_departamento)
    # org = OrganizacaoService.get_by_id(estab.orgao_id) #type:ignore
    # if not estab:
    #     flash('O estabelecimento solicitado não pode ser encontrado ou não existe', 'danger')
    #     return redirect(url_for('organization.manager_new_org'))
    
    ctx = {
        # 'org': org,
        # 'estab': estab,
        'form': form,
        'departamento': departamento,
        'menu_ativo': "Gestão Organizacional",
        'title': departamento.nome, #type:ignore
        'subtitle': f'{departamento.estabelecimento.organizacao.nome} | {departamento.estabelecimento.nome}', #type:ignore
        'usuarios': usuarios,
        'usuarios_departamento': usuarios_departamento
    }
    
    return render_template('/pages/organizacional/manager_depart.html', **ctx)