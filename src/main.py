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
    planets_query = Planets.query.all()
    all_planets = list(map(lambda planet: planet.serialize(),planets_query))
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

delete_planet = Planets.query.get(planet_id)
if delete_planet is None:
   raise APIException("El planeta que queires eliminar no ha sido encontrado", status_code=404)
db.session.delete(delete_planet)
db.session.commit()

@app.route('/Characters/all', methods=['GET'])
def Personajes_Favoritos():
    characters_query = Characters.query.all()
    all_characters = list(map(lambda character: character.serialize(), characters_query))
    return jsonify(all_characters), 200

@app.route('/Character', methods=['POST'])
def Post_Character():
    homeworld = request.json.get("homeworld", None)
    if homeworld is None:
        raise APIException("No has ingresado el planeta origen", status_code=400)
    name = request.json.get("name", None)
    if name is None:
        raise APIException("No has ingresado el nombre", status_code=400)

    new_Character = Characters(homeworld=homeworld, name=name)
    db.session.add(new_Character)
    db.session.commit()
    return jsonify(new_Character.serialize()), 200

delete_character = Characters.query.get(character_id)
if delete_character is None:
   raise APIException("El personaje que queires eliminar no ha sido encontrado", status_code=404)
db.session.delete(delete_character)
db.session.commit()

@app.route('/Starships/all', methods=['GET'])
def Naves_Favoritos():
    starships_query = Starships.query.all()
    all_starships = list(map(lambda starship: starship.serialize(), starships_query))
    return jsonify(all_starships), 200

@app.route('/Starship', methods=['POST'])
def Post_Starship():
    model = request.json.get("model", None)
    if model is None:
        raise APIException("No has ingresado el modelo", status_code=400)
    name = request.json.get("name", None)
    if name is None:
        raise APIException("No has ingresado el nombre", status_code=400)
    
    new_Starship = Starships(model=model, name=name)
    db.session.add(new_Starship)
    db.session.commit()
    return jsonify(new_Starship.serialize()), 200

delete_starship = Starships.query.get(starship_id)
if delete_starship is None:
   raise APIException("La nave que queires eliminar no ha sido encontrada", status_code=404)
db.session.delete(delete_starship)
db.session.commit()

@app.route('/Pilots/all', methods=['GET'])
def Pilotos_Favoritos():
    pilots_query = Pilots.query.all()
    all_pilots = list(map(lambda pilots: pilots.serialize(), pilots_query))
    return jsonify(all_pilots), 200

@app.route('/Pilot', methods=['POST'])
def Post_Pilot():
    Characters_id = request.json.get("Characters_id", None)
    if Characters_id is None:
        raise APIException("No has ingresado el ID del Personaje", status_code=400)
    Starship_id = request.json.get("Starship_id", None)
    if Starship_id is None:
        raise APIException("No has ingresado el ID de la Nave", status_code=400)

    new_Pilot = Pilots(Characters_id=Characters_id, Starship_id=Starship_id)
    db.session.add(new_Pilot)
    db.session.commit()
    return jsonify(new_Pilot.serialize()), 200

delete_pilot = Pilots.query.get(pilot_id)
if delete_pilot is None:
   raise APIException("El piloto que queires eliminar no ha sido encontrado", status_code=404)
db.session.delete(delete_pilot)
db.session.commit()

@app.route('/User/favscharacters/<int:user_id>', methods=['GET'])
def get_favscharacters(user_id):
    favorites_user = Characters.query.join(FavsCharacters, FavsCharacters.Characters_Relation_id == 
    Characters.id).filter(FavsCharacters.User_id == user_id).all()
    serialize_favorite_user = list(map(lambda favorite_user : favorite_user.serialize(), favorites_user))
    print(favorites_user)
    return jsonify(serialize_favorite_user), 200 

@app.route('/User/favscharacters/<int:user_id>', methods=['POST'])
def Post_Favorite_Characters():
    Characters_Relation_id = request.json.get("Characters_Relation_id", None)
    if Characters_Relation_id is None:
        raise APIException("No has ingresado el personaje favorito", status_code=400)
    User_id = request.json.get("User_id", None)
    if User_id is None:
        raise APIException("No has ingresado el id del usuario", status_code=400)
    
    new_FavCharacter = FavsCharacters(Characters_Relation_id=Characters_Relation_id, User_id=User_id)
    db.session.add(new_FavCharacter)
    db.session.commit()
    return jsonify(new_FavCharacter.serialize()), 200

delete_Favorite_Character = FavsCharacters.query.get(favcharacter_id)
if delete_Favorite_Character is None:
   raise APIException("El personaje que quieres eliminar no ha sido encontrado", status_code=404)
db.session.delete(delete_Favorite_Character)
db.session.commit()

@app.route('User/favsplanets/<int:user_id>', methods=['GET'])
def get_favsplanets(user_id):
    favorites_user = Planets.query.join(FavsPlanets, FavsPlanets.Planets_Relation_id ==
    Planets.id).filter(FavsPlanets.User_id == user_id).all()
    serialize_favorite_user = list(map(lambda favorite_user : favorite_user.serialize(), favorites_user))
    print(favorites_user)
    return jsonify(serialize_favorite_user), 200

@app.route('/User/favsplanets/<int:user_id>', methods=['POST'])
def Post_Favorite_Planets():
    Planets_Relation_id = request.json.get("Planets_Relation_id", None)
    if Planets_Relation_id is None:
        raise APIException("No has ingresado el planeta favorito", status_code=400)
    User_id = request.json.get("User_id", None)
    if User_id is None:
        raise APIException("No has ingresado el id del usuario", status_code=400)
    
    new_FavPlanet = FavsPlanets(Planets_Relation_id=Planets_Relation_id, User_id=User_id)
    db.session.add(new_FavPlanet)
    db.session.commit()
    return jsonify(new_FavPlanet.serialize()), 200

delete_Favorite_Planet = FavsPlanets.query.get(favplanet_id)
if delete_Favorite_Planet is None:
   raise APIException("El planeta que quieres eliminar no ha sido encontrado", status_code=404)
db.session.delete(delete_Favorite_Planet)
db.session.commit()

@app.route('User/favsstarships/<int:user_id>', methods=['GET'])
def get_favsstarships(user_id):
    favorites_user =Starships.query.join(FavsStarships, FavsStarships.Starships_Relation_id ==
    Starships.id).filter(FavsStarships,User_id == user_id).all()
    serialize_favorite_user = list(map(lambda favorite_user : favorite_user.serialize(), favorites_user))
    print(favorite_user)
    return jsonify(serialize_favorite_user), 200

@app.route('/User/favsstarships/<int:user_id>', methods=['POST'])
def Post_Favorite_Starship():
    Starships_Relation_id = request.json.get("Starships_Relation_id", None)
    if  Starships_Relation_id is None:
        raise APIException("No has ingresado la nave favorita", status_code=400)
    User_id = request.json.get("User_id", None)
    if User_id is None:
        raise APIException("No has ingresado el id del usuario", status_code=400)
    
    new_FavStarship = FavsStarships(Starships_Relation_id=Starships_Relation_id, User_id=User_id)
    db.session.add(new_FavStarship)
    db.session.commit()
    return jsonify(new_FavStarship.serialize()), 200 

delete_Favorite_Starship = FavsStarships.query.get(favstarship_id)
if delete_Favorite_Starship is None:
   raise APIException("La nave que quieres eliminar no ha sido encontrado", status_code=404)
db.session.delete(delete_Favorite_Starship)
db.session.commit()


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
