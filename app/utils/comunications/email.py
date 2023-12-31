import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import secrets

from flask import url_for

from app.models.token import Token
from app.models.users import Usuario

def gerar_token():
    # Gere um token único usando a biblioteca secrets
    return secrets.token_urlsafe(32)

def enviar_email(destinatario, assunto, body_txt=None, body_html=None):
    # Configurações do remetente
    remetente = str(os.getenv('EMAIL_USER'))
    senha = str(os.getenv('EMAIL_PASSWORD'))

    # Configurações do servidor SMTP do Gmail
    smtp_server = str(os.getenv('EMAIL_SMTP_SERVER'))
    smtp_port = str(os.getenv('EMAIL_SMTP_PORT'))

    # Configurando a mensagem
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto
    if body_txt:
        mensagem.attach(MIMEText(body_txt, 'plain'))
    if body_html:
        mensagem.attach(MIMEText(body_html, 'html'))

    # Iniciando a conexão com o servidor SMTP
    with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
        # Estabelecendo a conexão segura
        server.starttls()

        # Logando na conta do remetente
        server.login(remetente, senha)

        # Enviando o e-mail
        server.sendmail(remetente, destinatario, mensagem.as_string())


def novo_cadastro(nome_completo, username, senha, email):

    url = url_for('auth.login')
    destinatario = email
    assunto = f'Bem vindo {nome_completo} ao SIS-Health Plus!'

    corpo_email = f"""
    Olá {nome_completo},

    Bem-vindo ao Nosso Serviço! Estamos felizes em tê-lo como parte da nossa comunidade.

    Aqui estão suas credenciais de acesso:
    
    - Usuário: {username}
    - Senha: {senha}

    Por motivos de segurança, recomendamos que você altere sua senha assim que possível. 
    Para fazer isso, faça login em sua conta e vá para as configurações de perfil.

    Para acessar a nossa aplicação acesso o endereço:
    https://itaberai.sishp.edmaker.dev.br

    Se precisar de ajuda ou tiver alguma dúvida, não hesite em entrar em contato conosco.

    Atenciosamente,
    Centro de Soluções Tecnologicas em Saúde
    Secretaria Municipal de Sáude - Itaberaí/GO
    """

    try:
        enviar_email(destinatario, assunto, corpo_email)
        return {'enviado': True, 'msg': "Enviado com sucesso"}
    except Exception as e:
        print(e)
        return {'enviado': False, 'error': 'Não foi possivel enviar o email'}
    
def solicitação_de_recuperacao(nome_completo, username, email, user_id):
    destinatario = email
    assunto = 'Solicitação de Redefinição de Senha'

    # Gere um token exclusivo
    token = gerar_token()

    # Construa a URL com o token
    # url = f'http://localhost:5000/redefinir-senha/{username}?token={token}'
    url = url_for('redefinir_senha', username=username, token=token, _external=True)

    corpo_email = f"""
    Olá {nome_completo},

    Foi solicitada a redefinição de senha em nosso sistema. Se não foi você
    quem solicitou a redefinição de senha, por favor, ignore este e-mail. Caso
    tenha solicitado, clique no link abaixo para redefinir sua senha:

    {url}

    Atenciosamente,
    Centro de Soluções Tecnológicas em Saúde
    Secretaria Municipal de Saúde - Itaberaí/GO
    """

    try:
        # Salve o token associado ao usuário no banco de dados para verificação posterior
        Token.salvar_token_no_banco(user_id, token)

        # Envie o e-mail
        enviar_email(destinatario, assunto, corpo_email)

        return {'enviado': True, 'msg': "E-mail enviado com sucesso"}
    except Exception as e:
        print(e)
        return {'enviado': False, 'error': 'Não foi possível enviar o e-mail'}



    

    