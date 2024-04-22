import json
from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for, flash
from flask_login import login_required
from sqlalchemy import or_
from app.forms.cidadao_form import CidadaoForm
from app.forms.protocolo_form import ProtocoloForm
from app.models.cidadaos import Cidadaos, TelefoneCidadao
from app.utils.dict_layout import button_layout
from app.ext.database import db

bp_regulacao = Blueprint('regulacao', __name__, url_prefix='/regulacao' )

def search_citizens_with_params(cidadao=None, mae=None, data_de_nascimento=None, ordem='asc', per_page=20, page=1):
    query = db.session.query(
            Cidadaos
        )
    print(cidadao)
    if cidadao:
        query = query.filter(or_(
        Cidadaos.nome.like(f"%{cidadao}%"),
        Cidadaos.cpf == cidadao,
        Cidadaos.cns == cidadao
    ))

    if mae:
        query = query.filter(Cidadaos.mae.like(f"%{mae}%"))
    if data_de_nascimento:
        query = query.filter(Cidadaos.data_de_nascimento == data_de_nascimento)

    # Adicione a ordenação pela data ou outro campo apropriado
    if ordem == 'asc':
        query = query.order_by(Cidadaos.nome.asc())
    else:
        query = query.order_by(Cidadaos.nome.desc())

    cidadaos = query.paginate(page=page, per_page=per_page) # type: ignore

    return cidadaos

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
            novo_cidadao.save()
                
            # cadastrar telefone
            telefones_json = request.form.get('telefones')
            print('telefones_json', telefones_json)
            if telefones_json:
                telefones = json.loads(telefones_json)

                TelefoneCidadao.update_new_tels(novo_cidadao.id, telefones)
                flash('Cidadão cadastrado com sucesso, favor confirme os dados digitados!', 'success')
                return redirect(url_for('regulacao.cidadao'))
            else:
                msg = f'O cpf {novo_cidadao.cpf} já existe na base de dados!'
                flash(msg, 'danger')
                return redirect(url_for('regulacao.cidadao'))
        except Exception as e:
            print(e)
            flash('Houve um erro inesperado. Tente novamente mais tarde!', 'danger')
        return redirect(url_for('regulacao.cidadao_novo'))
    
    title = "Cadastrar novo cidadão"
    form = CidadaoForm()
    return render_template('pages/regulacao/cidadao/form.html',
                           form = form,
                           title=title)
    
@bp_regulacao.route('/cidadao/atualizar/<id_cidadao>/', methods=['GET', 'POST'])
@login_required
def cidadao_update(id_cidadao):
    if request.method == 'POST':
        form = CidadaoForm(request.form)
        # update_cidadao = Cidadaos.query.filter(Cidadaos.id == id_cidadao).first()
        update_cidadao = Cidadaos.query.get(id_cidadao)
        
        update_cidadao.nome = form.nome.data # type: ignore
        update_cidadao.mae = form.mae.data # type: ignore
        update_cidadao.cns = form.cns.data # type: ignore
        update_cidadao.cpf = form.cpf.data # type: ignore
        update_cidadao.rg = form.rg.data # type: ignore
        update_cidadao.orgao_expedidor = form.orgao_expedidor.data # type: ignore
        update_cidadao.data_de_nascimento = form.data_de_nascimento.data # type: ignore
        update_cidadao.sexo = form.sexo.data # type: ignore
        update_cidadao.cep = form.cep.data # type: ignore
        update_cidadao.cidade = form.cidade.data # type: ignore
        update_cidadao.uf = form.uf.data # type: ignore
        update_cidadao.logradouro = form.logradouro.data # type: ignore
        update_cidadao.numero = form.numero.data # type: ignore
        update_cidadao.complemento = form.complemento.data # type: ignore
        update_cidadao.bairro = form.bairro.data # type: ignore
        
        try:
            update_cidadao.save() # type: ignore
            telefones_json = request.form.get('telefones')
            
            if telefones_json:
                telefones = json.loads(telefones_json)
                TelefoneCidadao.update_new_tels(id_cidadao, telefones)
                
            flash('Cidadão atualizado com sucesso!', 'success')
            return redirect(url_for('regulacao.cidadao'))

        except Exception as e:
            print(e)
            flash(f'Houve um erro inesperado. Tente novamente mais tarde! {e}', 'danger')
            return redirect(url_for('regulacao.cidadao_update', id_cidadao=id_cidadao))
    
    citizen: Cidadaos = Cidadaos.query.get(id_cidadao) # type: ignore
    edit = True
    title = "Atualizar cidadão"
    form = CidadaoForm()
    form.nome.data = citizen.nome
    form.mae.data = citizen.mae
    form.cns.data = citizen.cns
    form.cpf.data = citizen.cpf
    form.rg.data = citizen.rg
    form.orgao_expedidor.data = citizen.orgao_expedidor
    form.data_de_nascimento.data = citizen.data_de_nascimento
    form.sexo.data = citizen.sexo
    form.cep.data = citizen.cep
    form.cidade.data = citizen.cidade
    form.uf.data = citizen.uf
    form.logradouro.data = citizen.logradouro
    form.numero.data = citizen.numero
    form.complemento.data = citizen.complemento
    form.bairro.data = citizen.bairro
    
    telefones = TelefoneCidadao.get_telefones_by_cidadao_id(id_cidadao)
    print(telefones)
    
    
    return render_template('pages/regulacao/cidadao/form.html',
                           form = form,
                           title=title,
                           edit=edit,
                           telefones=telefones,
                           id_cidadao=id_cidadao
                           )

