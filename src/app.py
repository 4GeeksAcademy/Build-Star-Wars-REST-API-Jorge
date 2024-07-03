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
from models import db, User, Personajes, Vehiculos, Planetas, Favoritos_personajes
#from models import Person

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

#métodos GET ALL
@app.route('/user', methods=['GET'])
def handle_hello():

    users = User.query.all()
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

#métodos para GET específico por ID
@app.route('/user/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    user = User.query.filter_by(id=people_id).first()
    user_serialize = user.serialize()

    response_body = {
        "msg": "Ok",
        "data": user_serialize
    }

    return jsonify(response_body), 200

#métodos para POST
@app.route('/user', methods=['POST'])
def create_user():
    body = request.json
    me = User(email=body["email"], password=body["password"], is_active=body["is_active"])
    db.session.add(me)
    db.session.commit()

    response_body = {
        "msg": "Ok",
        "id": me.id
    }

    return jsonify(response_body), 200

#métodos para DELETE


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
