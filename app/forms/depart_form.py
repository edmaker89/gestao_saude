from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class DepartForm(FlaskForm):
    departamento = StringField('Departamento: ', validators=[DataRequired(), Length(min=3, max=30)])
    submit = SubmitField('Salvar')
