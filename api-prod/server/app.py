import uvicorn
from flask import Flask
from flasgger import Swagger
from config import Config
from api.db import db
from api.routes.item_routes import item_bp
from api.routes.image_routes import image_bp
from api.routes.orders_routes import orders_bp
from api.routes.order_items_routes import order_items_bp
from api.routes.order_status_routes import order_status_bp
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Enable CORS for the entire app
CORS(app)

#blueprints
app.register_blueprint(item_bp)
app.register_blueprint(image_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(order_items_bp)
app.register_blueprint(order_status_bp)

with app.app_context():
    db.create_all()

#Swagger initialization
swagger = Swagger(app)

@app.route("/")
def home():
    """
    Welcome message
    ---
    responses:
      200:
        description: Welcome message
    """
    return {"message": "Welcome to the Food Ordering System API!"}, 200


def init_app():
    """
    Initializes the Flask app.

    Returns:
        app (Flask): Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Enable CORS for the entire app
    CORS(app)

    #blueprints
    app.register_blueprint(item_bp)
    app.register_blueprint(image_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(order_items_bp)
    app.register_blueprint(order_status_bp)
    return app

def create_db(app):
    """
    Creates the initial database.
    """
    with app.app_context():
        db.create_all()


def create_app():
    # Initialize app
    app = init_app()

    #Swagger initialization
    swagger = Swagger(app)

    create_db(app)

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
#     app = create_app()
    app.run(host="0.0.0.0", debug=True)
    #uvicorn.run(app,
    #            host="0.0.0.0",
    #            port=5000,
    #            debug=True
    #            )
