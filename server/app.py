from flask import Flask
from config import Config
from api.db import db
from api.routes.item_routes import item_bp
from api.routes.image_routes import image_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    app.register_blueprint(item_bp)
    app.register_blueprint(image_bp)

    with app.app_context():
        db.create_all()

    @app.route("/") 
    def home():
        return {"message": "Welcome to the Food Ordering System API!"}, 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
