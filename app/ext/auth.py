from flask_login import LoginManager

login_manager: LoginManager = LoginManager()

def init_app(app):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'#type: ignore 
    login_manager.login_message = "É necessário realizar o login para continuar"
    login_manager.login_message_category = 'info'