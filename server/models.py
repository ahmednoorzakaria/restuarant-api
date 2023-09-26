from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema , fields
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship


db = SQLAlchemy()

class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurant_pizzas = relationship('RestaurantPizza', back_populates='pizza')


    def __repr__(self):
        return f'<Pizza {self.name}, Ingredients: {self.ingredients}>'

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String)

    restaurant_pizzas = relationship('RestaurantPizza', back_populates='restaurant')


    def __repr__(self):
        return f'<Restaurant {self.name}, Address: {self.address}>'

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    pizza = relationship('Pizza', back_populates='restaurant_pizzas')
    restaurant = relationship('Restaurant', back_populates='restaurant_pizzas')

    def __repr__(self):
        return f'<RestaurantPizza {self.name}, Price: {self.price}>'
class PizzaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pizza

    restaurants = fields.Nested('RestaurantSchema', many=True)


class RestaurantSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Restaurant

    pizzas = fields.Nested('PizzaSchema', many=True)


class RestaurantPizzaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RestaurantPizza
