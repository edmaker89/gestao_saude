from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField

class FormLogin(FlaskForm):
    username = StringField('Usuario',  [validators.DataRequired() ])
    password = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=6, max=255)])
    submit = SubmitField('Entrar', )