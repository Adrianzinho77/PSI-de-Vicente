from utils import db


class Pizza(db.Model):
    __tablename__ = 'pizza'  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sabor = db.Column(db.String(280), nullable=False)
    imagem = db.Column(db.String(280), nullable=True)
    ingredientes = db.Column(db.String(280), nullable=True)
    preco = db.Column(db.Float, nullable=False)

    def __init__(self, sabor, imagem, ingredientes, preco):
        self.sabor = sabor
        self.imagem = imagem
        self.ingredientes = ingredientes
        self.preco = preco

    def __repr__(self):
        return f'<Pizza {self.sabor}>'
