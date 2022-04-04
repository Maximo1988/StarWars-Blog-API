from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.User

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    __tablename__ = 'Characters'
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50), nullable=False)
    height = db.Column(String(50)) 
    mass = db.Column(String(50))
    hair_color = db.Column(String(50))
    eye_color = db.Column(String(50))
    birth_year = db.Column(String(50))
    gender = db.Column(String(50))
    homeworld = db.Column(String(50))
    url = db.Column(String(50))
    description = db.Column(String(50))
    user_from_id = db.Column(Integer, ForeignKey('User.id'))
    user = relationship(User)

    def __repr__(self):
        return '<Characters %r>' % self.Characters

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "height": self.height, 
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "url": self.url,
            "description": self.description,
        }

class Planets(db.Model):
    __tablename__ = 'Planets'
    id = db.Column(Integer, primary_key=True)
    diameter = db.Column(String(50))
    rotation_period = db.Column(String(50))
    orbital_period = db.Column(String(50))
    gravity = db.Column(String(50))
    population = db.Column(String(50))
    climate = db.Column(String(50))
    terrain = db.Column(String(50))
    surface_water = db.Column(String(50))
    name = db.Column(String(50))
    url = db.Column(String(50))
    description = db.Column(String(50))
    characters_id = db.Column(Integer, ForeignKey('Characters.id'))
    characters = relationship(Characters)
    pilots_id = db.Column(Integer, ForeignKey('Pilots.id'))
    user_from_id = db.Column(Integer, ForeignKey('User.id'))
    user = relationship(User)

    def __repr__(self):
        return '<Planets %r>' % self.Planets

    def serialize(self):
        return {
            "id": self.id,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period, 
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "characters_id": self.characters_id,
            "pilots_id": self.pilots_id,
            "user_from_id": self.user_from_id,
        }

class Starships(db.Model):
    __tablename__ = 'Starships'
    id = db.Column(Integer, primary_key=True)
    model = db.Column(String(50))
    starship_class = db.Column(String(50))
    manufacturer = db.Column(String(50))
    cost_in_credits = db.Column(String(50))
    length = db.Column(String(50))
    crew = db.Column(String(50))
    passengers = db.Column(String(50))
    max_atmosphering_speed = db.Column(String(50))
    hyperdrive_rating = db.Column(String(50))
    MGLT = db.Column(String(50))
    cargo_capacity = db.Column(String(50))
    consumables = db.Column(String(50))
    name = db.Column(String(50))
    url = db.Column(String(50))
    description = db.Column(String(50))
    pilots_id = db.Column(Integer, ForeignKey('Pilots.id'))
    user_from_id = db.Column(Integer, ForeignKey('User.id'))
    user = relationship(User)

    def __repr__(self):
        return '<Starships %r>' % self.Starships

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "starship_class": self.starship_class, 
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "hyperdrive_rating": self.hyperdrive_rating,
            "MGLT": self.MGLT,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "pilots_id": self.pilots_id,
            "user_from_id": self.user_from_id,
        }
    
class FavsCharacters(db.Model):
    __tablename__ = 'FavsCharacters'
    id = db.Column(Integer, primary_key=True)
    Characters_Name = db.Column(String(50), ForeignKey('Characters.name'))
    Characters = relationship(Characters)
    User_id = relationship(User)

    def __repr__(self):
        return '<FavsCharacters %r>' % self.FavsCharacters

    def serialize(self):
        return {
            "id": self.id,
            "Characters_Name": self.Characters_Name,
        }

class FavsPlanets(db.Model):
    __tablename__ = 'FavsPlanets'
    id = db.Column(Integer, primary_key=True)
    Planets_Name = db.Column(String(50), ForeignKey('Planets.name'))
    Planets = relationship(Planets)
    User_id = relationship(User)

    def __repr__(self):
        return '<FavsPlanets %r>' % self.FavsPlanets

    def serialize(self):
        return {
            "id": self.id,
            "Planets_Name": self.Planets_Name,
        }

class FavsStarships(db.Model):
    __tablename__ = 'FavsStarships'
    id = db.Column(Integer, primary_key=True)
    Starships_Name = db.Column(String(50), ForeignKey('Starships.name'))
    Starships = relationship(Starships)
    User_id = relationship(User)

    def __repr__(self):
        return '<FavsStarships %r>' % self.FavsStarships

    def serialize(self):
        return {
            "id": self.id,
            "Starships_Name": self.Starships_Name,
        }

class Pilots(db.Model):
    __tablename__ = 'Pilots'
    id = db.Column(Integer, primary_key=True)
    Characters_Name = db.Column(String(50), ForeignKey('Characters.id'))
    Characters = relationship(Characters)
    Starship_Name = db.Column(String(50), ForeignKey('Starships.id'))
    Starships = relationship(Starships)

    def __repr__(self):
        return '<Pilots %r>' % self.Pilots

    def serialize(self):
        return {
            "id": self.id,
            "Characters_Name": self.Characters_Name,
            "Starship_Name": self.Starship_Name,
        }

    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')