from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Item(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    price = db.Column(db.Float)
    describtion = db.Column(db.String(256))
    
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    data = db.Column(db.LargeBinary)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"),on_delete="CASCADE")

def populate_db():
    return