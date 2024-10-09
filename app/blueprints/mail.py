from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.forms.mail_form import MailForm
from app.controllers.correspondencia_controller import CorrespondenciaController
from app.models.tipo_correspondencias import TipoCorrespondencias
from app.utils.verify_permission import permission_required

bp_mail = Blueprint("mail", __name__, url_prefix="/mail")

@bp_mail.route("/new", methods=['GET', 'POST'])
@login_required
def new():
    form = MailForm()
    title = "Nova Correspondencia"
    subtitle = "O numero da correspondecia será mostrado após cadastrar a correspondencia"
    menu_ativo = 'Nova'
    
    #if post
    if request.method == "POST":
        tipo_id = form.tipo.data
        assunto = form.assunto.data
        usuario_id = current_user.id
        
        try:
            mail = CorrespondenciaController.nova_correspondencia(
            tipo_id, assunto, usuario_id
            )
        except Exception as e:
            flash('[ERRO]: Algo inesperado aconteceu, tente novamente', 'danger')
            return redirect(url_for('mail.new'))
        

        return redirect(url_for('mail.create_success', id_mail=mail.id))
        
    
    #if get
    listaTipo = TipoCorrespondencias.query.all()
    choices = []
    for l in listaTipo:
        choices.append((l.id, l.tipo))
    form.tipo.choices = choices
    
    
    return render_template('/pages/mail/new.html', title=title, subtitle=subtitle, form=form, menu_ativo=menu_ativo)

@bp_mail.route('/create_success/<id_mail>')
@login_required
def create_success(id_mail):
    
    mail = CorrespondenciaController.get_correspondencia_by_id(id_mail)
    
    return render_template('/pages/mail/number_mail.html', mail=mail)


@bp_mail.route('/my_mails')
@login_required
def my_mails():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    user_id = current_user.id
    data = request.args.get('data', '', type=str)
    assunto = request.args.get('assunto', '', type=str)
    numero = request.args.get('numero', '', type=str)
    ordem = request.args.get('ordem', '', type=str)
    tipo = request.args.get('tipo', '', type=int)
    menu_ativo = 'Enviados'

    listaTipo = TipoCorrespondencias.query.all()
    tipos = []
    for l in listaTipo:
        tipos.append((l.id, l.tipo))

    mails = CorrespondenciaController.get_correspondencias_by_user_with_filters(
        user_id=user_id, page=page, per_page=per_page, assunto=assunto, data=data, numero=numero, tipo=tipo, ordem=ordem)

    title = 'Enviados'
    subtitle = "Lista de todos os números de envios gerados"

    return render_template('/pages/mail/my_mails.html',
                           mails=mails,
                           title=title,
                           subtitle=subtitle,
                           data=data,
                           assunto=assunto,
                           numero=numero,
                           ordem=ordem,
                           tipo=tipo,
                           tipos=tipos,
                           menu_ativo=menu_ativo                     
                           )

@bp_mail.route('/edit_assunto', methods=['POST'])
@login_required
def edit_assunto():
    if request.method == 'POST':
        form = request.form
        assunto = form.get('assunto')
        mail_id = form.get('mail_id')

        try:
            CorrespondenciaController.mail_edit_assunto(mail_id, assunto)
        except Exception as e:
            flash('Um erro inesperado ocorreu, não foi possivel alterar o assunto', 'danger')
            return redirect(url_for('mail.my_mails'))
        return redirect(url_for('mail.my_mails'))
    return abort(404)

@bp_mail.route('/all_mails')
@login_required
@permission_required('todas correspondencias')
def all_mails():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    data = request.args.get('data', '', type=str)
    assunto = request.args.get('assunto', '', type=str)
    numero = request.args.get('numero', '', type=str)
    ordem = request.args.get('ordem', '', type=str)
    tipo = request.args.get('tipo', '', type=int)

    listaTipo = TipoCorrespondencias.query.all()
    tipos = []
    for l in listaTipo:
        tipos.append((l.id, l.tipo))

    mails = CorrespondenciaController.get_correspondencias_by_user_with_filters(
        page=page, per_page=per_page, assunto=assunto, data=data, numero=numero, tipo=tipo, ordem=ordem)

    #cabecalho
    title = 'Todas as correspondências'
    subtitle = "Lista de todos os numeros de envios gerados"

    return render_template('/pages/mail/all_mails.html',
                           mails=mails,
                           title=title,
                           subtitle=subtitle,
                           data=data,
                           assunto=assunto,
                           numero=numero,
                           ordem=ordem,
                           tipo=tipo,
                           tipos=tipos                     
                           )