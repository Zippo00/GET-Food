from flask import Blueprint, request, jsonify
from flasgger import swag_from
from api.models.item import Item
from api.db import db
import uuid

item_bp = Blueprint("item", __name__, url_prefix="/items")

# Get All Items
@item_bp.route("/", methods=["GET"])
@swag_from({
    "responses": {
        200: {
            "description": "Retrieve all items",
            "examples": {
                "application/json": [
                    {"id": "uuid", "name": "Pizza", "price": 12.5, "description": "Cheese Pizza"},
                    {"id": "uuid", "name": "Burger", "price": 8.99, "description": "Beef Burger"}
                ]
            }
        }
    }
})
def get_items():
    items = Item.query.all()
    return jsonify([item.deserialize() for item in items]), 200

# Get Single Item by ID (UUID)
@item_bp.route("/<string:item_id>", methods=["GET"])
@swag_from({
    "parameters": [
        {
            "name": "item_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Item UUID"
        }
    ],
    "responses": {
        200: {
            "description": "Item details",
            "examples": {
                "application/json": {
                    "id": "uuid",
                    "name": "Pizza",
                    "price": 12.5,
                    "description": "Cheese Pizza"
                }
            }
        },
        404: {
            "description": "Item not found"
        },
        400: {
            "description": "Invalid UUID format"
        }
    }
})
def get_item(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item.deserialize()), 200
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400

# Create a New Item
@item_bp.route("/", methods=["POST"])
@swag_from({
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "schema": Item.json_schema(),
            "required": True,
            "description": "Item data to create"
        }
    ],
    "responses": {
        201: {
            "description": "Item created successfully"
        },
        400: {
            "description": "Missing required fields"
        },
        409: {
            "description": "Item with this name already exists"
        }
    }
})
def create_item():
    data = request.get_json()
    if "name" not in data or "price" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    existing_item = Item.query.filter_by(name=data["name"]).first()
    if existing_item:
        return jsonify({"error": "An item with this name already exists"}), 409  

    new_item = Item(name=data["name"], price=data["price"], description=data.get("description"))
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.deserialize()), 201

# Update an Item (UUID)
@item_bp.route("/<string:item_id>", methods=["PUT"])
@swag_from({
    "parameters": [
        {
            "name": "item_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Item UUID"
        },
        {
            "name": "body",
            "in": "body",
            "schema": Item.json_schema(),
            "required": True,
            "description": "Updated item data"
        }
    ],
    "responses": {
        200: {
            "description": "Item updated successfully"
        },
        400: {
            "description": "Invalid UUID format"
        },
        404: {
            "description": "Item not found"
        }
    }
})
def update_item(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404

        data = request.get_json()
        item.name = data.get("name", item.name)
        item.price = data.get("price", item.price)
        item.description = data.get("description", item.description)

        db.session.commit()
        return jsonify(item.deserialize()), 200
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400

# Delete an Item (UUID)
@item_bp.route("/<string:item_id>", methods=["DELETE"])
@swag_from({
    "parameters": [
        {
            "name": "item_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Item UUID"
        }
    ],
    "responses": {
        200: {
            "description": "Item deleted successfully"
        },
        404: {
            "description": "Item not found"
        },
        400: {
            "description": "Invalid UUID format"
        }
    }
})
def delete_item(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted"}), 200
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400
