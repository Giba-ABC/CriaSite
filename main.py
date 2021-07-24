# https://flask.palletsprojects.com/en/2.0.x/quickstart/#a-minimal-application

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")  ## indica qual url começa o site
def hello_world():
    return render_template('home.html')

@app.route("/contato")  ## criei a pasta contato
def dizai():
    return render_template('contato.html')





if __name__ == '__main__':
    app.run(debug=True) ## atualiza o site sem precisar para o APP

