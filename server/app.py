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
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Enable foreign key constraints in SQLite	
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

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


if __name__ == "__main__":
#     app = create_app()
    app.run(debug=True, host="0.0.0.0")
