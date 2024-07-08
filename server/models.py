from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    # add relationship
    user_collections = db.relationship('User_collection', back_populates='user', cascade='all, delete-orphan')

    # add serialization rules


class Collection(db.Model, SerializerMixin):
    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String)
    title = db.Column(db.String)
    description = db.Column(db.String)
    reviews = db.Column(db.String)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)

    # add relationship
    user_collections = db.relationship('User_collection', back_populates='collection', cascade='all, delete-orphan')

    # add serialization rules


class User_collection(db.Model, SerializerMixin):
    __tablename__ = "user_collections"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    collection_id = db.Column(db.Integer, ForeignKey('collections.id'), nullable=False)

    # add relationship
    user = db.relationshp('User', back_populates='user_collections')
    collection = db.relationshp('Collection', back_populates='user_collections')
    
    # add serialization rules