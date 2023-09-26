# Restaurant API

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
  - [Example Requests](#example-requests)
  - [Authentication](#authentication)
- [Data Models](#data-models)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Welcome to the Restaurant API, a powerful tool for managing restaurant and pizza data. This API allows you to perform various operations related to restaurants, pizzas, and their associations.

## Features

- View a list of restaurants and their details.
- Add new restaurants to the database.
- Retrieve information about individual restaurants by ID.
- Delete restaurants by ID, including associated data.
- Browse a catalog of pizzas, each with ingredients and details.
- Create and manage restaurant-pizza relationships.

## Getting Started

### Prerequisites

To run the Restaurant API, you'll need the following software:

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Other dependencies (see `requirements.txt`)

### Installation

1. Clone the repository to your local machine:

   ```shell
   git clone https://github.com/yourusername/restaurant-api.git
2. Create a virtual environment and activate it:

python3 -m venv venv
source venv/bin/activate
3. Install the required dependencies:

pip install -r requirements.txt
4. Run the API:

python app.py
## Usage
### API Endpoints
#### /restaurants
- GET: Retrieve a list of all restaurants.
- POST: Add a new restaurant to the database.
### /restaurants/<int:id>
- GET: Retrieve details of a specific restaurant by ID.
- DELETE: Delete a restaurant and its associated data by ID.
### /pizzas
- GET: Retrieve a list of all pizzas.
### /restaurant_pizzas
- POST: Create a new restaurant-pizza relationship.
#### Example Requests
Fetch all restaurants:


curl -X GET http://localhost:5555/restaurants
Add a new restaurant:


curl -X POST -H "Content-Type: application/json" -d '{"name": "New Restaurant", "address": "123 Main St"}' http://localhost:5555/restaurants
Retrieve details of a restaurant by ID:


curl -X GET http://localhost:5555/restaurants/1
Delete a restaurant by ID:

curl -X DELETE http://localhost:5555/restaurants/1
Authentication
(Optional: Describe any authentication mechanisms here, if applicable.)

## Data Models
- Restaurant: Represents a restaurant with attributes like name and address.
- Pizza: Represents a pizza with attributes like name and ingredients.
- RestaurantPizza: Represents the relationship between restaurants and pizzas, including the price.
## Contributing
We welcome contributions! Feel free to open issues and pull requests to help us improve this API.

License
This project is licensed under the MIT License.
