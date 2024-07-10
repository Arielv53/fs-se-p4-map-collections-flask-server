#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, User, Collection

fake = Faker()

def create_users():
    User.query.delete()
    
    users = []
    
    for i in range(20):
        user = User(
            username = fake.unique.first_name(),
            password = "password"
        )
        users.append(user)
        
    db.session.add_all(users)
    db.session.commit()
    
def create_collections():
    Collection.query.delete()
    
    collections = []
        
    for user_id in range(1, 20):
        for i in range(20):
            collection = Collection(
                title = fake.unique.word(),
                user_id = user_id,
            )
            collections.append(collection)
    if collections:
        db.session.add_all(collections)
        db.session.commit()
    

def create_items():
    pass

def seed_database():
    create_users()
    create_collections()
    create_items()

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!
        seed_database()
        