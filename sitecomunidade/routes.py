from flask import render_template, redirect, flash, url_for, request
from sitecomunidade import app
from sitecomunidade.forms import formLogin, formCriarConta

## Lista Usuários
usuarios = ['Giba','Bia','Visitante']

@app.route("/")  ## indica qual url começa o site
def inicio():
    return render_template('home.html')

@app.route("/contato")  ## criei a pasta contato
def dizai():
    return render_template('contato.html')

@app.route("/usuarios")  ## criei a pasta contato
def usuario():
    return render_template('usuarios.html', usuarios=usuarios)

# libera no html o metodo post e get (post - envia dados, get - carrega dados
@app.route("/login", methods=['GET','POST'])  ## criei a pasta contato
def login():
    Form_login = formLogin()
    Form_Cria  = formCriarConta()
    # verifica se conseguiu executar o botão com sucesso ! - request !
    if Form_login.validate_on_submit() and 'botaoL' in request.form:
        # conseguiu submeter o login (preencheu os campos corretamente
        # mensagem de ok -- flash e volta para o Inicio
        flash(f'Login feito com Sucesso no email: {Form_login.email.data}', 'alert-success')
        return redirect(url_for('inicio'))

    if Form_Cria.validate_on_submit() and 'botao' in request.form:
        flash(f'Conta criada para o {Form_login.email.data} com Suesso !! ', 'alert-success')
        return redirect(url_for('inicio'))

    return render_template('login.html', Form_login=Form_login, Form_Cria=Form_Cria)