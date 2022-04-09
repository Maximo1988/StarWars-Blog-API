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
from models import db, User, Characters, FavsCharacters, FavsPlanets, FavsStarships, Planets, Starships, Pilots
#from models import Person
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# generate sitemap with all your endpoints
@app.route('/Planets/all', methods=['GET'])
def Planetas_Favoritos():
    planets_query=Planets.query.all()
    all_planets=list(map(lambda planet: planet.serialize(),planets_query))
    return jsonify(all_planets), 200

@app.route('/Planet', methods=['POST'])
def Post_Planet():
    diameter = request.json.get("diameter", None)
    if diameter is None:
        raise APIException("No has ingresado el diámetro", status_code=400)
    name = request.json.get("name", None)
    if name is None:
        raise APIException("No has ingresado el nombre", status_code=400)

    new_Planet = Planets(diameter=diameter, name=name)
    db.session.add(new_Planet)
    db.session.commit()
    return jsonify(new_Planet.serialize()), 200

@app.route('/User/favscharacters/<int:user_id>', methods=['GET'])
def get_favscharacters(user_id):
    favorites_user = Characters.query.join(FavsCharacters, FavsCharacters.Characters_Relation_id == 
    Characters.id).filter(FavsCharacters.User_id == user_id).all()
    serialize_favorite_user = list(map(lambda favorite_user : favorite_user.serialize(), favorites_user))
    print(favorites_user)
    return jsonify(serialize_favorite_user), 200
    
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    pw_hash = bcrypt.generate_password_hash('hunter2')
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

@app.route('/person/<int:person_id>', methods=['PUT', 'GET'])
def get_single_person(person_id):
    """
    Single person
    """
    body = request.get_json() #{ 'username': 'new_username'}
    if request.method == 'PUT':
        user1 = Person.query.get(person_id)
        user1.username = body.username
        db.session.commit()
        return jsonify(user1.serialize()), 200
    if request.method == 'GET':
        user1 = Person.query.get(person_id)
        return jsonify(user1.serialize()), 200

    return "Invalid Method", 404
