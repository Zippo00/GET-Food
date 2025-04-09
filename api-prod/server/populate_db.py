import sys
import os
from sqlalchemy.exc import IntegrityError

from app import app
from api.db import db
from api.models.item import Item
from api.models.image import Image
from api.utils.file_utils import calculate_image_data


def populate_db(csvfile): 
    csvdirectory = os.path.dirname(csvfile)
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    with open(csvfile, "r") as f:
            for line in f:
                line = line.strip()
                itemdata, imagedata = line.split(";")
                name, price, description = itemdata.strip().split(",")

                item = Item(name=name, price=float(price), description =description )
                db.session.add(item)
                db.session.commit()

                item_id = item.id
                imagearray = imagedata.split(",")

                for i in range(0, len(imagearray) - 1, 2):
                    image = Image(name=imagearray[i], data=calculate_image_data(os.path.join(csvdirectory,imagearray[i+1])), item_id=item_id)
                    db.session.add(image)

                db.session.commit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python populate_db.py <csv_file>")
        sys.exit(1)
    try:
        populate_db(sys.argv[1])
    except IntegrityError as e:
        print("Duplicate entry in the csv file.")
        sys.exit(1)