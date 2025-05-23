from flask import Blueprint, request, jsonify
from api.models.order import Order
from api.db import db
import uuid
from flasgger import swag_from

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Orders'],
    'summary': 'Create a new order',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': Order.json_schema()
        }
    ],
    'responses': {
        201: {
            'description': 'Order created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string'},
                    'customer_name': {'type': 'string'},
                    'created_at': {'type': 'string', 'format': 'date-time'}
                }
            }
        }
    }
})
def create_order():
    data = request.get_json()
    order = Order(id=str(uuid.uuid4()), customer_name=data['customer_name'])
    db.session.add(order)
    db.session.commit()
    return jsonify(order.deserialize()), 201


@orders_bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Orders'],
    'summary': 'Get all orders',
    'responses': {
        200: {
            'description': 'List of all orders',
            'schema': {
                'type': 'array',
                'items': Order.json_schema()
            }
        }
    }
})
def get_orders():
    orders = Order.query.all()
    return jsonify([o.deserialize() for o in orders]), 200


@orders_bp.route('/<string:order_id>', methods=['GET'])
@swag_from({
    'tags': ['Orders'],
    'summary': 'Get order by ID',
    'parameters': [
        {
            'name': 'order_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'UUID of the order'
        }
    ],
    'responses': {
        200: {
            'description': 'Order data',
            'schema': Order.json_schema()
        },
        404: {
            'description': 'Order not found'
        }
    }
})
def get_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify(order.deserialize()), 200


@orders_bp.route('/<string:order_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Orders'],
    'summary': 'Delete order by ID',
    'parameters': [
        {
            'name': 'order_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'UUID of the order'
        }
    ],
    'responses': {
        200: {'description': 'Order deleted'},
        404: {'description': 'Order not found'},
        400: {'description': 'Invalid UUID format'}
    }
})
def delete_order(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted"}), 200
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400
