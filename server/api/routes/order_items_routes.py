from flask import Blueprint, request, jsonify
from api.db import db
from api.models.order_item import OrderItem
import uuid
from flasgger import swag_from

order_items_bp = Blueprint('order_items', __name__, url_prefix='/order-items')


@order_items_bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Order Items'],
    'summary': 'Add item to an order',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': OrderItem.json_schema()
        }
    ],
    'responses': {
        201: {
            'description': 'Item added to order successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string'},
                    'order_id': {'type': 'string'},
                    'item_id': {'type': 'string'},
                    'quantity': {'type': 'integer'}
                }
            }
        }
    }
})
def add_item_to_order():
    data = request.get_json()
    order_item = OrderItem(
        id=str(uuid.uuid4()),
        order_id=data['order_id'],
        item_id=data['item_id'],
        quantity=data['quantity']
    )
    db.session.add(order_item)
    db.session.commit()
    return jsonify(order_item.deserialize()), 201


@order_items_bp.route('/<order_id>', methods=['GET'])
@swag_from({
    'tags': ['Order Items'],
    'summary': 'Get all items for a specific order',
    'parameters': [
        {
            'name': 'order_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the order'
        }
    ],
    'responses': {
        200: {
            'description': 'List of items for the given order',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string'},
                        'order_id': {'type': 'string'},
                        'item_id': {'type': 'string'},
                        'quantity': {'type': 'integer'}
                    }
                }
            }
        }
    }
})
def get_items_by_order(order_id):
    items = OrderItem.query.filter_by(order_id=order_id).all()
    return jsonify([item.deserialize() for item in items]), 200
