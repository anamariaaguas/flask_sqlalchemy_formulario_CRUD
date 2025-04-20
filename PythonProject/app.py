from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db = SQLAlchemy(app)

class DadosFormulario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    mensagem = db.Column(db.String(200), nullable=False)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('formulario.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nome = request.form['nome']
    mensagem = request.form['mensagem']
    novo_dado = DadosFormulario(nome=nome, mensagem=mensagem)
    db.session.add(novo_dado)
    db.session.commit()
    return render_template('formulario.html', nome=novo_dado.nome, mensagem=novo_dado.mensagem)
@app.route('/listar')
def listar():
    dados = DadosFormulario.query.all()
    return render_template('lista.html', dados=dados)
@app.route('/deletar/<int:id>')
def deletar(id):
    dado_para_deletar = DadosFormulario.query.get_or_404(id)
    db.session.delete(dado_para_deletar)
    db.session.commit()
    return redirect(url_for('listar'))


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    # Busca o registro pelo ID
    dado = DadosFormulario.query.get_or_404(id)

    if request.method == 'POST':
        # Atualiza os dados do registro com os valores do formulário
        dado.nome = request.form['nome']
        dado.mensagem = request.form['mensagem']

        # Salva as alterações no banco de dados
        db.session.commit()

        # Redireciona para a página de listagem
        return redirect(url_for('listar'))

    # Renderiza o template de edição com os dados atuais
    return render_template('editar.html', dado=dado)
if __name__ == '__main__':
    app.run(debug=True)