# criação do formulário - usando o flask
from flask_wtf import FlaskForm
# tipo de campos e botão
from wtforms   import StringField, PasswordField, SubmitField, BooleanField
# validações ...
from wtforms.validators import DataRequired, Length, Email, EqualTo

class formCriarConta(FlaskForm):
    username = StringField('Nome do Usuário', validators=[DataRequired()])
    email    = StringField('e-Mail', validators=[DataRequired(),Email()])
    senha    = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    confirma = PasswordField('Redigite a Senha', validators=[DataRequired(), EqualTo('senha')])
    botao    = SubmitField('Criar Conta')

class formLogin(FlaskForm):
    email    = StringField('e-Mail', validators=[DataRequired(), Email()])
    senha    = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    lembrar  = BooleanField('Lembrar dados de Acesso')
    botaoL    = SubmitField('Fazer Login')