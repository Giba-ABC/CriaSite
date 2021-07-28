from flask import render_template, redirect, flash, url_for, request, abort
from sitecomunidade import app, database, bcrypt
from sitecomunidade.forms import formLogin, formCriarConta, formEditarPerfil, FormCriarPost   ## importar os formularios
from sitecomunidade.models import Usuario, Post ### carrega o objeto Usuario (tabela) + Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets ## cria token + alterar nome do arquivo up-load
import os      ## separa nome do arquivo e extensão
from PIL import Image # PIL = Pillow

# from sitecomunidade import database, bcrypt

## Lista Usuários
# busca do banco de dados

@app.route("/")  ## indica qual url começa o site
def inicio():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts = posts)

@app.route("/contato")  ## criei a pasta contato
def dizai():
    return render_template('contato.html')

@app.route("/usuarios")  ## criei a pasta contato
@login_required
def usuario():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

# libera no html o metodo post e get (post - envia dados, get - carrega dados
@app.route("/login", methods=['GET','POST'])  ## criei a pasta contato
def login():
    Form_login = formLogin()
    Form_Cria  = formCriarConta()
    # verifica se conseguiu executar o botão com sucesso ! - request !
    if Form_login.validate_on_submit() and 'botaoL' in request.form:
        # verificar se exite o usuario
        usuario = Usuario.query.filter_by(email = Form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, Form_login.senha.data):
            # conseguiu submeter o login (preencheu os campos corretamente
            # mensagem de ok -- flash e volta para o Inicio
            login_user(usuario, remember= Form_login.lembrar.data)
            flash(f'Login feito com Sucesso no email: {Form_login.email.data}', 'alert-success')
            # verifica origem do link
            # # par_next = '' # request.args.get('next')
            # # if par_next:
            # #     return redirect(url_for(par_next))
            # else:
            return redirect(url_for('inicio'))
        else:
            flash(f'Falha no acesso - email: {Form_login.email.data}', 'alert-danger')

    if Form_Cria.validate_on_submit() and 'botao' in request.form:
        senha_cript = bcrypt.generate_password_hash(Form_Cria.senha.data)
        # cria o registro na tabela usuário
        usuario = Usuario(username=Form_Cria.username.data, email=Form_Cria.email.data, senha=senha_cript)
        # adiciona sessao
        database.session.add(usuario)
        database.session.commit()

        flash(f'Conta criada para o {Form_login.email.data} com Sucesso !! ', 'alert-success')
        return redirect(url_for('inicio'))

    return render_template('login.html', Form_login=Form_login, Form_Cria=Form_Cria)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com Sucesso !! ', 'alert-success')
    return redirect(url_for('inicio'))

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil = foto_perfil)

@app.route('/post/criar', methods=['GET','POST'])
@login_required
def post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo = form.corpo.data, autor=current_user)
        database.session.add(post)  ## insert
        database.session.commit()
        flash(f'Post atualizado com Sucesso !! ', 'alert-success')
        return redirect(url_for('inicio'))

    return render_template('criarpost.html', form = form)

def salva_imagem(imagem):
    '''
        # alterar nome da imagem
        # reduzir imagem
        # salvar fotos_perfil
        # alterar no banco
    '''
    codigo = secrets.token_hex(8)
    arq, ext = os.path.splitext(imagem.filename)
    nome_completo = arq + codigo + ext
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_completo)
    tamanho_imagem = (200,200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho_imagem)
    imagem_reduzida.save(caminho_completo)

    return nome_completo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                # adicionar texto do .label na lista de cursos
                lista_cursos.append(campo.label.text)

    return ';'.join(lista_cursos)  ## concatena ... usando o ; como separador

@app.route('/perfil/editar',methods=['GET','POST'])
@login_required
def editar_perfil():
    # instanciar o formulario criado em forms
    form = formEditarPerfil()
    if form.validate_on_submit(): ## formulário valido
        current_user.email = form.email.data
        current_user.username = form.username.data
        # tratamento da foto ... grava nome e baixa arquivo na pasta de fotos_perfil + compactando imagem
        if form.foto_perfil.data:
            nome_imagem = salva_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        # varre o formulario (objeto e verifica os cursos selecionados
        current_user.cursos = atualizar_cursos(form)

        database.session.commit()
        flash(f'Perfil atualizado com Sucesso !! ', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil = foto_perfil, form=form)
    ## aqui o formulário para para o html

## editar o post - nova pagina
@app.route('/post/<post_id>', methods=['GET','POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post atualizado com Sucesso', 'alter-success' )
            return redirect(url_for('inicio'))
    else:
        form = None

    return render_template('post.html', post=post, form = form)

@app.route('/post/<post_id>/excluir', methods=['GET','POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluido com Sucesso', 'alert-danger')
        return redirect(url_for('inicio'))
    else:
        abort(403)
