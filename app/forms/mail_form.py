from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, InputRequired
from flask import current_app

class MailForm(FlaskForm):
    assunto = StringField('Assunto: ', validators=[DataRequired(), Length(12, 255)])
    tipo = RadioField('Tipo de correspondência', validators=[InputRequired(message=None)], choices=[])
    submit = SubmitField('Gerar número')
