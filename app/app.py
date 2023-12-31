# Arquivo principal da aplicacao
from flask import Flask
from app.ext import configuration
from app.utils.context_processors import inject_permissions
from app.utils.filters import format_data, format_cpf
from flask_talisman import Talisman

def minimal_app():
    app = Flask(__name__)
    app.jinja_env.filters['format_cpf'] = format_cpf
    app.jinja_env.filters['format_data'] = format_data
    app.context_processor(inject_permissions)
    Talisman(app, force_https=True)
    configuration.init_app(app)

    return app


def create_app():
    app = minimal_app()
    configuration.load_extensions(app)


    return app

