import uuid
from api.db import db

class Order(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    customer_name = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime,nullable=False, default=db.func.now())

    order_items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    order_status = db.relationship("OrderStatus", back_populates="order", cascade="all, delete-orphan")

    def deserialize(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "created_at": self.created_at.isoformat()
        }

    @staticmethod
    def json_schema():
        return {
            "type": "object",
            "properties": {
                "customer_name": {"type": "string", "minLength": 1}
            },
            "required": ["customer_name"]
        }
