import json
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for, flash
from flask_login import login_required
from app.forms.cidadao_form import CidadaoForm

from app.forms.protocolo_form import ProtocoloForm
from app.models.cidadaos import Cidadaos, TelefoneCidadao
from app.utils.dict_layout import button_layout

bp_regulacao = Blueprint('regulacao', __name__, url_prefix='/regulacao' )

cidadaos = [
    {
        'nome': 'Sebastiana Camilo Neris',
        'telefone': 'XX XXXXXXXXX',  # Preencha com o número de telefone da pessoa
        'cpf': 'XXX.XXX.XXX-XX',  # Preencha com o CPF da pessoa
        'endereco': 'Endereço completo',  # Preencha com o endereço da pessoa
        'email': 'email@example.com'  # Preencha com o email da pessoa
    },
    {
        'nome': 'Marcos Paulo de Souza',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Benedito Rodrigues Chaveiro Neto',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Daniela Dias de Oliveira',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Marco Antonio Morais Guimarães',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Lúcia Maria da Silva Costa',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Polyane Guimarães da Mota',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Noah Borges Dias',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Nair Maria de Jesus Silva',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Herculano Pereira da Silva',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Sandra Alves de Oliveira',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Maria do Rosário Emídio de Oliveira',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Patrícia Cristina Pistore',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Cleusa Francisco Camargo Graciano',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Solange Ribeiro da Silva',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'José Modesto de Souza',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Oranizio José de Sousa',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Lyandra Vitória Gonçalves de Sousa',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Estácio José de Lima Neto',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Lucas Luiz da Silva Oliveira',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Elismar Miguel Almeida Faria Barbosa',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Ivaneide Ferreira da Cruz',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Gemima Amaral Cândido',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'Marceni Paiva Moreira',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    },
    {
        'nome': 'José de Fátima de Souza',
        'telefone': 'XX XXXXXXXXX',
        'cpf': 'XXX.XXX.XXX-XX',
        'endereco': 'Endereço completo',
        'email': 'email@example.com'
    }
]

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

@bp_regulacao.route('/cidadao/novo/', methods=['GET', 'POST'])
@login_required
def cidadao_novo():
    if request.method == 'POST':
        form = CidadaoForm(request.form)
        novo_cidadao = Cidadaos()
        novo_cidadao.nome = form.nome.data
        novo_cidadao.mae = form.mae.data
        novo_cidadao.cns = form.cns.data
        novo_cidadao.cpf = form.cpf.data
        novo_cidadao.rg = form.rg.data
        novo_cidadao.orgao_expedidor = form.orgao_expedidor.data
        novo_cidadao.data_de_nascimento = form.data_de_nascimento.data
        novo_cidadao.sexo = form.sexo.data
        novo_cidadao.cep = form.cep.data
        novo_cidadao.cidade = form.cidade.data
        novo_cidadao.uf = form.uf.data
        novo_cidadao.logradouro = form.logradouro.data
        novo_cidadao.numero = form.numero.data
        novo_cidadao.complemento = form.complemento.data
        novo_cidadao.bairro = form.bairro.data
        
        try:
            cadastrado = novo_cidadao.save()
            if cadastrado:
                msg = 'Cadastrado com sucesso!'
                flash(msg, 'success')
                
            # cadastrar telefone
            telefones_json = request.form.get('telefones')
            print('telefones_json', telefones_json)
            if telefones_json:
                telefones = json.loads(telefones_json)

                for telefone in telefones:
                    print(telefone)
                    print(telefone['ddd'])
                    novo_telefone = TelefoneCidadao()
                    novo_telefone.ddd = telefone['ddd']
                    novo_telefone.numero = telefone['numero']
                    novo_telefone.tipo = telefone['whatsapp']
                    novo_telefone.cidadao_id = novo_cidadao.id
                    
                    novo_telefone.save()
            else:
                msg = f'O cpf {novo_cidadao.cpf} já existe na base de dados!'
                flash(msg, 'danger')
        except Exception as e:
            print(e)
            flash('Houve um erro inesperado. Tente novamente mais tarde!', 'danger')
        
        
        
        
        return redirect(url_for('regulacao.cidadao_novo'))
    
    title = "Cadastrar novo cidadão"
    form = CidadaoForm()
    
    return render_template('pages/regulacao/cidadao/form.html',
                           form = form,
                           title=title)


@bp_regulacao.route('/buscar_cidadao')
def buscar_cidadao():
    termo_busca = request.args.get('query')  # Obtém o termo de busca do parâmetro cidadao
    # Chame sua função que consome a API com o termo de busca
    resultados = cidadaos
    # Renderiza os resultados como uma lista de <li>
    lista_resultados = jsonify([resultado for resultado in resultados])

    return lista_resultados


@bp_regulacao.route('/protocolo')
@login_required
def protocolo():
    title = 'Regulação - Protocolo'
    page = request.args.get('page', 1, type=int)
    departamento = request.args.get('departamento', '', type=str)
    ordem = request.args.get('ordem', 'asc', type=str)
    data_entrada = request.args.get('data-entrada', 'asc', type=str)
    data_liberacao = request.args.get('data-liberacao', 'asc', type=str)
    data_entrega = request.args.get('data-entrega', 'asc', type=str)
    especialidade = request.args.get('especialidade', 'asc', type=str)
    status = request.args.get('status', 'asc', type=str)
    per_page = 20

    novo_protocolo = button_layout(url='regulacao.selecionar_cidadao', classname='button is-primary', label="Novo protocolo", icon='fa-solid fa-file-circle-plus')

    return render_template('/pages/regulacao/protocolo.html', 
                           departamento=departamento, 
                           page=page, 
                           protocolos=list_protocolo, 
                           ordem=ordem, 
                           title=title, 
                           button_layout=novo_protocolo)
    
@bp_regulacao.route('/protocolo/selecionar_cidadao')
@login_required
def selecionar_cidadao():
    
    return render_template('pages/regulacao/selecionar_cidadao.html')

@bp_regulacao.route('/protocolo/form', methods=['GET', 'POST'])
@login_required
def form_protocolo():
    
    form = ProtocoloForm()
    return render_template('pages/regulacao/form_protocolo.html', 
                           id_protocolo=None, 
                           form=form,
                           citizens=cidadaos
                           )