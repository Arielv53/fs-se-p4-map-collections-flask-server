#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker
from app import app
from models import db, User, Collection, CollectionItem

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
        
    for user_id in range(1, 21):
        for i in range(20):
            collection = Collection(
                title = fake.unique.word(),
                group = fake.unique.word(),
                user_id = user_id,
            )
            collections.append(collection)
    if collections:
        db.session.add_all(collections)
        db.session.commit()
    

def create_items():
    CollectionItem.query.delete()
    
    items = []
    
    for collection_id in range(1, 401):
        for item in range(20):
            collection_item = CollectionItem(
                group = fake.word(),
                name = fake.word(),
                address = fake.street_address(),
                comment = fake.paragraph(),
                review = fake.paragraph(),
                collection_id = collection_id,
            )
            items.append(collection_item)
        db.session.add_all(items)
        db.session.commit()

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
        