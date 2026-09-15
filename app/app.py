import os
# Arquivo principal da aplicacao
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from app.ext import configuration
from app.utils.context_processors import inject_permissions
from app.utils.filters import format_cns, format_data, format_cpf


def _env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in ("1", "true", "yes", "on")


def minimal_app():
    app = Flask(__name__)

    # Pega a URI do banco de dados da variável de ambiente
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        raise ValueError("A variável de ambiente DATABASE_URL não foi definida!")

    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise ValueError("A variável de ambiente SECRET_KEY não foi definida!")

    # Configura a URI do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.jinja_env.filters['format_cpf'] = format_cpf
    app.jinja_env.filters['format_cns'] = format_cns
    app.jinja_env.filters['format_data'] = format_data
    app.context_processor(inject_permissions)
    configuration.init_app(app)

    # Configurações de segurança aplicadas após o Dynaconf para terem precedência
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SESSION_COOKIE_SECURE'] = _env_bool('SESSION_COOKIE_SECURE', True)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.debug = False

    # Permite operar atrás de um proxy reverso (nginx)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    return app


def create_app():
    app = minimal_app()
    configuration.load_extensions(app)


    return app

