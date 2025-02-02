from flask import Blueprint, jsonify

menu_blueprint = Blueprint('menu', __name__)

MENU_ITEMS = [
    {"id": 1, "name": "Margherita Pizza", "category": "Pizza", "price": 12.99},
    {"id": 2, "name": "Cheeseburger", "category": "Burgers", "price": 9.99},
    {"id": 3, "name": "Caesar Salad", "category": "Salads", "price": 8.49},
    {"id": 4, "name": "Chocolate Cake", "category": "Desserts", "price": 6.99},
]

@menu_blueprint.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(MENU_ITEMS)
