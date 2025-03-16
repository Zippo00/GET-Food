import sys
from api import create_app
from api.db import db
from api.models.item import Item
from api.models.image import Image
from api.utils.file_utils import calculate_image_data

app = create_app()

def populate_db(csvfile):
    with app.app_context():
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
                    image = Image(name=imagearray[i], data=calculate_image_data(imagearray[i + 1]), item_id=item_id)
                    db.session.add(image)

                db.session.commit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python populate_db.py <csv_file>")
        sys.exit(1)

    populate_db(sys.argv[1])
