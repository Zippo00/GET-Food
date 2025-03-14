from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys,os
from werkzeug.exceptions import UnsupportedMediaType, NotFound, Conflict, BadRequest

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32),nullable=False)
    price = db.Column(db.Float,nullable=False)
    describtion = db.Column(db.String(256),nullable=True)

    def deserialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "describtion": self.describtion
        }
    
    @staticmethod
    def json_schema():
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "price": {"type": "number"},
                "describtion": {"type": "string"}
            },
            "required": ["name", "price"]
        }
class ItemConverter:
    def to_python(self, item_id):
        db_item = Item.query.filter_by(name=item_id).first()
        if db_item is None:
            raise NotFound
        return db_item
        
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32),nullable=False)
    data = db.Column(db.LargeBinary,nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id",ondelete="CASCADE"),nullable=False)

    def deserialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "item_id": self.item_id
        }
    
    @staticmethod
    def json_schema():
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "item_id": {"type": "number"}
            },
            "required": ["name", "item_id"]
        }

class ImageConverter:
    def to_python(self, image_id):
        db_image = Image.query.filter_by(name=image_id).first()
        if db_image is None:
            raise NotFound
        return db_image

def populate_db():
    with app.app_context():
        db.create_all()
        csvfile = sys.argv[1]
        with open(csvfile, "r") as f:
            for line in f:
                print(line)
                line = line.rstrip("\n")
                itemdata, imagedata = line.split(";")
                name, price, describtion = itemdata.strip().split(",")
                item = Item(name=name, price=price, describtion=describtion)
                db.session.add(item)
                imagearray = imagedata.split(",")
                item_id = item.query.filter_by(name=name).first().id
                for i in range(0, len(imagearray) - 1, 2):
                    image = Image(name=imagearray[i], data=calculate_image_data(imagearray[i + 1]), item_id=item.id)
                    db.session.add(image)

                db.session.commit()
    return

def calculate_image_data(path):
    with open(path, "rb") as f:
        return f.read()
