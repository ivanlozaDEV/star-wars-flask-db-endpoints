from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    favorites = db.relationship('Favorites', backref='user', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

    def __repr__(self):
        return '<User %r>' % self.username
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.Integer, nullable=True)
    orbital_period = db.Column(db.Integer, nullable=True)
    diameter = db.Column(db.Integer, nullable=True)
    climate = db.Column(db.String(250), nullable=True)
    terrain= db.Column(db.String(250), nullable=True)
    favorites= db.relationship('Favorites', backref= 'planet', lazy=True)



    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain 
             }
    
    def __repr__(self):
        return f"<Planet {self.name}>"
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(250), nullable=False)
    height = db.Column(db.Integer, nullable=True)
    mass = db.Column(db.Integer, nullable=True)
    hair_color= db.Column(db.String(250), nullable=True)
    skin_color= db.Column(db.String(250), nullable=True)
    eye_color= db.Column(db.String(250), nullable=True)
    birth_year= db.Column(db.String(250), nullable=True)
    gender= db.Column(db.String(250), nullable=True)
    favorites = db.relationship('Favorites', backref='character', lazy=True)


    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
        }
    def __repr__(self):
        return f"<Character {self.name}>"


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model= db.Column(db.String(250), nullable=False)
    cost = db.Column(db.Integer, nullable=True)
    max_speed= db.Column(db.Integer, nullable=True)
    crew= db.Column(db.Integer, nullable=True)
    passengers= db.Column(db.Integer, nullable=True)
    cargo_capacity= db.Column(db.Integer, nullable=True)
    consumables=db.Column(db.Integer, nullable=True)
    hyperdrive_rating= db.Column(db.String(250), nullable=True)
    favorites= db.relationship('Favorites', backref='vehicle', lazy=True)


    def serialize(self):
        return{
            "id": self.id,
            "model": self.model,
            "cost": self.cost,
            "max_speed": self.max_speed,
            "passengers": self.passengers,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "hyperdrive_rating": self.hyperdrive_rating
        }
    def __repr__(self):
        return f"<Vehicle {self.model}>"
   

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    character_id =db. Column(db.Integer, db.ForeignKey('character.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))

    def __init__(self, user_id, planet_id=None, character_id=None, vehicle_id=None):
        self.user_id = user_id
        self.planet_id = planet_id
        self.character_id = character_id
        self.vehicle_id = vehicle_id

    def __repr__(self):
        return f"<Favorites user_id={self.user_id}>"