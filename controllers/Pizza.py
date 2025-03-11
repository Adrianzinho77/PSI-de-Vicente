from flask import render_template, request, redirect, flash, url_for
from models.Pizza import Pizza  
from utils import db
from flask import Blueprint

bp_pizzas = Blueprint("pizzas", __name__, template_folder='templates')

@bp_pizzas.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template('pizza_create.html')
    
    elif request.method == "POST":
        sabor = request.form['sabor']
        imagem = request.form['imagem']
        ingredientes = request.form['ingredientes']
        preco = request.form['preco']

        pizza = Pizza(sabor=sabor, imagem=imagem, ingredientes=ingredientes, preco=preco)
        db.session.add(pizza)
        db.session.commit()
        flash('Pizza criada com sucesso!', 'success')
        return redirect(url_for('.recovery'))

@bp_pizzas.route('/recovery', defaults={'id': 0})
@bp_pizzas.route('/recovery/<int:id>')
def recovery(id):
    if id == 0:
        pizzas = Pizza.query.all()
        return render_template('pizza_recovery.html', pizzas=pizzas)
    else:
        pizza = Pizza.query.get(id)
        return render_template('pizza_detalhes.html', pizza=pizza)

@bp_pizzas.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if id and request.method == 'GET':
        pizza = Pizza.query.get(id)
        return render_template('pizza_update.html', pizza=pizza)

    if request.method == 'POST':
        pizza = Pizza.query.get(id)
        pizza.sabor = request.form.get('sabor')
        pizza.imagem = request.form.get('imagem')
        pizza.ingredientes = request.form.get('ingredientes')
        pizza.preco = request.form.get('preco')

        db.session.add(pizza)
        db.session.commit()
        flash('Pizza atualizada com sucesso!')
        return redirect(url_for('.recovery', id=id))

@bp_pizzas.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if id == 0: 
        flash('É preciso definir uma pizza para ser excluída') 
        return redirect(url_for('.recovery'))

    if request.method == 'GET':
        pizza = Pizza.query.get(id)
        return render_template('pizza_delete.html', pizza=pizza)
    
    if request.method == 'POST':
        pizza = Pizza.query.get(id)
        db.session.delete(pizza)
        db.session.commit()
        flash('Pizza excluída com sucesso!')
        return redirect(url_for('.recovery'))
