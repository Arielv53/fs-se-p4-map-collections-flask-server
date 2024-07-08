from models import db, Collection, User, User_collection
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Phase 4 Project</h1>"

@app.route("/collections", methods=['GET', 'POST'])
def collections():
    if request.method == 'GET':
        collections = Collection.query.all()
        return [collection.to_dict() for collection in collections], 200
    
    elif request.method == 'POST':
        data = request.get_json()

        try:
            new_collection = Collection(
                genre=data.get('genre'), 
                title=data.get('title'), 
                description=data.get('description'), 
                reviews=data.get('reviews'), 
                user_id=data.get('user_id')
            )
        except ValueError as e:
            return {'error': str(e)}, 400
        
        db.session.add(new_collection)
        db.session.commit()

        return new_collection.to_dict(), 201
        

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

        return {}, 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)