from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired

class MailForm(FlaskForm):
    assunto = StringField('Assunto: ', validators=[DataRequired(), Length(12, 255)])
    tipo = RadioField('Tipo de correspondência', validators=[InputRequired(message=None)], choices=[])
    visibilidade = SelectField('Visibilidade:', choices=[('publica', 'Pública'), ('privada', 'Privada'), ('sigilosa', 'Sigilosa')])
    submit = SubmitField('Gerar número')
