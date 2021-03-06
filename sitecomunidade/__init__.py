# Bibliotecas
from flask import Flask
# importa os objetos do forms
# from sitecomunidade.forms import formLogin, formCriarConta
# Banco de Dados - suporte Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
##############
# criação de token import secrets secrets.hotken_hex(16)
app.config['SECRET_KEY'] = 'e78c855a27ee91c8eece771236535242'
### Caminho banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)
# criptografia no site
bcrypt = Bcrypt(app)
# controle de Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'  ## indicar pagina apos confirmação do acesso a pagina
login_manager.login_message_category = 'alert-info'


# carrega os direcionadores - depois de criar o app
from sitecomunidade import routes
