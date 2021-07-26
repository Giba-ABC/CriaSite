# Bibliotecas
from flask import Flask
# importa os objetos do forms
# from sitecomunidade.forms import formLogin, formCriarConta
# Banco de Dados - suporte Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
##############
# criação de token import secrets secrets.hotken_hex(16)
app.config['SECRET_KEY'] = 'e78c855a27ee91c8eece771236535242'
### Caminho banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)
# carrega os direcionadores - depois de criar o app
from sitecomunidade import routes
