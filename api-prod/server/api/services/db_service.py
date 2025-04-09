from api.db import db

def save_to_db(instance):
    db.session.add(instance)
    db.session.commit()
