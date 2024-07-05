"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Personajes, Vehiculos, Planetas, Favoritos_personajes, Favoritos_vehiculos, Favoritos_planetas


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

########################################## métodos GET ALL
@app.route('/users', methods=['GET'])
def handle_hello():
    users = Users.query.all()
    users_serialized = list(map(lambda item:item.serialize(), users))
    response_body = {
        "msg": "OK",
        "data": users_serialized
    }
    return jsonify(response_body), 200

@app.route('/personajes', methods=['GET'])
def handle_personajes():
    personajes = Personajes.query.all()
    personajes_serialized = list(map(lambda item:item.serialize(), personajes))
    response_body = {
        "msg": "OK",
        "data": personajes_serialized
    }
    return jsonify(response_body), 200

@app.route('/vehiculos', methods=['GET'])
def handle_vehiculos():
    vehiculos = Vehiculos.query.all()
    vehiculos_serialized = list(map(lambda item:item.serialize(), vehiculos))
    response_body = {
        "msg": "OK",
        "data": vehiculos_serialized
    }
    return jsonify(response_body), 200

@app.route('/planetas', methods=['GET'])
def handle_planetas():
    planetas = Planetas.query.all()
    planetas_serialized = list(map(lambda item:item.serialize(), planetas))
    response_body = {
        "msg": "OK",
        "data": planetas_serialized
    }
    return jsonify(response_body), 200

@app.route('/favoritos_personajes', methods=['GET'])
def handle_favoritos_personajes():
    favoritos_personajes = Favoritos_personajes.query.all()
    favoritos_personajes_serialized = list(map(lambda item:item.serialize(), favoritos_personajes))
    response_body = {
        "msg": "OK",
        "data": favoritos_personajes_serialized
    }
    return jsonify(response_body), 200

@app.route('/favoritos_vehiculos', methods=['GET'])
def handle_favoritos_vehiculos():
    favoritos_vehiculos = Favoritos_vehiculos.query.all()
    favoritos_vehiculos_serialized = list(map(lambda item:item.serialize(), favoritos_vehiculos))
    response_body = {
        "msg": "OK",
        "data": favoritos_vehiculos_serialized
    }
    return jsonify(response_body), 200

@app.route('/favoritos_planetas', methods=['GET'])
def handle_favoritos_planetas():
    favoritos_planetas = Favoritos_planetas.query.all()
    favoritos_planetas_serialized = list(map(lambda item:item.serialize(), favoritos_planetas))
    response_body = {
        "msg": "OK",
        "data": favoritos_planetas_serialized
    }
    return jsonify(response_body), 200

#################################################### métodos para GET específico por ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = Users.query.filter_by(id=user_id).first()
    user_serialize = user.serialize()
    response_body = {
        "msg": "Ok",
        "data": user_serialize
    }
    return jsonify(response_body), 200

@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def get_personaje_by_id(personaje_id):
    personaje = Personajes.query.filter_by(id=personaje_id).first()
    personaje_serialize = personaje.serialize()
    response_body = {
        "msg": "Ok",
        "data": personaje_serialize
    }
    return jsonify(response_body), 200

@app.route('/vehiculos/<int:vehiculo_id>', methods=['GET'])
def get_vehiculo_by_id(vehiculo_id):
    vehiculo = Vehiculos.query.filter_by(id=vehiculo_id).first()
    vehiculo_serialize = vehiculo.serialize()
    response_body = {
        "msg": "Ok",
        "data": vehiculo_serialize
    }
    return jsonify(response_body), 200

@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def get_planeta_by_id(planeta_id):
    planeta = Planetas.query.filter_by(id=planeta_id).first()
    planeta_serialize = planeta.serialize()
    response_body = {
        "msg": "Ok",
        "data": planeta_serialize
    }
    return jsonify(response_body), 200

