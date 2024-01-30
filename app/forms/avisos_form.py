from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, InputRequired
from flask import current_app

class AvisosForm(FlaskForm):
    titulo = StringField('Titulo: ', validators=[DataRequired(), Length(12, 255)])
    descricao = TextAreaField('Descrição: ', validators=[DataRequired()])
    submit = SubmitField('Salvar')
