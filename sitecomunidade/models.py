# Estrutura do Banco de Dados
from sitecomunidade import database, login_manager
from flask_login    import UserMixin ## controle de Login
# data
from datetime import datetime

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id          = database.Column(database.Integer, primary_key=True)
    username    = database.Column(database.String, nullable=False)
    senha       = database.Column(database.String)
    email       = database.Column(database.String, unique=True)
    foto_perfil = database.Column(database.String, default='padrao.jpg', nullable=False)
    cursos      = database.Column(database.String, default='Não Informado', nullable=False)
    posts       = database.relationship('Post', backref='autor', lazy=True)

    def contar_posts(self):
        return len(self.posts)

class Post(database.Model):
    id          = database.Column(database.Integer, primary_key=True)
    titulo      = database.Column(database.String, nullable=False)
    corpo       = database.Column(database.Text, nullable=False)
    ## utcnow --> passa objeto e não função por isso sem o ()
    data        = database.Column(database.DateTime, default=datetime.utcnow, nullable=False,)
    id_usuario  = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)