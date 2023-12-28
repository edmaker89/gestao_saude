from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class PermissionForm(FlaskForm):
    nome = StringField('Permissão: ', validators=[DataRequired(), Length(min=3, max=30)])
    descricao = StringField('Descrição: ', validators=[DataRequired(), Length(min=3, max=250)])
    submit = SubmitField('Salvar')