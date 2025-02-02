from flask import Blueprint, jsonify

menu_blueprint = Blueprint('menu', __name__)

MENU_ITEMS = [
    {"id": 1, "name": "Margherita Pizza", "category": "Pizza", "price": 12.99},
    {"id": 2, "name": "Cheeseburger", "category": "Burgers", "price": 9.99},
]

@menu_blueprint.route('/', methods=['GET'])
def get_menu():
    return jsonify(MENU_ITEMS)

@menu_blueprint.route('/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    item = next((item for item in MENU_ITEMS if item["id"] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404
