from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app.controllers.depart_controller import DepartController
from app.controllers.usuario_controller import UsuarioController
from app.forms.depart_form import DepartForm

from app.models.departamento import Departamento
from app.utils.dict_layout import button_layout

bp_depart = Blueprint('depart', __name__, url_prefix='/depart' )

@bp_depart.route('/manager')
@login_required
def manager():
    title = 'Gestão de Departamentos'
    page = request.args.get('page', 1, type=int)
    departamento = request.args.get('departamento', '', type=str)
    ordem = request.args.get('ordem', 'asc', type=str)
    per_page = 20
    menu_ativo = "Gestão Organizacional"

    novo_departamento = button_layout(url='depart.new_depart', classname='button is-primary', label="Novo departamento", icon='fa-solid fa-folder-plus')

    lista_departamentos = DepartController.get_departs_by_filters(page=page, per_page=per_page, departamento=departamento, ordem=ordem)

    return render_template('/pages/depart/manager.html', menu_ativo=menu_ativo, departamento=departamento, page=page, departamentos=lista_departamentos, ordem=ordem, title=title, button_layout=novo_departamento)

@bp_depart.route('/new_depart', methods=['GET', 'POST'])
@login_required
def new_depart():
    if request.method == "POST":
        print('metodo request')
        form = DepartForm(request.form)
        departamento = form.departamento.data
        verify_depart = Departamento.query.filter(Departamento.nome == departamento).first()
        print(verify_depart)
        if verify_depart:
            print('verify_depart?')
            flash('Não é possivel criar um novo departamento, pois o mesmo ja existe', 'danger')
            return redirect(url_for('depart.new_depart'))
        print('novo_departamento', departamento)
        novo_departamento = Departamento.new_depart(departamento=departamento)
        print('return novo_departamento', novo_departamento)
        if novo_departamento:
            print('departamento criado')
            flash("Departamento criado com sucesso!", 'success')
            return redirect(url_for('depart.manager', departamento=departamento))
        flash('Houve um erro inesperado, tente novamente mais tarde!', 'danger')
        return redirect(url_for('depart.new_depart'))
    title = 'Novo Departamento'
    subtitle = 'Sempre verifique antes se o departamento não existe'
    form = DepartForm()
    
    return render_template('/pages/depart/form.html', form=form, title=title, subtitle=subtitle)

@bp_depart.route('/edit_depart/<depart_id>', methods=['GET', 'POST'])
@login_required
def edit_depart(depart_id):
    if request.method == "POST":
        print('metodo request')
        form = DepartForm(request.form)
        departamento = form.departamento.data
        verify_depart = Departamento.query.filter(Departamento.nome == departamento).first()
        print(verify_depart)
        if verify_depart:
            print('verify_depart?')
            flash('Não é possivel editar departamento, existe outro departamento com mesmo nome', 'danger')
            return redirect(url_for('depart.edit_depart', depart_id=depart_id))
        update_depart = Departamento.update(depart_id, departamento)
        if update_depart:
            flash("Departamento atualizado com sucesso!", 'success')
            return redirect(url_for('depart.manager', departamento=departamento))
        flash('Houve um erro inesperado, tente novamente mais tarde!', 'danger')
        return redirect(url_for('depart.edit_depart', depart_id=depart_id))

    title = 'Editar Departamento'
    form = DepartForm()
    departamento = Departamento.query.filter(Departamento.id == depart_id).first()
    form.departamento.data = departamento.nome #type: ignore
    
    return render_template('/pages/depart/form.html', form=form, title=title, id_depart=depart_id)


@bp_depart.route('/delete_depart/<depart_id>')
def delete_depart(depart_id):

    pessoas = UsuarioController.departamento_vazio(depart_id)
    if not pessoas:
        try:
            departamento = Departamento.get_departamento(depart_id)
            departamento.delete()
            flash('Departamento Excluido com sucesso!', 'success')
        except:
            flash('Não foi possivel excluir o departamento, tente novamente mais tarde!', 'danger')
        finally:
            return redirect(url_for('depart.manager'))
        
    flash('Existem colaboradores vinculados ao departamento! Só é possivel apagar um departamento vazio', 'info')   
    return redirect(url_for('depart.manager'))