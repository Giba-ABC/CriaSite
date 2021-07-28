# criação do formulário - usando o flask
from flask_wtf import FlaskForm
# tratamento de arquivos
from flask_wtf.file import FileField, FileAllowed
# tipo de campos e botão
from wtforms   import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
# validações ...
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# busca o Usuario
from sitecomunidade.models import Usuario
### pegando o usuário
from flask_login import current_user

class formCriarConta(FlaskForm):
    username = StringField('Nome do Usuário', validators=[DataRequired()])
    email    = StringField('e-Mail', validators=[DataRequired(),Email()])
    senha    = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    confirma = PasswordField('Redigite a Senha', validators=[DataRequired(), EqualTo('senha')])
    botao    = SubmitField('Criar Conta')

    # função de suporte para o validators, criar função com nome _validate_
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email = email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado, use outro e-mail')

class formLogin(FlaskForm):
    email    = StringField('e-Mail', validators=[DataRequired(), Email()])
    senha    = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    lembrar  = BooleanField('Lembrar dados de Acesso')
    botaoL    = SubmitField('Fazer Login')

class formEditarPerfil(FlaskForm):
    username = StringField('Nome do Usuário', validators=[DataRequired()])
    email    = StringField('e-Mail', validators=[DataRequired(),Email()])
    foto_perfil = FileField('Atualizar foto de perfil !', validators=[FileAllowed(['jpg','png'])])
    curso_excel = BooleanField('Excel')
    curso_vba   = BooleanField('VBA')
    curso_pbi = BooleanField('PowerBI')
    curso_pyton = BooleanField('Python')
    curso_ppt = BooleanField('Apresentação')
    curso_sql = BooleanField('SQL')

    botao    = SubmitField('Alterar Perfil')

    def validate_email(self, email):
        # verifica se digitou outro email
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email = email.data).first()
            if usuario:
                raise ValidationError('E-mail já cadastrado, use outro e-mail')

class FormCriarPost(FlaskForm):
    titulo =  StringField('Titulo do Post', validators=[DataRequired(), Length(2,140)])
    corpo = TextAreaField('Escreva seu Post aqui', validators=[DataRequired()])
    botaoP = SubmitField('Criar Post')