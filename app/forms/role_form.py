from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class RoleForm(FlaskForm):
    role = StringField('Perfil: ', validators=[DataRequired(), Length(min=3, max=30)])
    description = StringField('Descrição: ', validators=[DataRequired(), Length(min=3, max=250)])
    submit = SubmitField('Salvar')