import os
# Arquivo principal da aplicacao
from flask import Flask
from app.ext import configuration
from app.utils.context_processors import inject_permissions
from app.utils.filters import format_cns, format_data, format_cpf

def minimal_app():
    app = Flask(__name__)
    
    # Pega a URI do banco de dados da variável de ambiente
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        raise ValueError("A variável de ambiente DATABASE_URL não foi definida!")  
    
    # Configura a URI do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
    
    app.jinja_env.filters['format_cpf'] = format_cpf
    app.jinja_env.filters['format_cns'] = format_cns
    app.jinja_env.filters['format_data'] = format_data
    app.context_processor(inject_permissions)
    configuration.init_app(app)

    return app


def create_app():
    app = minimal_app()
    configuration.load_extensions(app)


    return app

