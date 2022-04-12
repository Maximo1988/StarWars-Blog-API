from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
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
    __tablename__ = 'Planets'
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
    homeworld = db.Column(db.Integer, db.ForeignKey('Planets.id', ondelete='CASCADE'))
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
    pilot_id = db.Column(db.Integer, db.ForeignKey('Characters.id', ondelete='CASCADE'))
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
    
class FavsCharacters(db.Model):
    __tablename__ = 'Favorite Characters'
    id = db.Column(db.Integer, primary_key=True)
    Characters_Relation_id = db.Column(db.Integer, db.ForeignKey('Characters.id', ondelete='CASCADE'))
    Characters_Relation = relationship(Characters, primaryjoin=Characters_Relation_id == Characters.id)
    User_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'))
    User_Relation = relationship(User, primaryjoin=User_id == User.id)

    def __repr__(self):
        return '<Favorite Characters %r>' % self.Characters_Relation_id

    def serialize(self):
        return {
            "id": self.id,
            "Characters_Relation_id": self.Characters_Relation_id,
        }

class FavsPlanets(db.Model):
    __tablename__ = 'Favorite Planets'
    id = db.Column(db.Integer, primary_key=True)
    Planets_Relation_id = db.Column(db.Integer, db.ForeignKey('Planets.id', ondelete='CASCADE'))
    Planets_Relation = relationship(Planets, primaryjoin=Planets_Relation_id == Planets.id)
    User_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'))
    User_Relation = relationship(User, primaryjoin=User_id == User.id)

    def __repr__(self):
        return '<Favorite Planets %r>' % self.Planets_Relation_id

    def serialize(self):
        return {
            "id": self.id,
            "Planets_Relation_id": self.Planets_Relation_id,
        }

class FavsStarships(db.Model):
    __tablename__ = 'Favorite Starships'
    id = db.Column(db.Integer, primary_key=True)
    Starships_Relation_id = db.Column(db.Integer, db.ForeignKey('Starships.id', ondelete='CASCADE'))
    Starships_Relation = relationship(Starships, primaryjoin=Starships_Relation_id == Starships.id)
    User_id = db.Column(db.Integer, db.ForeignKey('User.id', ondelete='CASCADE'))
    User_Relation = relationship(User, primaryjoin=User_id == User.id)

    def __repr__(self):
        return '<Favorite Starships %r>' % self.Starships_Relation_id

    def serialize(self):
        return {
            "id": self.id,
            "Starships_Relation_id": self.Starships_Relation_id,
        }

class Pilots(db.Model):
    __tablename__ = 'Pilots'
    id = db.Column(db.Integer, primary_key=True)
    Characters_id = db.Column(db.Integer, db.ForeignKey('Characters.id', ondelete='CASCADE'))
    Characters = relationship(Characters, primaryjoin=Characters_id == Characters.id )
    Starships_id = db.Column(db.Integer, db.ForeignKey('Starships.id', ondelete='CASCADE'))
    Starship_Relation_id = relationship(Starships, primaryjoin=Starships_id == Starships.id)

    def __repr__(self):
        return '<Pilots %r>' % self.Characters_id

    def serialize(self):
        return {
            "id": self.id,
            "Characters_id": self.Characters_id,
            "Starship_id": self.Starships_id,
        }

    def to_dict(self):
        return {}
