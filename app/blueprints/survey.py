from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app.controllers.depart_controller import DepartController
from app.controllers.usuario_controller import UsuarioController
from app.forms.depart_form import DepartForm

from app.models.departamento import Departamento
from app.utils.dict_layout import button_layout

bp_survey = Blueprint('survey', __name__, url_prefix='/survey' )

@bp_survey.route('/')
@login_required
def index():
    title = 'Criar nova pesquisa'
    context = {
        "title":title
    }
    return render_template('/pages/survey/index.html', **context)