"""
Unit tests for API.
"""
import pytest
from app import app

test_img_base64 = open(r"template_image_base64.txt","r")
print(f"test_img_base64:\n{test_img_base64}\n")

@pytest.fixture
def client():
    """
    Provides a test client.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# DEFAULT API FUNCTIONALITIES

def test_add_image(client):
    """
    Test adding an image
    """
    response = client.post('/images', json={"data": test_img_base64, "item_id": "1", "name": "test"})

    assert response.status_code == 201 # Should work with test_img_base64 data ... ?

def test_add_image_missing_field(client):
    """
    Test adding an image with a missing field.
    """
    response = client.post('/images', json={"data": test_img_base64, "name": "test"})

    assert response.status_code == 400

def test_add_image_invalid_data(client):
    """
    Test adding an image with invalid image data.
    """
    response = client.post('/images', json={"data": "test_invalid_data", "item_id": "1", "name": "test"})

    assert response.status_code == 400

def test_delete_image(client):
    """
    Test deleting an added image.
    """
    # Add an image to db
    client.post('/images', json={"data": test_img_base64, "item_id": "1", "name": "test"})
    # Attempt to remove it
    response = client.delete('/images/1')

    assert response.status_code == 200

def test_delete_image_not_found(client):
    """
    Test deleting a non-existent image.
    """
    # Attempt to remove it
    response = client.delete('/images/108723')

    assert response.status_code == 404

def test_get_images(client):
    """
    Test retrieving all images. /images/
    """
    # Add an image to db
    client.post('/images', json={"data": test_img_base64, "item_id": "1", "name": "test"})
    # Retrieve the added image
    response = client.get('/images/')

    assert response.status_code == 200
    assert response.json[0]["name"] == "test" # TODO: is syntax correct here?

def test_get_images_empty_db(client):
    """
    Test retrieving all images from an empty db.
    """
    response = client.get('/images/')

    assert response.status_code == 200

def test_get_specific_image(client):
    """
    Test retrieving a specific image.
    """
    # Add an image to db
    client.post('/images', json={"data": test_img_base64, "item_id": "1", "name": "test"})
    # Retrieve it
    response = client.get('/images/1')

    assert response.status_code == 200
    assert response.json["data"] == test_img_base64

def test_get_specific_image_not_found(client):
    """
    Test retrieving a non-existent image
    """
    response = client.get('/images/1001')

    assert response.status_code == 404

def test_get_items(client):
    """
    Test retrieving all items.
    """
    # Post an item
    client.post('/items/', json={"description": "test", "name": "test", "price": 1})
    # Get items
    response = client.get('/items/')

    assert response.status_code == 200
    assert response.json[0]["description"] == "test"

def test_get_items_empty(client):
    """
    Test retrieving all items from an empty db.
    """
    # Get items
    response = client.get('/items/')

    assert response.status_code == 200
    

def test_post_items(client):
    """
    Test posting an item.
    """
    # Post an item
    response = client.post('/items/', json={"description": "test", "name": "test", "price": 1})

    assert response.status_code == 201

def test_post_items_missing_field(client):
    """
    Test posting an item with a missing field.
    """
    # Post an item
    response = client.post('/items/', json={"description": "test", "name": "test"})

    assert response.status_code == 400

def test_post_duplicate_item(client):
    """est posting a duplicate item
    """
    # Post an item
    client.post('/items/', json={"description": "test", "name": "test", "price": 1})
    # Post it again
    response = client.post('/items/', json={"description": "test", "name": "test", "price": 1})

    assert response.status_code == 409

def test_delete_item(client):
    """
    Test deleting an item.
    """
    #TODO: How does the API assign UUIDs, and will they start from 1 or 0 for each individual unit test or will the id keep increasing?
    pass

def test_delete_item_invalid_uuid(client):
    """
    Test deleting an item with invalid uuid
    """
    pass

def test_delete_item_not_found(client):
    """
    """
    pass

def test_get_specific_item(client):
    """
    """
    pass

def test_get_specific_item_invalid_uuid(client):
    """
    """
    pass

def test_get_specific_item_not_found(client):
    """
    """
    pass

def test_put_specific_item(client):
    """
    """
    pass

def test_put_specific_item_invalid_uuid(client):
    """
    """
    pass

def test_put_specific_item_not_found(client):
    """
    """
    pass

# ORDER ITEMS FUNCTIONALITITES

def test_order_item_post(client):
    """
    """
    pass

def test_order_item_post_error(client):
    """
    """
    pass

def test_order_item_get(client):
    """
    """
    pass

def test_order_item_get_error(client):
    """
    """
    pass

# ORDER STATUS FUNCTIONALITIES

def test_order_status_post(client):
    """
    """
    pass

def test_order_status_post_error(client):
    """
    """
    pass

def test_order_status_get(client):
    """
    """
    pass

def test_order_status_get_error(client):
    """
    """
    pass

# ORDERS FUNCTIONALITIES

def test_orders_get(client):
    """
    """
    pass

def test_orders_get_error(client):
    """
    """
    pass

def test_orders_post(client):
    """
    """
    pass

def test_orders_post_error(client):
    """
    """
    pass