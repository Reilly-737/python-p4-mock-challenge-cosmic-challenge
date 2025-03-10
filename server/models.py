from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    serialize_rules = ("-missions.planet", "-scientists.planets")
    
    # Add relationship
    missions = db.relationship("Mission", back_populates="planet", cascade="all, delete-orphan")
    scientists = association_proxy("missions", "scientist")
    # Add serialization rules


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    # Add relationship
    missions = db.relationship(
        "Mission", back_populates="scientist", cascade="all, delete-orphan")
    planets = association_proxy("missions", "planet")
    # Add serialization rules

    serialize_rules = ("-missions.scientist", "-planets.scientists")
    
    # Add validation
    @validates('name')
    def validate_name(self, key, name):
        if not name: 
            raise ValueError('Name cannot be empty.')
        return name
    @validates('field_of_study')
    def validate_field_of_study(self, k, field_of_study):
        if not field_of_study:
            raise ValueError('Field of study cannot be empty.')
        return field_of_study

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    scientist_id = db.Column(db.Integer, db.ForeignKey("scientists.id"))
    
    # Add relationships
    scientist = db.relationship("Scientist", back_populates="missions") 
    planet = db.relationship("Planet", back_populates="missions")
    
    # Add serialization rules
    serialize_rules = ("-scientist.missions", "-planet.missions" )
    # Add validation
    @validates('name')
    def validate_name(self, key, name):
        if not name: 
            raise ValueError('Name cannot be empty.')
        return name
    
    @validates('scientist_id')
    def validate_scientist_id(self, key, scientist_id):
        if not scientist_id: 
            raise ValueError('scientist_id has to be present.')
        return scientist_id
    
    @validates('planet_id')
    def validate_name(self, key, planet_id):
        if not planet_id: 
            raise ValueError('Planet_id cannot be empty.')
        return planet_id

# add any models you may need.
