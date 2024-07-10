#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, User, Collection

fake = Faker()

def create_users():
    User.query.delete()
    
    users = []
    
    count = 1
    
    for i in range(20):
        user = User(
            username = f'Guest{count}',
            password = "pass"
        )
        count += 1
        users.append(user)
        
    db.session.add_all(users)
    db.session.commit()
    
def create_collections():
    Collection.query.delete()
    
    collections = []
    
    # count = 1
     
    for i in range(20):
        collection = Collection(
            title = fake.name(),
            user_id = 1,
        )
        collections.append(collection)
    
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
        