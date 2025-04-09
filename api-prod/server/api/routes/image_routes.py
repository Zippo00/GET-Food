from flask import Blueprint, request, jsonify
from flasgger import swag_from
from api.models.image import Image
from api.models.item import Item
from api.db import db
import base64
import binascii

image_bp = Blueprint("image", __name__, url_prefix="/images")

@image_bp.route("/", methods=["GET"])
@swag_from({
    "responses": {
        200: {
            "description": "Retrieve all images",
            "examples": {
                "application/json": [
                    {"id": "uuid", "name": "Pizza Image", "item_id": "uuid"},
                    {"id": "uuid", "name": "Burger Image", "item_id": "uuid"}
                ]
            }
        }
    }
})
def get_images():
    images = Image.query.all()
    return jsonify([image.deserialize(include_data=False) for image in images]), 200

@image_bp.route("/<string:image_id>", methods=["GET"])
@swag_from({
    "parameters": [
        {
            "name": "image_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Image UUID"
        }
    ],
    "responses": {
        200: {
            "description": "Image details",
            "examples": {
                "application/json": {
                    "id": "uuid",
                    "name": "Pizza Image",
                    "item_id": "uuid",
                    "data": "Base64 encoded data"
                }
            }
        },
        404: {
            "description": "Image not found"
        }
    }
})
def get_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({"error": "Image not found"}), 404

    return jsonify(image.deserialize(include_data=True)), 200

@image_bp.route("/", methods=["POST"])
@swag_from({
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "item_id": {"type": "string"},
                    "data": {"type": "string", "description": "Base64 encoded image"}
                },
                "required": ["name", "item_id", "data"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Image uploaded successfully"
        },
        400: {
            "description": "Missing required fields or Invalid Base64 image data"
        },
        404: {
            "description": "Item does not exist"
        }
    }
})
def upload_image():
    data = request.get_json()
    if "name" not in data or "item_id" not in data or "data" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    item = Item.query.get(data["item_id"])
    if not item:
        return jsonify({"error": "Item does not exist"}), 404

    try:
        image_data = base64.b64decode(data["data"])
    except binascii.Error:
        return jsonify({"error": "Invalid Base64 image data"}), 400

    new_image = Image(
        name=data["name"],
        data=image_data,
        item_id=data["item_id"]
    )
    db.session.add(new_image)
    db.session.commit()
    
    return jsonify(new_image.deserialize(include_data=True)), 201

@image_bp.route("/<string:image_id>", methods=["DELETE"])
@swag_from({
    "parameters": [
        {
            "name": "image_id",
            "in": "path",
            "type": "string",
            "required": True,
            "description": "Image UUID"
        }
    ],
    "responses": {
        200: {
            "description": "Image deleted successfully"
        },
        404: {
            "description": "Image not found"
        }
    }
})
def delete_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({"error": "Image not found"}), 404

    db.session.delete(image)
    db.session.commit()
    return jsonify({"message": "Image deleted"}), 200
