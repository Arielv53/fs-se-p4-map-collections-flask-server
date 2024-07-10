from models import db, Collection, User, User_collection, CollectionItem
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify, session
from flask_restful import Api, Resource
from flask_cors import CORS
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']


migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

CORS(app, supports_credentials=True)

@app.route("/")
def index():
    return "<h1>Phase 4 Project</h1>"

@app.route("/<int:user_id>/collections", methods=['GET', 'POST'])
def collections(user_id):
    if request.method == 'GET':
        collections = Collection.query.filter(Collection.user_id == user_id).all()
        return [collection.to_dict() for collection in collections], 200
    
    elif request.method == 'POST':
        data = request.get_json(user_id)

        try:
            new_collection = Collection(
                genre=data.get('genre'), 
                title=data.get('title'), 
                description=data.get('description'), 
                reviews=data.get('reviews'), 
                user_id=user_id
            )
        except ValueError as e:
            return {'error': str(e)}, 400
        
        db.session.add(new_collection)
        db.session.commit()

        return new_collection.to_dict(), 201
    
@app.route('/<int:collection_id>/items', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def all_items_by_collection_id(collection_id):
    items = CollectionItem.query.filter(CollectionItem.collection_id == collection_id).all()
    if request.method == 'GET':
        if not items:
            return {'error':'locations not found'}, 404
        return [i.to_dict() for i in items], 200
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return {'error': 'invalid request'}, 400
        try:
            new_item = CollectionItem(
                'type': data.get('type'),
                name: data.get('name'),
                address: data.get('address'),
                comment: data.get('comment'),
                review: data.get('review')
            )
        except ValueError as e:
            return {'error': str(e)}, 400
        
        db.session.add(new_item)
        db.session.commit()
        
        return new_item.to_dict(), 201
    
    elif request.method == 'PATCH':
        data = request.get_json()
        for field in data:
            try:
                setattr(items, field, data.get(f'{field}'))
            except ValueError as e:
                return {'error': str(e)}, 400
            
        db.session.add(items)
        db.session.commit()

        return items.to_dict(), 200
    
    elif request.method == 'DELETE':
        db.session.delete(items)
        db.session.commit()
        

@app.route("/collections/<int:id>", methods=['GET', 'DELETE', 'PATCH'])
def collections_by_id(id):
    collection = Collection.query.filter(Collection.id == id).first()

    if request.method == 'GET':
        return collection.to_dict(), 200
    
    elif request.method == 'PATCH':
        data = request.get_json()
        for field in data:
            try:
                setattr(collection, field, data.get(f'{field}'))
            except ValueError as e:
                return {'error': str(e)}, 400
            
        db.session.add(collection)
        db.session.commit()

        return collection.to_dict(), 200
    
    elif request.method == 'DELETE':
        db.session.delete(collection)
        db.session.commit()
    

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter(User.username == data['username']).first()
    
    if not user:
        return {'error': 'login failed'}, 401
    
    if not user.authenticate(data['password']):
        return {'error': 'login failed'}, 401
    
    session['user_id'] = user.id

    return user.to_dict(), 200

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    user = User.query.filter(User.username == data['username']).first()
    if user:
        return {'error': 'username already exists'}, 400
    
    new_user = User(
        username=data['username'],
        password=data['password']
    )

    db.session.add(new_user)
    db.session.commit()

    return new_user.to_dict(), 201

@app.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return {}, 204

@app.route('/check_session')
def check_session():
    user_id = session.get('user_id')

    if not user_id:
        return {'error': 'authorization failed'}, 401
    
    user = User.query.filter(User.id == user_id).first()
    if not user:
        return {'error': 'authorization failed'}, 401
    
    return user.to_dict(), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)