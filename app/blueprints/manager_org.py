from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app.services.depart_service import DepartmentService
from app.services.organizacao_service import OrganizacaoService
from app.services.usuario_service import UsuarioService
from app.forms.depart_form import DepartForm

from app.models.departamento import Departamento
from app.models.organizacao import Organizacao
from app.utils.dict_layout import button_layout

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