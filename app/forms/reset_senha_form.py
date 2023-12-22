from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, InputRequired

class ResetSenhaForm(FlaskForm):
    senha_atual = PasswordField('Senha atual: ', validators=[DataRequired(), Length(6, 255)])
    nova_senha = PasswordField('Nova senha: ', validators=[DataRequired(), Length(6, 255)])
    confirmar_senha = PasswordField('Confirmar Senha: ', validators=[DataRequired(), Length(6, 255)])
    submit = SubmitField('Alterar senha')
