from flask import Blueprint, request, jsonify
from api.models.image import Image
from api.models.item import Item
from api.db import db
import base64

image_bp = Blueprint("image", __name__, url_prefix="/images")

#Get All Images
@image_bp.route("/", methods=["GET"])
def get_images():
    images = Image.query.all()
    return jsonify([image.deserialize() for image in images]), 200

#Get Single Image by ID (UUID)
@image_bp.route("/<string:image_id>", methods=["GET"])
def get_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({"error": "Image not found"}), 404

    return jsonify(image.deserialize()), 200

#Upload Image (Base64 Encoded, UUID Item ID)
@image_bp.route("/", methods=["POST"])
def upload_image():
    data = request.get_json()
    if "name" not in data or "item_id" not in data or "data" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    item = Item.query.get(data["item_id"])
    if not item:
        return jsonify({"error": "Item does not exist"}), 404

    try:
        image_data = base64.b64decode(data["data"])  # Decoding to Base64....
    except Exception:
        return jsonify({"error": "Invalid Base64 image data"}), 400

    new_image = Image(
        name=data["name"],
        data=image_data,
        item_id=data["item_id"]
    )
    db.session.add(new_image)
    db.session.commit()
    
    return jsonify(new_image.deserialize()), 201

#Delete Image by (UUID)
@image_bp.route("/<string:image_id>", methods=["DELETE"])
def delete_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        return jsonify({"error": "Image not found"}), 404

    db.session.delete(image)
    db.session.commit()
    return jsonify({"message": "Image deleted"}), 200
