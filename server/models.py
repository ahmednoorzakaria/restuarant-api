from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship

from marshmallow import Schema, fields


db = SQLAlchemy()

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
    serialize_rules = ("-restaurant_pizzas.pizza")

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurant_pizzas = relationship('RestaurantPizza', backref='pizza')

    def __repr__(self):
        return f'<Pizza {self.name}, Ingredients: {self.ingredients}>'

class PizzaSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    ingredients = fields.String(required=True)

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
    serialize_rules = ("-restaurant_pizzas.restaurant")
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String)

    restaurant_pizzas = relationship('RestaurantPizza', backref='restaurant')


    def __repr__(self):
        return f'<Restaurant {self.name}, Address: {self.address}>'

class RestaurantSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
    address = fields.String(required=False)
    pizzas = fields.List(fields.Nested(PizzaSchema))

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'
    
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    #pizza = relationship('Pizza', back_populates='restaurant_pizzas')
    #restaurant = relationship('Restaurant', back_populates='restaurant_pizzas')
    serialize_rules = ("-pizza.restaurant_pizzas","-restaurant.restaurant_pizzas")

    def __repr__(self):
        return f'<RestaurantPizza , Price: {self.price}>'
