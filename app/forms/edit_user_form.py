from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, SubmitField, SelectField, EmailField

from app.models.departamento import Departamento

class EditUserForm(FlaskForm):
    username = StringField('Usuário', [validators.DataRequired(), validators.length(3, 20)])
    nome_completo = StringField('Nome',  [validators.DataRequired()])
    departamento = SelectField('Departamento', [validators.DataRequired()])
    email = EmailField('e-mail')
    submit = SubmitField('Salvar Alterações')

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
    
        departamentos = Departamento.query.all()
        choices = [('', 'Selecione um departamento')]
        choices.extend([(dep.id, dep.nome) for dep in departamentos])
        self.departamento.choices = choices