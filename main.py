from flask import Flask, Response, json
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/faketicias'
db = SQLAlchemy(app)

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column('id', db.Integer, primary_key = True)
    menu_id = db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'))
    name = db.Column('name', db.Unicode)
    quantity = db.Column('quantity', db.Integer)

class Menu (db.Model):
    __tablename__ = 'menu'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.Unicode)
    price = db.Column('price', db.Unicode)
    description = db.Column('description', db.Unicode)
    recipes = db.relationship('Recipe', backref='menu', lazy=True)

lista_faketicias = Menu.query.all()

@cross_origin()
@app.route('/menu')
def all_food_by_db():
    global json_banco
    json_banco = {
        "comidas": [
        ]}

    for i in range(len(lista_faketicias)):
        json_banco["comidas"].append({})

    for i in json_banco["comidas"]:
        json_banco["comidas"][json_banco["comidas"].index(i)] = {
            "id": lista_faketicias[json_banco["comidas"].index(i)].id,
            "name": lista_faketicias[json_banco["comidas"].index(i)].name,
            "price": lista_faketicias[json_banco["comidas"].index(i)].price,
            "description": lista_faketicias[json_banco["comidas"].index(i)].description
        }
    for i in json_banco["comidas"]:
        if i["id"] < 10:
            i["id"] = "0" + str(i["id"])

    return Response(response=json.dumps(json_banco),
                    content_type='Application/json',
                    status=200)

@cross_origin()
@app.route('/menuestatico')
def all_food():
    all = {
    "comidas" : [
        {
            "id": 1,
            "name": "Hamburguer",
            "price": "R$15.00",
            "description": "Duas fatias de pão fofinho, queijo, hamburguer e salada."
        },
        {
            "id": 2,
            "name": "Batata Frita",
            "price": "R$12.99",
            "description": "200g de Batata frita e molho a parte."
        },
        {
            "id": 3,
            "name": "Nuggets",
            "price": "R$9.99",
            "description": "8 unidades de nuggets bem crocantes com molho a parte."
        },
        {
            "id": 4,
            "name": "Milkshake",
            "price": "R$10.00",
            "description": "600ml de Milk Shake em diversos sabores."
        }

    ]

    }
    for i in all["comidas"]:
        if i["id"] < 10:
            i["id"] = "0" + str(i["id"])


    return Response(response=json.dumps(all),
                    content_type='Application/json',
                    status=200)

@app.route('/menu/<int:menu_id>')
def one_food(menu_id : int):  #mostrar o id e os recipes
    # ans = ''
    dict_ans = {}
    for i in lista_faketicias:
        if i.id == menu_id:
            # ans += i.name + ':'
            dict_ans = {
                str(i.name) : [
                    str(i.description)
                ]
            }
            for ingredientes in i.recipes:
                # ans += ('<br>' + str(ingredientes.quantity) + 'x ' + str (ingredientes.name))
                dict_ans[str(i.name)].append(str(ingredientes.quantity) + 'x ' + str(ingredientes.name))
    return dict_ans


if __name__ == "__main__":
    app.run()

