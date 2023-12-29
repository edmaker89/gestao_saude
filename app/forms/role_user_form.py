from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, validators

from app.models.role_permissions import Role

class RoleUserForm(FlaskForm):
    
    role = SelectField('Selecionar Perfil', [validators.DataRequired()], choices=[])
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(RoleUserForm, self).__init__(*args, **kwargs)
    
        roles = Role.query.all()
        choices = []
        choices.extend([(role.id, role.nome) for role in roles])
        self.role.choices = choices