from flask import Blueprint
from .routes.menu_routes import menu_blueprint
from .routes.category_routes import category_blueprint
from .routes.order_routes import order_blueprint

api_blueprint = Blueprint('api', __name__)

api_blueprint.register_blueprint(menu_blueprint, url_prefix='/menu')
api_blueprint.register_blueprint(category_blueprint, url_prefix='/categories')
api_blueprint.register_blueprint(order_blueprint, url_prefix='/order')
