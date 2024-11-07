from flask import Blueprint, abort, ctx, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.forms.mail_form import MailForm
from app.models import estabelecimento, organizacao
from app.models.users import Usuario
from app.services.correspondencia_service import CorrespondenciaService
from app.models.tipo_correspondencias import TipoCorrespondencias
from app.services.departamento_service import DepartamentoService
from app.services.estabelecimento_service import EstabelecimentoService
from app.services.organizacao_service import OrganizacaoService
from app.services.usuario_service import UsuarioService
from app.utils.breadcrumbItem import BreadcrumbItem, BreadcrumbManager
from app.utils.verify_permission import permission_required, verify_permission

bp_mail = Blueprint("mail", __name__, url_prefix="/mail")

@bp_mail.route("/new", methods=['GET', 'POST'])
@login_required
def new():
    form = MailForm()
    title = "Nova Correspondência"
    subtitle = "O numero da correspondecia será mostrado após cadastrar a correspondencia"
    menu_ativo = 'Nova'
    
    #if post
    if request.method == "POST":
        tipo_id = form.tipo.data
        assunto = form.assunto.data
        usuario_atual: Usuario = current_user #type:ignore
        visibilidade = form.visibilidade.data
        
        print(tipo_id, assunto, usuario_atual.id, usuario_atual.departamento_id, usuario_atual.departamento.estabelecimento.organizacao.id, visibilidade)
        
        try:
            # departamento_id, org_id, visibilidade = None
            mail = CorrespondenciaService.nova_correspondencia(
            tipo_id=tipo_id, 
            assunto=assunto, 
            usuario_id=usuario_atual.id, 
            departamento_id=usuario_atual.departamento_id, 
            org_id=usuario_atual.departamento.estabelecimento.organizacao.id,
            visibilidade=visibilidade
            )
        except Exception as e:
            print(e)
            flash('[ERRO]: Algo inesperado aconteceu, tente novamente', 'danger')
            return redirect(url_for('mail.new'))
        

        return redirect(url_for('mail.create_success', id_mail=mail.id))
        
    
    #if get
    listaTipo = TipoCorrespondencias.query.all()
    choices = []
    for l in listaTipo:
        choices.append((l.id, l.tipo))
    form.tipo.choices = choices
    rotas = [('Início', {}), (title, {})]
    bread_manager=BreadcrumbManager()
    breads = bread_manager.gerar_breads(rotas)
    ctx_breads = {'breads': breads, 'bread_ativo':title}
    
    return render_template('/pages/mail/new.html', title=title, subtitle=subtitle, form=form, menu_ativo=menu_ativo, **ctx_breads)

@bp_mail.route('/create_success/<id_mail>')
@login_required
def create_success(id_mail):
    
    mail = CorrespondenciaService.get_correspondencia_by_id(id_mail)
    
    return render_template('/pages/mail/number_mail.html', mail=mail)


