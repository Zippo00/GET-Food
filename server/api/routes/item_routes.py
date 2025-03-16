from flask import Blueprint, request, jsonify
from api.models.item import Item
from api.db import db
import uuid

item_bp = Blueprint("item", __name__, url_prefix="/items")

#Get All Items
@item_bp.route("/", methods=["GET"])
def get_items():
    items = Item.query.all()
    return jsonify([item.deserialize() for item in items]), 200

#Get Single Item by ID (UUID)..
@item_bp.route("/<string:item_id>", methods=["GET"])
def get_item(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item.deserialize()), 200
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400

#Create a New Item...
@item_bp.route("/", methods=["POST"])
def create_item():
    data = request.get_json()
    if "name" not in data or "price" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    #Check if item with the same name exists..
    existing_item = Item.query.filter_by(name=data["name"]).first()
    if existing_item:
        return jsonify({"error": "An item with this name already exists"}), 409  

    new_item = Item(name=data["name"], price=data["price"], description =data.get("description"))
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.deserialize()), 201


#Update an Item (UUID)..
@item_bp.route("/<string:item_id>", methods=["PUT"])
def update_item(item_id):
    try:
        item = Item.query.get(item_id)
        if not item:
            return jsonify({"error": "Item not found"}), 404

        data = request.get_json()
        item.name = data.get("name", item.name)
        item.price = data.get("price", item.price)
        item.description  = data.get("description ", item.description )

        db.session.commit()
        return jsonify(item.deserialize()), 200
    except ValueError:
        return jsonify({"error": "Invalid UUID format"}), 400

#Delete an Item (UUID)
@item_bp.route("/<string:item_id>", methods=["DELETE"])
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
