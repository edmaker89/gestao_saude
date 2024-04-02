from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

class CidadaoForm(FlaskForm):
    nome = StringField('Nome: ', validators=[DataRequired(), Length(min=3)])
    cns = StringField('CNS: ', validators=[Length(min=15, max=15)])
    cpf = StringField('CPF: ', validators=[Length(min=11, max=11)])
    rg = StringField('RG :', validators=[Length(min=4)])
    orgao_expedidor = StringField('Orgão expedidor', validators=[Length(max=50)])
    data_de_nascimento = DateField('Data de nascimento', validators=[DataRequired()])
    sexo = SelectField('Sexo: ', validators=[DataRequired()], choices=[('','Selecione'), ('F','feminino'), ('M', 'masculino')])
    cep = StringField('CEP: ', validators=[DataRequired(), Length(min=8, max=9)])
    logradouro = StringField('Logradouro: ', validators=[Length(max=255)])
    numero = StringField('Número: ')
    complemento = StringField('Complemento: ')
    bairro = StringField('Bairro: ')
    cidade = StringField('Cidade: ')
    uf = StringField('UF: ')
    ocupacao = StringField('Ocupacao: ')
    responsavel = StringField('Responsavel: ')
    
    submit = SubmitField('Salvar')
