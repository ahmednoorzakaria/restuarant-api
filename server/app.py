from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant,  Pizza,RestaurantPizza,RestaurantSchema,PizzaSchema
from marshmallow import Schema, fields

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

api.add_resource(RestaurantAPIInfo, '/')

class Restaurants(Resource):

    def get(self):
        restaurants = Restaurant.query.all()
        restaurant_list = []
        for rest in restaurants:
            rest_dict = {
                "name":rest.name,
                "address":rest.address
            }
            restaurant_list.append(rest_dict)
        restaurant_schema = RestaurantSchema(many=True)
        serialized_restaurants = restaurant_schema.dump(restaurants)
        restaurant_dict = [rest.to_dict() for rest in restaurants ]
        
        print(restaurant_list)
        return make_response(jsonify(restaurant_list), 200)

    def post(self):
        data = request.get_json()

        if 'name' not in data or 'address' not in data:
            return make_response(jsonify({'message': 'Missing required fields'}), 400)

        if data['name'] == '':
            return make_response(jsonify({'message': 'Invalid name'}), 400)

        new_restaurant = Restaurant(
            name=data['name'],
            address=data['address']
        )
        print (data)
        db.session.add(new_restaurant)
        db.session.commit()

        restaurant_schema = RestaurantSchema()
        serialized_restaurant = restaurant_schema.dump(new_restaurant)

        return make_response(jsonify(serialized_restaurant), 201)

#api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):

    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            restaurant_schema = RestaurantSchema()
            serialized_restaurant = restaurant_schema.dump(restaurant)
            return make_response(jsonify(serialized_restaurant), 200)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)

    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
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
        pizzas = Pizza.query.all()
        pizza_schema = PizzaSchema(many=True)
        serialized_pizzas = pizza_schema.dump(pizzas)
        return make_response(jsonify(serialized_pizzas), 200)

api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):

    def post(self):
        data = request.get_json()

        new_restaurant_pizza = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )
        print(new_restaurant_pizza)

        db.session.add(new_restaurant_pizza)
        db.session.commit()

        new_restaurant_pizza_dict = new_restaurant_pizza.to_dict()
        response = make_response(jsonify(new_restaurant_pizza_dict),201)
        return response

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')


if __name__ == '__main__':
    app.run(port=5555, debug=True)