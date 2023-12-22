from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField, EmailField

from app.models.departamento import Departamento

class EditPerfilForm(FlaskForm):
    nome_completo = StringField('Nome',  [validators.DataRequired()])
    departamento = SelectField('Departamento', [validators.DataRequired()])
    email = EmailField('e-mail')
    submit = SubmitField('Salvar Alterações')

    def __init__(self, *args, **kwargs):
        super(EditPerfilForm, self).__init__(*args, **kwargs)
    
        departamentos = Departamento.query.all()
        self.departamento.choices = [(dep.id, dep.nome) for dep in departamentos]
