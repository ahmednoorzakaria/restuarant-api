#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from sqlalchemy.exc import IntegrityError

from models import db, Restaurant, RestaurantSchema, Pizza, PizzaSchema, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
class RestaurantAPIInfo(Resource):

    def get(self):
        info = {
            "name": "Restaurant API",
            "description": "An API for managing restaurants and pizzas",
            "version": "1.0",
        }
        return make_response(jsonify(info), 200)

# Add the RestaurantAPIInfo resource to the API
api.add_resource(RestaurantAPIInfo, '/')

class Restaurants(Resource):

    def get(self):
        restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()]
        return make_response(jsonify(restaurants), 200)

    def post(self):
        data = request.get_json()

        new_restaurant = Restaurant(
            name=data['name'],
            address=data['address']
        )

        db.session.add(new_restaurant)
        db.session.commit()

        return make_response(new_restaurant.to_dict(), 201)

api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):

    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            restaurant_dict = restaurant.to_dict()
            # Include associated pizzas
            restaurant_dict['pizzas'] = [pizza.to_dict() for pizza in restaurant.pizzas]
            return make_response(jsonify(restaurant_dict), 200)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)

    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            # Delete associated restaurant pizzas
            for restaurant_pizza in restaurant.restaurant_pizzas:
                db.session.delete(restaurant_pizza)
            db.session.delete(restaurant)
            db.session.commit()
            return make_response('', 204)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)

api.add_resource(RestaurantByID, '/restaurants/<int:id>')

class Pizzas(Resource):

    def get(self):
        pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]
        return make_response(jsonify(pizzas), 200)

api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):

    def post(self):
        data = request.get_json()

        new_restaurant_pizza = RestaurantPizza(
            name=data['name'],
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )

        db.session.add(new_restaurant_pizza)
        db.session.commit()

        # Return details of the associated pizza
        pizza = Pizza.query.get(data['pizza_id'])
        return make_response(pizza.to_dict(), 200)

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

