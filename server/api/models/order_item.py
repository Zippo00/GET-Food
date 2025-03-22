import uuid
from api.db import db

class OrderItem(db.Model):
    __tablename__ = 'orderitem'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    order_id = db.Column(db.String(36), db.ForeignKey("order.id", ondelete="CASCADE"), nullable=False)
    item_id = db.Column(db.String(36), db.ForeignKey("item.id", ondelete="CASCADE"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def deserialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "item_id": self.item_id,
            "quantity": self.quantity
        }

    @staticmethod
    def json_schema():
        return {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"},
                "item_id": {"type": "string"},
                "quantity": {"type": "integer", "minimum": 1}
            },
            "required": ["order_id", "item_id", "quantity"]
        }
