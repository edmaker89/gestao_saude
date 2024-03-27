from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app.controllers.depart_controller import DepartController
from app.controllers.usuario_controller import UsuarioController
from app.forms.depart_form import DepartForm

from app.models.departamento import Departamento
from app.utils.dict_layout import button_layout

bp_regulacao = Blueprint('regulacao', __name__, url_prefix='/regulacao' )

list_protocolo = [
    {
        'id_protocolo': 1,
        'numero': 202401191,
        'data_entrada': '2024-01-19 17:00:00',
        'usuario_entrada': 'Kimberlee G. Lavin',
        'usuario_ultima_atualizacao': 'Alex Cavalcanti Martins',
        'usuario_entrega': 'Alex Cavalcanti Martins',
        'usuario_liberacao': 'Enzo Carvalho Martins',
        'cidadao': 'Silvia Aparecida de Oliveira',
        'telefone': '62 985453325',
        'whatsapp': '62 985453325',
        'especilialidade': 'oftalmologista',
        'tipo_atendimento': 'consulta',
        'data_liberacao': '2024-03-26',
        'estabelecimento': 'Fundação Banco de Olhos',
        'observacao': 'consulta para cirurgia dos olhos',
        'status': 'liberado',
        'data_entrega': '2024-03-27 08:33:15',
        'entregue_para': 'Marcia Aparecida da Silva',
        'data_hora_atendimento': '2024-04-05 09:00:00'
    },
     {
        'id_protocolo': 2,
        'numero': 202403271,
        'data_entrada': '2024-03-27 10:45:00',
        'usuario_entrada': 'Kimberlee G. Lavin',
        'usuario_ultima_atualizacao': 'Marcia Aparecida da Silva',
        'usuario_entrega': None,
        'usuario_liberacao': None,
        'cidadao': 'João da Silva',
        'telefone': '11 987654321',
        'whatsapp': '11 987654321',
        'especilialidade': 'clínico geral',
        'tipo_atendimento': 'consulta',
        'data_liberacao': None,
        'estabelecimento': 'Hospital São Lucas',
        'observacao': 'Consulta de rotina',
        'status': 'pendente',
        'data_entrega': None,
        'entregue_para': None,
        'data_hora_atendimento': '2024-04-10 14:30:00'
    },
    {
        'id_protocolo': 3,
        'numero': 202403272,
        'data_entrada': '2024-03-27 11:30:00',
        'usuario_entrada': 'Alex Cavalcanti Martins',
        'usuario_ultima_atualizacao': 'Marcia Aparecida da Silva',
        'usuario_entrega': 'Joana Lima',
        'usuario_liberacao': None,
        'cidadao': 'Maria Oliveira',
        'telefone': '21 9988776655',
        'whatsapp': '21 9988776655',
        'especilialidade': 'pediatra',
        'tipo_atendimento': 'consulta',
        'data_liberacao': None,
        'estabelecimento': 'Clínica Infantil Feliz',
        'observacao': 'Avaliação do desenvolvimento infantil',
        'status': 'entregue',
        'data_entrega': '2024-03-27 15:20:00',
        'entregue_para': 'Joana Lima',
        'data_hora_atendimento': '2024-04-03 10:00:00'
    },
    {
        'id_protocolo': 4,
        'numero': 202403273,
        'data_entrada': '2024-03-27 12:15:00',
        'usuario_entrada': 'Enzo Carvalho Martins',
        'usuario_ultima_atualizacao': 'Marcia Aparecida da Silva',
        'usuario_entrega': 'Pedro Henrique Oliveira',
        'usuario_liberacao': 'Enzo Carvalho Martins',
        'cidadao': 'Ana Paula Santos',
        'telefone': '31 987654321',
        'whatsapp': '31 987654321',
        'especilialidade': 'dermatologista',
        'tipo_atendimento': 'consulta',
        'data_liberacao': '2024-03-27',
        'estabelecimento': 'Clínica de Dermatologia Skin',
        'observacao': 'Avaliação de manchas na pele',
        'status': 'liberado',
        'data_entrega': '2024-03-27 17:45:00',
        'entregue_para': 'Pedro Henrique Oliveira',
        'data_hora_atendimento': '2024-04-02 16:00:00'
    },
    {
        'id_protocolo': 5,
        'numero': 202403274,
        'data_entrada': '2024-03-27 13:00:00',
        'usuario_entrada': 'Kimberlee G. Lavin',
        'usuario_ultima_atualizacao': 'Marcia Aparecida da Silva',
        'usuario_entrega': None,
        'usuario_liberacao': 'Enzo Carvalho Martins',
        'cidadao': 'Carlos Eduardo',
        'telefone': '48 987654321',
        'whatsapp': '48 987654321',
        'especilialidade': 'ortopedista',
        'tipo_atendimento': 'consulta',
        'data_liberacao': '2024-03-27',
        'estabelecimento': 'Clínica Ortopédica Bem Estar',
        'observacao': 'Avaliação de lesão no joelho',
        'status': 'liberado',
        'data_entrega': None,
        'entregue_para': None,
        'data_hora_atendimento': '2024-04-05 11:00:00'
    },
    {
        'id_protocolo': 6,
        'numero': 202403275,
        'data_entrada': '2024-03-27 13:45:00',
        'usuario_entrada': 'Enzo Carvalho Martins',
        'usuario_ultima_atualizacao': 'Marcia Aparecida da Silva',
        'usuario_entrega': 'Ana Luiza Oliveira',
        'usuario_liberacao': None,
        'cidadao': 'Ricardo Ferreira',
        'telefone': '85 987654321',
        'whatsapp': '85 987654321',
        'especilialidade': 'cardiologista',
        'tipo_atendimento': 'consulta',
        'data_liberacao': None,
        'estabelecimento': 'Hospital do Coração',
        'observacao': 'Consulta de acompanhamento',
        'status': 'pendente',
        'data_entrega': '2024-03-27 16:30:00',
        'entregue_para': 'Ana Luiza Oliveira',
        'data_hora_atendimento': '2024-04-08 09:30:00'
    }
]

@bp_regulacao.route('/protocolo')
@login_required
def protocolo():
    title = 'Regulação - Protocolo'
    page = request.args.get('page', 1, type=int)
    departamento = request.args.get('departamento', '', type=str)
    ordem = request.args.get('ordem', 'asc', type=str)
    per_page = 20

    novo_departamento = button_layout(url='depart.new_depart', classname='button is-primary', label="Novo protocolo", icon='fa-solid fa-file-circle-plus')

    lista_departamentos = DepartController.get_departs_by_filters(page=page, per_page=per_page, departamento=departamento, ordem=ordem)

    return render_template('/pages/regulacao/protocolo.html', departamento=departamento, page=page, protocolos=list_protocolo, ordem=ordem, title=title, button_layout=novo_departamento)