@bp_regulacao.route('/cidadao/')
def cidadao():
    page = request.args.get('page', 1, type=int)
    cidadao = request.args.get('cidadao', '', type=str)
    print(cidadao)
    ordem = request.args.get('ordem', 'asc', type=str)
    mae = request.args.get('mae', '', type=str)
    per_page = 20
    data_de_nascimento = request.args.get('dataNascimento', '', type=str)
    title = 'Cidadão'
    subtitle = 'Procure por cidadãos cadastrados ou realize um novo cadastros'
    
    if cidadao != '' or mae != '' or data_de_nascimento != '':
        cidadaos = search_citizens_with_params(cidadao, mae, data_de_nascimento, ordem, per_page, page)
    else:
        cidadaos = []
    
    btn_novo_cidadao = button_layout('regulacao.cidadao_novo', 'button is-info', 'Novo Cidadao', 'fa-solid fa-user-plus')
    
    form = request.form
    return render_template('pages/regulacao/cidadao/cidadao.html', 
                           form=form,
                           title=title,
                           subtitle=subtitle,
                           button_layout=btn_novo_cidadao,
                           page=page,
                           cidadao=cidadao,
                           ordem=ordem,
                           mae=mae,
                           data_de_nascimento=data_de_nascimento,
                           cidadaos=cidadaos
                           )


@bp_regulacao.route('/protocolo')
@login_required
def protocolo():
    title = 'Regulação - Protocolo'
    page = request.args.get('page', 1, type=int)
    ordem = request.args.get('ordem', 'asc', type=str)
    nome = request.args.get('nome', '', type=str)
    
    data_entrada = request.args.get('data_entrada', '', type=str)
    data_liberacao = request.args.get('data_liberacao', '', type=str)
    data_entrega = request.args.get('data_entrega', '', type=str)
    especialidade = request.args.get('especialidade', '', type=str)
    protocolo = request.args.get('protocolo', '', type=str)
    status = request.args.get('status', '', type=str)
    per_page = 20
    
    especialidades = [(1, 'Oftalmologista'), (2, 'Clinico Geral'), (3, 'Pediatria')]
    situacao = [(1, 'liberado'), (2, 'pendente'), (3, 'entregue'), (4, 'cancelado'), (5, 'negado')]
    print(nome)
    
    params = {
        'page': page,
        'ordem':ordem, 
        'nome':nome, 
        'data_entrada': data_entrada,
        'data_liberacao': data_liberacao,
        'data_entrega': data_entrega,
        'especialidade': especialidade,
        'protocolo': protocolo,
        'status': status,
        }

    novo_protocolo = button_layout(url='regulacao.selecionar_cidadao', classname='button is-primary', label="Novo protocolo", icon='fa-solid fa-file-circle-plus')

    return render_template('/pages/regulacao/protocolo.html', 
                           protocolos=list_protocolo, 
                           title=title, 
                           button_layout=novo_protocolo,
                           especialidades=especialidades,
                           situacao=situacao,
                           params = params
                           )
    
@bp_regulacao.route('/protocolo/selecionar_cidadao')
@login_required
def selecionar_cidadao():
    title = "Selecione o cidadão"
    button_novo_cidadao = button_layout(url='regulacao.cidadao_novo', classname='button is-primary', label='Novo cidadao')
    return render_template('pages/regulacao/selecionar_cidadao.html', button_layout=button_novo_cidadao, title=title)

@bp_regulacao.route('/protocolo/form', methods=['GET', 'POST'])
@login_required
def form_protocolo():
    
    form = ProtocoloForm()
    return render_template('pages/regulacao/form_protocolo.html', 
                           id_protocolo=None, 
                           form=form,
                           citizens=[]
                           )