import uuid
from api.db import db

class OrderStatus(db.Model):
    __tablename__ = 'order_status'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    order_id = db.Column(db.String(36), db.ForeignKey("order.id", ondelete="CASCADE"), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    updated_at = db.Column(db.DateTime,nullable=False, default=db.func.now())

    order = db.relationship("Order", back_populates="order_status")

    def deserialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "status": self.status,
            "updated_at": self.updated_at.isoformat()
        }

    @staticmethod
    def json_schema():
        return {
            "type": "object",
            "properties": {
                "order_id": {"type": "string"},
                "status": {"type": "string"}
            },
            "required": ["order_id", "status"]
        }
