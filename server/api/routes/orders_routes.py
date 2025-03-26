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
    order = Order(
        id=str(uuid.uuid4()),
        customer_name=data['customer_name']
    )
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
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string'},
                        'customer_name': {'type': 'string'},
                        'created_at': {'type': 'string', 'format': 'date-time'}
                    }
                }
            }
        }
    }
})
def get_orders():
    orders = Order.query.all()
    return jsonify([o.deserialize() for o in orders]), 200
