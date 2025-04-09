from flask import Blueprint, request, jsonify
from api.models.order_status import OrderStatus
from api.db import db
import uuid
from flasgger import swag_from

order_status_bp = Blueprint('order_status', __name__, url_prefix='/order-status')


@order_status_bp.route('/', methods=['POST'])
@swag_from({
    'tags': ['Order Status'],
    'summary': 'Update the status of an order',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': OrderStatus.json_schema()
        }
    ],
    'responses': {
        201: {
            'description': 'Order status created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string'},
                    'order_id': {'type': 'string'},
                    'status': {'type': 'string'},
                    'updated_at': {'type': 'string', 'format': 'date-time'}
                }
            }
        },
        400: {
            'description': 'Missing required fields'
        }
    }
})
def update_status():
    data = request.get_json()

    if not data or 'order_id' not in data or 'status' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    status = OrderStatus(
        id=str(uuid.uuid4()),
        order_id=data['order_id'],
        status=data['status']
    )
    db.session.add(status)
    db.session.commit()
    return jsonify(status.deserialize()), 201

@order_status_bp.route('/<order_id>', methods=['GET'])
@swag_from({
    'tags': ['Order Status'],
    'summary': 'Get status history for an order',
    'parameters': [
        {
            'name': 'order_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the order to fetch status history for'
        }
    ],
    'responses': {
        200: {
            'description': 'List of status updates for the given order',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string'},
                        'order_id': {'type': 'string'},
                        'status': {'type': 'string'},
                        'updated_at': {'type': 'string', 'format': 'date-time'}
                    }
                }
            }
        }
    }
})
def get_status_history(order_id):
    statuses = OrderStatus.query.filter_by(order_id=order_id).order_by(OrderStatus.updated_at.asc()).all()
    return jsonify([s.deserialize() for s in statuses]), 200
