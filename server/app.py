from flask import Flask
from flasgger import Swagger
from config import Config
from api.db import db
from api.routes.item_routes import item_bp
from api.routes.image_routes import image_bp
from api.routes.orders_routes import orders_bp
from api.routes.order_items_routes import order_items_bp
from api.routes.order_status_routes import order_status_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    #blueprints
    app.register_blueprint(item_bp)
    app.register_blueprint(image_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(order_items_bp)
    app.register_blueprint(order_status_bp)


    #Swagger initialization
    swagger = Swagger(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        """Welcome message
        ---
        responses:
          200:
            description: Welcome message
        """
        return {"message": "Welcome to the Food Ordering System API!"}, 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
