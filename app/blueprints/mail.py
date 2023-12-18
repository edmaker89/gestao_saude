from datetime import date
import re
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from app.forms.mail_form import MailForm
from app.controllers.correspondencia_controller import CorrespondenciaController
from app.models import correspondencias
from app.models.tipo_correspondencias import TipoCorrespondencias

bp_mail = Blueprint("mail", __name__, url_prefix="/mail")

@bp_mail.route("/new", methods=['GET', 'POST'])
def new():
    form = MailForm()
    title = "Nova Correspondencia"
    subtitle = "O numero da correspondecia será mostrado após cadastrar a correspondencia"
    
    #if post
    if request.method == "POST":
        tipo_id = form.tipo.data
        assunto = form.assunto.data
        usuario_id = 1
        
        try:
            mail = CorrespondenciaController.nova_correspondencia(
            tipo_id, assunto, usuario_id
            )
        except Exception as e:
            # flash('[ERRO]: Algo inesperado aconteceu, tente novamente', 'danger')
            return redirect(url_for('mail.new'))
        

        return redirect(url_for('mail.create_success', id_mail=mail.id))
        
    
    #if get
    listaTipo = TipoCorrespondencias.query.all()
    choices = []
    for l in listaTipo:
        choices.append((l.id, l.tipo))
    form.tipo.choices = choices
    
    
    return render_template('/pages/mail/new.html', title=title, subtitle=subtitle, form=form)

@bp_mail.route('/create_success/<id_mail>')
def create_success(id_mail):
    
    mail = CorrespondenciaController.get_correspondencia_by_id(id_mail)
    
    return render_template('/pages/mail/number_mail.html', mail=mail)

@bp_mail.route('/my_mails')
def my_mails():
    page = request.args.get('page', 1, type=int)
    user_id = 1
    # minhas correspondencias
    mails = CorrespondenciaController.get_last_correspondencias_by_user(user_id, page=page)

    #cabecalho
    title = 'Minhas Correspondências'
    subtitle = "Lista de todos os numeros de envios gerados"

    return render_template('/pages/mail/my_mails.html',
                           mails=mails,
                           title=title,
                           subtitle=subtitle                           
                           )

@bp_mail.route('/edit_assunto', methods=['POST'])
def edit_assunto():

    if request.method == 'POST':
        form = request.form
        assunto = form.get('assunto')
        mail_id = form.get('mail_id')

        try:
            CorrespondenciaController.mail_edit_assunto(mail_id, assunto)
        except Exception as e:
            print('deu erro')
            return redirect(url_for('mail.my_mails'))

        print('deu certo') 
        return redirect(url_for('mail.my_mails'))

    
    return abort(404)