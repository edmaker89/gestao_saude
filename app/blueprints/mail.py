from datetime import date
import re
from flask import Blueprint, redirect, render_template, request, url_for
from app.forms.mail_form import MailForm
from app.controllers.correspondencia_controller import CorrespondenciaController
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
            CorrespondenciaController.nova_correspondencia(
            tipo_id, assunto, usuario_id
            )
        except Exception as e:
            print('erro', e)
            return redirect(url_for('mail.new'))
        
        print('deu certo')
        return redirect(url_for('mail.new'))
        
    
    #if get
    listaTipo = TipoCorrespondencias.query.all()
    choices = []
    for l in listaTipo:
        choices.append((l.id, l.tipo))
    form.tipo.choices = choices
    
    
    return render_template('/pages/mail/new.html', title=title, subtitle=subtitle, form=form)

@bp_mail.route('/create_success/<id_mail>')
def create_success(id_mail):
    
    numero = '2/2023'
    assunto = 'Solicitação de Pagamento'
    tipo = 'Memorando'
    data = '17/12/2023'
    
    return render_template('/pages/mail/number_mail.html', numero=numero, assunto=assunto, tipo=tipo, data=data)