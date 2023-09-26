#!/usr/bin/env python3

from flask import Flask
from faker import Faker
from sqlalchemy import func

from models  import db, Restaurant, Pizza, RestaurantPizza
from app import app

with app.app_context():
    fake = Faker()


    for _ in range(10):
        restaurant = Restaurant(
            name=fake.unique.first_name(),  
            address=fake.address()
        )
        db.session.add(restaurant)

    for _ in range(10):  
        pizza = Pizza(
            name=fake.unique.word(),  
            ingredients=fake.sentence()
        )
        db.session.add(pizza)

    for _ in range(20):  
        restaurant = Restaurant.query.order_by(func.random()).first() 
        pizza = Pizza.query.order_by(func.random()).first() 

        restaurant_pizza = RestaurantPizza(
            name=fake.unique.company(),
            price=fake.random_int(min=5, max=20), 
            restaurant=restaurant
        )
        db.session.add(restaurant_pizza)

    db.session.commit()

print("Database seeded successfully with Faker data!")

