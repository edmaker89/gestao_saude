from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField, EmailField

from app.models.departamento import Departamento

class EditPerfilForm(FlaskForm):
    nome_completo = StringField('Nome',  [validators.DataRequired()])
    email = EmailField('e-mail')
    submit = SubmitField('Salvar Alterações')