@app.route('/favoritos_personajes/<int:favorito_personaje_id>', methods=['GET'])
def get_favorito_personaje_by_id(favorito_personaje_id):
    favorito_personaje = Favoritos_personajes.query.filter_by(id=favorito_personaje_id).first()
    favorito_personaje_serialize = favorito_personaje.serialize()
    response_body = {
        "msg": "Ok",
        "data": favorito_personaje_serialize
    }
    return jsonify(response_body), 200

@app.route('/favoritos_vehiculos/<int:favorito_vehiculo_id>', methods=['GET'])
def get_favorito_vehiculo_by_id(favorito_vehiculo_id):
    favorito_vehiculo = Favoritos_vehiculos.query.filter_by(id=favorito_vehiculo_id).first()
    favorito_vehiculo_serialize = favorito_vehiculo.serialize()
    response_body = {
        "msg": "Ok",
        "data": favorito_vehiculo_serialize
    }
    return jsonify(response_body), 200

@app.route('/favoritos_planetas/<int:favorito_planeta_id>', methods=['GET'])
def get_favorito_planeta_by_id(favorito_planeta_id):
    favorito_planeta = Favoritos_planetas.query.filter_by(id=favorito_planeta_id).first()
    favorito_planeta_serialize = favorito_planeta.serialize()

    response_body = {
        "msg": "Ok",
        "data": favorito_planeta_serialize
    }

    return jsonify(response_body), 200
#################################################### métodos para POST
@app.route('/users', methods=['POST'])
def create_user():
    body = request.json
    me = Users(email=body["email"], password=body["password"], is_active=body["is_active"])
    db.session.add(me)
    db.session.commit()
    response_body = {
        "msg": "Ok",
        "id": me.id
    }
    return jsonify(response_body), 200

@app.route('/personajes', methods=['POST'])
def create_personaje():
    body = request.json
    me = Personajes(name=body["name"], eye_color=body["eye_color"], hair_color=body["hair_color"])
    db.session.add(me)
    db.session.commit()
    response_body = {
        "msg": "Ok",
        "id": me.id
    }
    return jsonify(response_body), 200

@app.route('/vehiculos', methods=['POST'])
def create_vehiculo():
    body = request.json
    me = Vehiculos(name=body["name"], model=body["model"])
    db.session.add(me)
    db.session.commit()
    response_body = {
        "msg": "Ok",
        "id": me.id
    }
    return jsonify(response_body), 200

@app.route('/planetas', methods=['POST'])
def create_planeta():
    body = request.json
    me = Planetas(name=body["name"], population=body["population"])
    db.session.add(me)
    db.session.commit()
    response_body = {
        "msg": "Ok",
        "id": me.id
    }
    return jsonify(response_body), 200

@app.route('/favoritos_personajes', methods=['POST'])
def create_favorito_personaje():
    body = request.json
    me = Favoritos_personajes(personajes_relacion=body["personajes_relacion"], usuarios_relacion=body["usuarios_relacion"])
    db.session.add(me)
    db.session.commit()
    response_body = {
        "msg": "Ok",
        "id": me.id
    }
    return jsonify(response_body), 200

@app.route('/favoritos_vehiculos', methods=['POST'])
def create_favorito_vehiculo():
    body = request.json
    me = Favoritos_vehiculos(vehiculos_relacion=body["vehiculos_relacion"], usuarios_relacion=body["usuarios_relacion"])
    db.session.add(me)
    db.session.commit()
    response_body = {
        "msg": "Ok",
        "id": me.id
    }
    return jsonify(response_body), 200

@app.route('/favoritos_planetas', methods=['POST'])
def create_favorito_planeta():
    body = request.json
    me = Favoritos_planetas(planetas_relacion=body["planetas_relacion"], usuarios_relacion=body["usuarios_relacion"])
    db.session.add(me)
    db.session.commit()
    response_body = {
        "msg": "Ok",
        "id": me.id
    }
    return jsonify(response_body), 200
################################################### métodos para DELETE


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
