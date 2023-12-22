from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, SubmitField, SelectField, EmailField

from app.models.departamento import Departamento

class NewUserForm(FlaskForm):
    username = StringField('Usuário', [validators.DataRequired(), validators.length(3, 20)])
    nome_completo = StringField('Nome',  [validators.DataRequired()])
    departamento = SelectField('Departamento', [validators.DataRequired()])
    email = EmailField('e-mail')
    senha= PasswordField('Senha')
    confirmar_senha = PasswordField('Confirmar senha')
    submit = SubmitField('Salvar Alterações')

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
    
        departamentos = Departamento.query.all()
        self.departamento.choices = [(dep.id, dep.nome) for dep in departamentos]
