from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)
bcrypt = Bcrypt()


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column(db.String, nullable=False)

    @hybrid_property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, new_password):
        hash = bcrypt.generate_password_hash(new_password.encode('utf-8'))
        self._password = hash

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password, password.encode('utf-8'))

    # add relationship
    user_collections = db.relationship('User_collection', back_populates='user', cascade='all, delete-orphan')

    # add serialization rules
    serialize_rules = ['-_password']

class Collection(db.Model, SerializerMixin):
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    type = db.Column(db.String)
    description = db.Column(db.String)
    reviews = db.Column(db.String)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))

     # add relationship
    user_collections = db.relationship('User_collection', back_populates='collection', cascade='all, delete-orphan')
    collection_items = db.relationship('CollectionItem', back_populates='collection')
    
    # add serialization rules
    serialize_rules = ['-user_collections.user', '-user_collections.collection']


class CollectionItem(db.Model, SerializerMixin):
    __tablename__ = "collection_items"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    name = db.Column(db.String)
    address = db.Column(db.String)
    comment = db.Column(db.String)
    review = db.Column(db.Integer)
    collection_id = db.Column(db.Integer, ForeignKey('collections.id'), nullable=False)

    # add relationship
    collection = db.relationship('Collection', back_populates='collection_items')

    # add serialization rules
    serialize_rules = ['-collection.collection_items']


class User_collection(db.Model, SerializerMixin):
    __tablename__ = "user_collections"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    collection_id = db.Column(db.Integer, ForeignKey('collections.id'), nullable=False)

    # add relationship
    user = db.relationship('User', back_populates='user_collections')
    collection = db.relationship('Collection', back_populates='user_collections')
    
    # add serialization rules
    serialize_rules = ['-user.user_collections', '-collection.user_collections']