@bp_mail.route('/my_mails')
@login_required
def my_mails():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    user_id = request.args.get('user', None, type=int)
    departamento_id = request.args.get('departamento', None, type=int)
    estabelecimento_id = request.args.get('estabelecimento', None, type=int)
    user_id = request.args.get('colaborador', None, type=int)
    data_inicial = request.args.get('data_inicial', '', type=str)
    data_final = request.args.get('data_final', '', type=str)
    assunto = request.args.get('assunto', '', type=str)
    numero = request.args.get('numero', '', type=str)
    ordem = request.args.get('ordem', '', type=str)
    tipo = request.args.get('tipo', '', type=int)
    menu_ativo = 'Enviados'

    listaTipo = TipoCorrespondencias.query.all()
    tipos = []
    for l in listaTipo:
        tipos.append((l.id, l.tipo))

    title = 'Enviados'
    subtitle = "Lista de todos os números de envios gerados"
    rotas = [('Início', {}), ('Enviados', {})]
    bread_manager=BreadcrumbManager()
    breads = bread_manager.gerar_breads(rotas)
    ctx_breads = {'breads': breads, 'bread_ativo':title}
    
    estabelecimentos = []
    departamentos = []
    colaboradores = []
    organizacao_id = current_user.departamento.estabelecimento.organizacao.id
    
    params = {
        'data_inicial':data_inicial,
        'data_final':data_final,
        'user':user_id,
        'id_departamento':departamento_id,
        'id_estabelecimento':estabelecimento_id,
        'id_organizacao':organizacao_id,
        'id_colaborador':user_id,
        'assunto':assunto,
        'numero':numero,
        'ordem':ordem,
        'tipo':tipo,
        }
    
    e_responsavel = None
     
    if OrganizacaoService.e_responsavel(current_user.id, organizacao_id):
        e_responsavel = 'organizacao'
        lista_estabelecimentos = EstabelecimentoService.list_all(orgao_id=organizacao_id)
        for estab in lista_estabelecimentos:
            estabelecimentos.append((estab.id, estab.nome))
    elif EstabelecimentoService.e_responsavel(current_user.id, current_user.departamento.estabelecimento.id):
        e_responsavel = 'estabelecimento'
        lista_departamentos = DepartamentoService.list_all_by_estab(current_user.departamento.estabelecimento.id)
        for departamento in lista_departamentos:
            departamentos.append((departamento.id, departamento.nome))
    elif DepartamentoService.e_responsavel(current_user.id, current_user.departamento_id):
        e_responsavel = 'departamento'
        lista_colaboradores = UsuarioService.usuarios_por_departamento(current_user.departamento_id)
        for colaborador in lista_colaboradores:
            colaboradores.append((colaborador.id, colaborador.nome_completo))
        #implementar visualizar todas as correspondencias
    else:
        e_responsavel = None
    
    mails = CorrespondenciaService.get_correspondencias_by_user_with_filters(
       user_id=user_id, page=page, per_page=per_page, assunto=assunto, data_inicial=data_inicial, data_final=data_final, numero=numero, 
       tipo=tipo, ordem=ordem, departamento_id=departamento_id, estabelecimento_id=estabelecimento_id, organizacao_id=organizacao_id)
    

    return render_template('/pages/mail/my_mails.html',
                           e_responsavel=e_responsavel,
                           mails=mails,
                           title=title,
                           subtitle=subtitle,
                           tipos=tipos,
                           menu_ativo=menu_ativo,
                           estabelecimentos= estabelecimentos,
                           departamentos=departamentos,
                           colaboradores=colaboradores,
                           **params,
                           **ctx_breads,                    
                           )

@bp_mail.route('/edit_assunto', methods=['POST'])
@login_required
def edit_assunto():
    if request.method == 'POST':
        form = request.form
        assunto = form.get('assunto')
        visibilidade = form.get('visibilidade')
        mail_id = form.get('mail_id')

        try:
            CorrespondenciaService.mail_edit_assunto(mail_id, assunto, visibilidade)
        except Exception as e:
            print(e)
            flash('Um erro inesperado ocorreu, não foi possivel alterar o assunto', 'danger')
            return redirect(url_for('mail.my_mails'))
        return redirect(url_for('mail.my_mails'))
    return abort(404)

# @bp_mail.route('/all_mails')
# @login_required
# @permission_required('todas correspondencias')
# def all_mails():
#     page = request.args.get('page', 1, type=int)
#     per_page = 20
#     data = request.args.get('data', '', type=str)
#     assunto = request.args.get('assunto', '', type=str)
#     numero = request.args.get('numero', '', type=str)
#     ordem = request.args.get('ordem', '', type=str)
#     tipo = request.args.get('tipo', '', type=int)

#     listaTipo = TipoCorrespondencias.query.all()
#     tipos = []
#     for l in listaTipo:
#         tipos.append((l.id, l.tipo))

#     mails = CorrespondenciaService.get_correspondencias_by_user_with_filters(
#         page=page, per_page=per_page, assunto=assunto, data=data, numero=numero, tipo=tipo, ordem=ordem)

#     #cabecalho
#     title = 'Todas as correspondências'
#     subtitle = "Lista de todos os numeros de envios gerados"
    

#     return render_template('/pages/mail/all_mails.html',
#                            mails=mails,
#                            title=title,
#                            subtitle=subtitle,
#                            data=data,
#                            assunto=assunto,
#                            numero=numero,
#                            ordem=ordem,
#                            tipo=tipo,
#                            tipos=tipos                     
#                            )