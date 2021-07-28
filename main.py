# https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application
# pip install flask
# pip install flask-wtf (criação de formulários - forms.py
# pip install email_validator
# pip install flask-sqlalchemy (banco de dados)
# pip install flask-bcrypt (criptografia da senha)
# pip install flask-login
# pip install pillow - compacta imagem

from sitecomunidade import app

if __name__ == '__main__':
    app.run(debug=True) ## atualiza o site sem precisar para o APP

