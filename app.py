from flask import Flask, render_template, redirect, url_for, flash, request
from utils import db
import os
from flask_migrate import Migrate
from models.Usuario import Usuario
from controllers.Usuario import bp_usuarios
from models.Pizza import Pizza
from controllers.Pizza import bp_pizzas
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.register_blueprint(bp_usuarios, url_prefix='/usuarios')
app.register_blueprint(bp_pizzas, url_prefix='/pizzas')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'minha_chave_secreta')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'database.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        user = Usuario.query.filter_by(nome=usuario).first()

        if user and user.senha == senha:
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index')) 
        else:
            flash('Usuário ou senha incorretos!', 'danger')
            return redirect(url_for('login'))  
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        csenha = request.form['csenha']

        if senha != csenha:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('cadastro'))  

        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('cadastro'))  

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))  
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar usuário: {e}', 'danger')

    return render_template('usuarios_create.html')

if __name__ == '__main__':
    app.run(debug=True)
