from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.String(50))
    name = db.Column(db.String(50))
    url = db.Column(db.String(50))
    description = db.Column(db.String(50))

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "diameter": self.diameter,
            "name": self.name,
            "url": self.url,
            "description": self.description,
        }

class Characters(db.Model):
    __tablename__ = 'Characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    homeworld = db.Column(db.Integer, db.ForeignKey('planets.id'))
    homeworld_relation = relationship(Planets, primaryjoin=homeworld == Planets.id)
    url = db.Column(db.String(100))
    description = db.Column(db.String(50))

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "homeworld": self.homeworld,
            "url": self.url,
            "description": self.description,
        }



class Starships(db.Model):
    __tablename__ = 'Starships'
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50))
    name = db.Column(db.String(50))
    url = db.Column(db.String(50))
    description = db.Column(db.String(50))
    pilot_id = db.Column(db.Integer, db.ForeignKey('Characters.id'))
    pilot_relation = relationship(Characters, primaryjoin=pilot_id == Characters.id)

    def __repr__(self):
        return '<Starships %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "name": self.name,
            "url": self.url,
            "description": self.description,
            "pilot_id": self.pilot_id,
        }
    
""" class FavsCharacters(db.Model):
    __tablename__ = 'FavsCharacters'
    id = db.Column(db.Integer, primary_key=True)
    Characters_Name = db.Column(db.String(50), db.ForeignKey('Characters.name'))
    Characters = db.relationship(Characters)
    User_id = db.relationship(User)

    def __repr__(self):
        return '<FavsCharacters %r>' % self.FavsCharacters

    def serialize(self):
        return {
            "id": self.id,
            "Characters_Name": self.Characters_Name,
        } """

""" class FavsPlanets(db.Model):
    __tablename__ = 'FavsPlanets'
    id = db.Column(db.Integer, primary_key=True)
    Planets_Name = db.Column(db.String(50), db.ForeignKey('Planets.name'))
    Planets = db.relationship(Planets)
    User_id = db.relationship(User)

    def __repr__(self):
        return '<FavsPlanets %r>' % self.FavsPlanets

    def serialize(self):
        return {
            "id": self.id,
            "Planets_Name": self.Planets_Name,
        }

class FavsStarships(db.Model):
    __tablename__ = 'FavsStarships'
    id = db.Column(db.Integer, primary_key=True)
    Starships_Name = db.Column(db.String(50), db.ForeignKey('Starships.name'))
    Starships = db.relationship(Starships)
    User_id = db.relationship(User)

    def __repr__(self):
        return '<FavsStarships %r>' % self.FavsStarships

    def serialize(self):
        return {
            "id": self.id,
            "Starships_Name": self.Starships_Name,
        }

class Pilots(db.Model):
    __tablename__ = 'Pilots'
    id = db.Column(db.Integer, primary_key=True)
    Characters_Name = db.Column(db.String(50), db.ForeignKey('Characters.id'))
    Characters = db.relationship(Characters)
    Starship_Name = db.Column(db.String(50), db.ForeignKey('Starships.id'))
    Starships = db.relationship(Starships)

    def __repr__(self):
        return '<Pilots %r>' % self.Pilots

    def serialize(self):
        return {
            "id": self.id,
            "Characters_Name": self.Characters_Name,
            "Starship_Name": self.Starship_Name,
        }

    def to_dict(self):
        return {} """
