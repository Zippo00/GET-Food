from flask import Blueprint, jsonify

category_blueprint = Blueprint('category', __name__)

CATEGORIES = ["Pizza", "Burgers"]

@category_blueprint.route('/', methods=['GET'])
def get_categories():
    return jsonify(CATEGORIES)
