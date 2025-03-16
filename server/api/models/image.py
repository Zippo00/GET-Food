import uuid
from api.db import db

class Image(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    item_id = db.Column(db.String(36), db.ForeignKey("item.id", ondelete="CASCADE"), nullable=False)

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
                "item_id": {"type": "string"} 
            },
            "required": ["name", "item_id"]
        }
