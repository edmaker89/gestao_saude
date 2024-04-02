from logging import PlaceHolder
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

class ProtocoloForm(FlaskForm):
    telefone = StringField('Telefone', validators=[DataRequired(), Length(min=10, max=(11))])
    whatsapp = StringField('Whatsapp', validators=[DataRequired(), Length(min=10, max=(11))])
    especialidade = SelectField('Especialidade', validators=[DataRequired()], choices=[('','')])
    tipo_atendimento = SelectField('Tipo Atendimento', validators=[DataRequired()], choices=[(0,'Exame'), (1, 'Consulta')])
    data_liberacao = DateTimeField('Data Liberação')
    estabelecimento = SelectField('Estabelecimento', validators=[DataRequired()], choices=[('','')])
    faturamento = SelectField('Faturamento', validators=[DataRequired()], choices=[('','')])
    obs = TextAreaField('Observação:')
    data_atendimento = DateTimeField('Data Atendimento')
    status = SelectField('Situação', validators=[DataRequired()], choices=[('','')])
    data_entrega = DateTimeField('Data Entrega')
    entregue_para = SelectField('Entregue para', validators=[DataRequired()], choices=[('','')])
    submit = SubmitField('Salvar')
