from flask import Blueprint, request, jsonify

order_blueprint = Blueprint('order', __name__)

ORDERS = []  

@order_blueprint.route('/', methods=['POST'])
def place_order():
    data = request.json
    if not data or "items" not in data:
        return jsonify({"error": "Invalid order data"}), 400

    order_id = len(ORDERS) + 1
    order = {"id": order_id, "items": data["items"], "status": "pending"}
    ORDERS.append(order)

    return jsonify({"message": "Order placed successfully", "order": order}), 201

@order_blueprint.route('/', methods=['GET'])
def get_orders():
    return jsonify(ORDERS)
