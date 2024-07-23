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
from models import db, User, Planet, Character, Vehicle, Favorites
#from models import Person
from werkzeug.security import generate_password_hash, check_password_hash

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


@app.route('/register', methods= ['POST'])
def user_register():
    try:
        body = request.json
        username= body.get("username", None)
        email= email.get("email", None)
        password = body.get("password", None)

        if username is None or  email is None or password is None:
            return jsonify({"error" : "username, email and password are requiered"}), 400
        
        email_is_taken = User.query.filter_by(email=email).first()
        if email_is_taken:
            return jsonify({"error":"Email is already in use"}), 400
        
        username_is_taken = User.query.filter_by(username=username).first()
        if username_is_taken:
            return jsonify({"error":"Username is already in use"}), 400
        
        password_hash = generate_password_hash(password)


        user = User(username= username, email=email, password= password_hash )
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg":"User created"}), 201
    
    except Exception as error:
        return jsonify ({"error": f"{error}"}), 500
        

@app.route('/character', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    serialized_characters= [character.serialize() for character in characters]
    return jsonify({"characters": serialized_characters})

@app.route('/character', methods=["POST"])
def add_character():
    body = request.json

    name = body.get("name", None)
    height = body.get("height", None)
    mass = body.get("mass", None)
    hair_color= body.get("hair_color", None)
    skin_color= body.get("skin_color", None)
    eye_color= body.get("eye_color", None)
    birth_year= body.get("birth_year", None)
    gender= body.get("gender", None)

    if name is None or height is None or mass is None or hair_color is None or skin_color is None or eye_color is None or birth_year is None or gender is None:
        return jsonify ({"error": "missing fields"}), 400

    character = Character( name= name, height= height, mass = mass , hair_color = hair_color , skin_color = skin_color , eye_color = eye_color, birth_year = birth_year, gender = gender )

    try:
        db.session.add(character)
        db.session.commit()
        db.session.refresh(character)

        return jsonify({"message": f"Character created {character.name}!"}), 201
    
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500

@app.route('/planet', methods=["POST"])
def add_planet():
    body = request.json

    name = body.get("name", None)
    orbital_period = body.get("orbital_period", None)
    diameter = body.get("diameter", None)
    rotation_period= body.get("rotation_period", None)
    climate= body.get("climate", None)
    terrain= body.get("terrain", None)
    

    if name is None or orbital_period is None or diameter is None or rotation_period is None or climate is None or terrain is None:
        return jsonify ({"error": "missing fields"}), 400

    planet = Planet( name= name, orbital_period= orbital_period, diameter = diameter , rotation_period = rotation_period , climate = climate , terrain = terrain )

    try:
        db.session.add(planet)
        db.session.commit()
        db.session.refresh(planet)

        return jsonify({"message": f"Planet created {planet.name}!"}), 201
    
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500

@app.route('/character/<int:id>', methods=['GET'])
def get_character(id):
    try:
        character = Character.query.get(id)
        if character is None:
            return jsonify({'error': "Character not found"}), 404
        return jsonify({"character": character.serialize()}), 200
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500

@app.route('/planet', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    serialized_planets= [planet.serialize() for planet in planets]
    return jsonify({"planets": serialized_planets})

@app.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):
    try:
        planet = Planet.query.get(id)
        if planet is None:
            return jsonify({'error': "Planet not found"}), 404
        return jsonify({"planet": planet.serialize()}), 200
    except Exception as error:
        return jsonify({"error": f"{error}"}), 



@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    vehicles = Vehicle.query.all()
    serialized_vehicles= [vehicle.serialize() for vehicle in vehicles]
    return jsonify({"vehicles": serialized_vehicles})

@app.route('/vehicle/<int:id>', methods=['GET'])
def get_vehicle(id):
    try:
        vehicle = Vehicle.query.get(id)
        if vehicle is None:
            return jsonify({'error': "vehicle not found"}), 404
        return jsonify({"vehicle": vehicle.serialize()}), 200
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500

@app.route('/user', methods=['GET'])
def get_all_users():   
    users = User.query.all()
    serialized_users= [user.serialize() for user in users]
    return jsonify({"users":serialized_users})

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    try:
       
        favorites = Favorites.query.filter_by(user_id=user_id).all()
        serialized_favorites = []
        for favorite in favorites:
            favorite_data = {"id": favorite.id}
            if favorite.planet_id:
                planet = Planet.query.get(favorite.planet_id)
                favorite_data["planet"] = planet.serialize() if planet else None
            if favorite.character_id:
                character = Character.query.get(favorite.character_id)
                favorite_data["character"] = character.serialize() if character else None
            if favorite.vehicle_id:
                vehicle = Vehicle.query.get(favorite.vehicle_id)
                favorite_data["vehicle"] = vehicle.serialize() if vehicle else None
            serialized_favorites.append(favorite_data)

        return jsonify({"user_id": user_id, "favorites": serialized_favorites})

    except Exception as error:
             return jsonify({"error": f"{error}"}), 500


@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"error": "Planet not found"}), 404
    

        new_favorite= Favorites(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify ({"Success": "New favorite planet added"}), 200
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500 
    
@app.route('/user/<int:user_id>/favorites/character/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        character = Character.query.get(character_id)
        if not character:
            return jsonify({"error": "Character not found"}), 404
    

        new_favorite= Favorites(user_id=user_id, character_id=character_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify ({"Success": "New favorite character added"}), 200
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500 

@app.route('/user/<int:user_id>/favorites/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(user_id, vehicle_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
    

        new_favorite= Favorites(user_id=user_id, vehicle_id=vehicle_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify ({"Success": "New favorite vehicle added"}), 200
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500 

@app.route('/user/<int:user_id>/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"error": "Planet not found"}), 404

        favorite = Favorites.query.filter_by(user_id= user_id, planet_id=planet_id).first()
        if not favorite:
            return jsonify({"error": "Favorite not found"}), 404

       
        db.session.delete(favorite)
        db.session.commit()

        return jsonify ({"Success": "favorite planet deleted"}), 200
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500 

@app.route('/user/<int:user_id>/favorites/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        character = Character.query.get(character_id)
        if not character:
            return jsonify({"error": "Character not found"}), 404

        favorite = Favorites.query.filter_by(user_id= user_id, character_id=character_id).first()
        if not favorite:
            return jsonify({"error": "Favorite not found"}), 404

        
        db.session.delete(favorite)
        db.session.commit()

        return jsonify ({"Success": "favorite character deleted"}), 200
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500 
    
@app.route('/user/<int:user_id>/favorites/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(user_id, vehicle_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404

        favorite = Favorites.query.filter_by(user_id= user_id, vehicle_id=vehicle_id).first()
        if not favorite:
            return jsonify({"error": "Favorite not found"}), 404

        
        db.session.delete(favorite)
        db.session.commit()

        return jsonify ({"Success": "favorite vehicle deleted"}), 200
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500 

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
