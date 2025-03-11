from flask import render_template, request, redirect, flash, url_for
from models.Usuario import Usuario
from utils import db
from flask import Blueprint

bp_usuarios = Blueprint("usuarios", __name__, template_folder='templates')

@bp_usuarios.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template('usuarios_create.html')
    
    elif request.method == "POST":
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        csenha = request.form.get('csenha')

        if not nome or not email or not senha:
            flash('Todos os campos são obrigatórios!', 'danger')
            return redirect(url_for('.create'))

        if senha != csenha:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('.create'))

        # Verificar se o e-mail já está cadastrado
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('.create'))

        usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('.recovery'))


@bp_usuarios.route('/recovery', defaults={'id': 0})
@bp_usuarios.route('/recovery/<int:id>')
def recovery(id):
    if id == 0:
        usuarios = Usuario.query.all()
        return render_template('usuarios_recovery.html', usuarios=usuarios)
    else:
        usuario = Usuario.query.get(id)
        if usuario:
            return render_template('usuarios_detalhes.html', usuario=usuario)
        flash('Usuário não encontrado!', 'danger')
        return redirect(url_for('.recovery'))


@bp_usuarios.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        flash('Usuário não encontrado!', 'danger')
        return redirect(url_for('.recovery'))

    if request.method == 'GET':
        return render_template('usuarios_update.html', usuario=usuario)

    if request.method == 'POST':
        usuario.nome = request.form.get('nome', usuario.nome)
        usuario.email = request.form.get('email', usuario.email)
        
        senha = request.form.get('senha')
        csenha = request.form.get('csenha')

        if senha:
            if senha == csenha:
                usuario.senha = senha
            else:
                flash('As senhas não coincidem!', 'danger')
                return redirect(url_for('.update', id=id))

        db.session.commit()
        flash('Dados atualizados com sucesso!', 'success')
        return redirect(url_for('.recovery'))


@bp_usuarios.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        flash('Usuário não encontrado!', 'danger')
        return redirect(url_for('.recovery'))

    if request.method == 'GET':
        return render_template('usuarios_delete.html', usuario=usuario)
    
    if request.method == 'POST':
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário excluído com sucesso!', 'success')
        return redirect(url_for('.recovery'))
