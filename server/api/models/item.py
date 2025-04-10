import uuid
from api.db import db

class Item(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(32), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(256), nullable=True)  

    images = db.relationship("Image", back_populates="item", cascade="all, delete-orphan")
    order_items = db.relationship("OrderItem", back_populates="item", cascade="all, delete-orphan")

    def deserialize(self):
        """Convert database object to JSON format."""
        return {
            "id": str(self.id),  
            "name": self.name,
            "price": self.price,
            "description": self.description or ""  
        }

    @staticmethod
    def json_schema():
        """Return JSON Schema for validation."""
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "maxLength": 32, "minLength": 1},
                "price": {"type": "number", "minimum": 0},  
                "description": {"type": "string", "maxLength": 256}
            },
            "required": ["name", "price"]
        }
