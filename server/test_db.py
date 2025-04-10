"""
Unit tests for Database.
"""
import pytest
import app
import os
import pytest
import tempfile
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import event
from api.models.item import Item
from api.models.image import Image
from api.models.order import Order
from api.models.order_item import OrderItem
from api.models.order_status import OrderStatus
from sqlalchemy.exc import IntegrityError, StatementError

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.app.config["TESTING"] = True

    ctx = app.app.app_context()
    ctx.push()
    app.db.create_all()
        
    yield app.db
    
    app.db.session.rollback()
    app.db.drop_all()
    app.db.session.remove()
    ctx.pop()
    os.close(db_fd)
    os.unlink(db_fname)

def _get_item():
    return Item(
        name="test_item",
        description="test_description",
        price=1.0,
        )

def _get_image(item_id):
    return Image(
        data = b"test_image_data",
        item_id=item_id,
        name="test_image"
    )

def _get_order():
    return Order(
        customer_name="test_customer",
        created_at=datetime.now(),
    )

def get_order_item(order_id, item_id):
    return OrderItem(
        order_id=order_id,
        item_id=item_id,
        quantity=1,
    )

def _get_order_status(order_id):
    return OrderStatus(
        order_id=order_id,
        status="pending",
        updated_at=datetime.now(),
    )

def test_create_instances(db_handle):
    """
    Tests that we can create one instance of each model and save them to the
    database using valid values for all columns. After creation, test that 
    everything can be found from database, and that all foreign keys have been
    saved correctly.
    """

    # Create item
    item = _get_item()
    db_handle.session.add(item)
    db_handle.session.commit()


    for item in Item.query.all():
        print(item.id, item.name, item.description, item.price)
    # Check that item exists
    assert Item.query.count() == 1
    db_item = Item.query.first()

    # Create image
    image = _get_image(db_item.id)
    db_handle.session.add(image)
    db_handle.session.commit()

    # Check that image exists
    assert Image.query.count() == 1
    db_image = Image.query.first()

    #check that image has the correct itemId
    assert db_image.item_id == db_item.id

    #Create order
    order = _get_order()
    db_handle.session.add(order)
    db_handle.session.commit()

    #Check that order exists
    assert Order.query.count() == 1
    db_order = Order.query.first()

    #Create order item
    order_item = get_order_item(db_order.id, db_item.id)
    db_handle.session.add(order_item)
    db_handle.session.commit()

    # Check that order item exists
    assert OrderItem.query.count() == 1
    db_order_item = OrderItem.query.first()

    #check that order item has the correct orderId and itemId
    assert db_order_item.order_id == db_order.id
    assert db_order_item.item_id == db_item.id

    #Create order status
    order_status = _get_order_status(db_order.id)
    db_handle.session.add(order_status)
    db_handle.session.commit()

    # Check that order status exists
    assert OrderStatus.query.count() == 1
    db_order_status = OrderStatus.query.first()

    #check that order status has the correct orderId
    assert db_order_status.order_id == db_order.id

def test_image_ondelete_item(db_handle):
    """
    Tests that image is deleted when the item
    is deleted.
    """
    item = _get_item()
    db_handle.session.add(item)
    db_item = Item.query.first()

    image = _get_image(db_item.id)
    db_handle.session.add(image)
    db_image = Image.query.first()

    assert db_image.item_id == db_item.id

    db_handle.session.commit()
    db_handle.session.delete(db_item)

    assert Item.query.first() is None

    db_handle.session.commit()

    assert Image.query.first() is None

def test_image_onupdate_item(db_handle):
    """
    Tests that images foreign key is updated when the item
    is updated.
    """
    item = _get_item()
    db_handle.session.add(item)
    db_item = Item.query.first()
    image = _get_image(db_item.id)
    db_handle.session.add(image)
    db_handle.session.commit()
    db_item.id = "new_id"
    assert db_item.id == "new_id"
    db_handle.session.commit()
    assert image.item_id == db_item.id

def test_order_item_ondelete_order(db_handle):
    """
    Tests that an order item is deleted when the order
    is deleted.
    """
    item = _get_item()
    db_handle.session.add(item)
    db_item = Item.query.first()

    order = _get_order()
    db_handle.session.add(order)
    db_order = Order.query.first()

    order_item = get_order_item(db_order.id, db_item.id)
    db_handle.session.add(order_item)
    db_order_item = OrderItem.query.first()

    assert db_order_item.order_id == db_order.id

    db_handle.session.commit()
    db_handle.session.delete(db_order)

    assert Order.query.first() is None

    db_handle.session.commit()

    assert OrderItem.query.first() is None

def test_order_item_ondelete_item(db_handle):
    """
    Tests that an order items is deleted when the item
    is deleted.
    """
    item = _get_item()
    db_handle.session.add(item)
    db_item = Item.query.first()

    order = _get_order()
    db_handle.session.add(order)
    db_order = Order.query.first()

    order_item = get_order_item(db_order.id, db_item.id)
    db_handle.session.add(order_item)
    db_order_item = OrderItem.query.first()

    assert db_order_item.item_id == db_item.id

    db_handle.session.commit()
    db_handle.session.delete(db_item)

    assert Item.query.first() is None

    db_handle.session.commit()

    assert OrderItem.query.first() is None

def test_order_item_onupdate_item(db_handle):
    """
    Tests that an order items foreign key is updated when the item
    is updated.
    """
    item = _get_item()
    db_handle.session.add(item)
    db_item = Item.query.first()

    order = _get_order()
    db_handle.session.add(order)
    db_order = Order.query.first()

    order_item = get_order_item(db_order.id, db_item.id)
    db_handle.session.add(order_item)
    db_handle.session.commit()
    
    db_item.id = "new_id"
    assert db_item.id == "new_id"
    
    db_handle.session.commit()
    
    assert order_item.item_id == db_item.id

def test_order_item_onupdate_order(db_handle):
    """
    Tests that an order items foreign key is updated when the order
    is updated.
    """
    item = _get_item()
    db_handle.session.add(item)
    db_item = Item.query.first()

    order = _get_order()
    db_handle.session.add(order)
    db_order = Order.query.first()

    order_item = get_order_item(db_order.id, db_item.id)
    db_handle.session.add(order_item)
    db_handle.session.commit()
    
    db_order.id = "new_id"
    assert db_order.id == "new_id"
    
    db_handle.session.commit()
    
    assert order_item.order_id == db_order.id

def test_order_status_ondelete_order(db_handle):
    """
    Tests that an order status is deleted when the order
    is deleted.
    """
    order = _get_order()
    db_handle.session.add(order)
    db_order = Order.query.first()

    order_status = _get_order_status(db_order.id)
    db_handle.session.add(order_status)
    db_order_status = OrderStatus.query.first()

    assert db_order_status.order_id == db_order.id

    db_handle.session.commit()
    db_handle.session.delete(db_order)

    assert Order.query.first() is None

    db_handle.session.commit()

    assert OrderStatus.query.first() is None

def test_order_status_onupdate_order(db_handle):
    """
    Tests that the order status foreign keys is updated when the order
    is updated.
    """
    order = _get_order()
    db_handle.session.add(order)
    db_order = Order.query.first()

    order_status = _get_order_status(db_order.id)
    db_handle.session.add(order_status)
    db_handle.session.commit()
    
    db_order.id = "new_id"
    assert db_order.id == "new_id"
    
    db_handle.session.commit()
    
    assert order_status.order_id == db_order.id

def test_item_columns(db_handle):
    """
    Tests the types and restrictions of item columns.
    """
    #test id not null
    item = _get_item()
    db_handle.session.add(item)
    assert Item.query.count() == 1
    db_item = Item.query.first()
    assert db_item.id is not None

    db_handle.session.rollback()

    #test id unique
    item1 = _get_item()
    db_handle.session.add(item1)
    db_item1 = Item.query.first()
    item2 = _get_item()
    item2.id = db_item1.id
    db_handle.session.add(item2)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    
    db_handle.session.rollback()

    #test name not null
    item = _get_item()
    item.name = None
    db_handle.session.add(item)
    with pytest.raises(StatementError):
        db_handle.session.commit()
        
    db_handle.session.rollback()
    
    #test name unique
    item1 = _get_item()
    item2 = _get_item()
    item2.name = item1.name
    db_handle.session.add(item1)
    db_handle.session.add(item2)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
        
    db_handle.session.rollback()
    

    #test price not null
    item = _get_item()
    item.price = None
    db_handle.session.add(item)
    with pytest.raises(StatementError):
        db_handle.session.commit()
        
    db_handle.session.rollback()

    #test price type
    item = _get_item()
    item.price = str(item.price) + "wrong"
    db_handle.session.add(item)
    with pytest.raises(StatementError):
        db_handle.session.commit()
    
    db_handle.session.rollback()

    #test description nullable
    item = _get_item()
    item.description = None
    db_handle.session.add(item)
    assert Item.query.count() == 1
    db_item = Item.query.first()
    assert db_item.description is None
    
def test_image_columns(db_handle):
    """
    Tests image columns' restrictions. 
    """

    item= _get_item()
    db_handle.session.add(item)
    db_item = Item.query.first()

    db_handle.session.commit()

    #test id not null
    image = _get_image(db_item.id)
    db_handle.session.add(image)
    db_image = Image.query.first()
    assert db_image.id is not None

    db_handle.session.delete(db_image)

    #test id unique
    image1 = _get_image(db_item.id)
    db_handle.session.add(image1)
    db_image1 = Image.query.first()
    image2 = _get_image(db_item.id)
    image2.id = db_image1.id
    db_handle.session.add(image2)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    
    db_handle.session.rollback()

    #test data not null
    image = _get_image(db_item.id)
    image.data = None
    db_handle.session.add(image)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    
    db_handle.session.rollback()

    #test data type
    image = _get_image(db_item.id)
    image.data = "this is not binary data"
    db_handle.session.add(image)
    with pytest.raises(StatementError):
        db_handle.session.commit()

    db_handle.session.rollback()

    #test name not null
    image = _get_image("test_id")
    image.name = None
    db_handle.session.add(image)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    #test item_id not null
    image = _get_image(None)
    db_handle.session.add(image)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()
    
def test_order_columns(db_handle):
    """
    Test order columns' restrictions.
    """

    #test id not null
    order = _get_order()
    db_handle.session.add(order)
    assert Order.query.count() == 1
    db_order = Order.query.first()
    assert db_order.id is not None

    db_handle.session.rollback()

    #test id unique
    order1 = _get_order()
    db_handle.session.add(order1)
    db_order1 = Order.query.first()
    order2 = _get_order()
    order2.id = db_order1.id
    db_handle.session.add(order2)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    #test customer_name not null
    order = _get_order()
    order.customer_name = None
    db_handle.session.add(order)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    #test created_at type
    order = _get_order()
    order.created_at = str(order.created_at) + "wrong"
    db_handle.session.add(order)
    with pytest.raises(StatementError):
        db_handle.session.commit()

    db_handle.session.rollback()

    #test created_at sets default
    order = _get_order()
    order.created_at = None
    db_handle.session.add(order)
    db_order = Order.query.first()
    assert db_order.created_at is not None
        
def test_order_item_columns(db_handle):
    """
    Tests order item columns' restrictions.
    """

    item = _get_item()
    db_handle.session.add(item)
    db_item = Item.query.first()
    order = _get_order()
    db_handle.session.add(order)
    db_order = Order.query.first()

    db_handle.session.commit()

    #test id not null
    order_item = get_order_item(db_order.id,db_item.id)
    db_handle.session.add(order_item)
    assert OrderItem.query.count() == 1
    db_order_item = OrderItem.query.first()
    assert db_order_item.id is not None

    #test id unique
    order_item1 = get_order_item(db_order.id,db_item.id)
    db_handle.session.add(order_item1)
    db_order_item1 = OrderItem.query.first()
    order_item2 = get_order_item(db_order.id,db_item.id)
    order_item2.id = db_order_item1.id
    db_handle.session.add(order_item2)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    #test order_id not null
    order_item = get_order_item(None,db_item.id)
    db_handle.session.add(order_item)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    #test item_id not null
    order_item = get_order_item(db_order.id,None)
    db_handle.session.add(order_item)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    #test quantity default value
    order_item = get_order_item(db_order.id,db_item.id)
    order_item.quantity = None
    db_handle.session.add(order_item)
    db_order_item = OrderItem.query.first()
    assert db_order_item.quantity == 1

    db_handle.session.delete(order_item)
    assert OrderItem.query.count() == 0

    #test quantity type
    order_item = get_order_item(db_order.id,db_item.id)
    order_item.quantity = 1,5
    db_handle.session.add(order_item)
    with pytest.raises(StatementError):
        db_handle.session.commit()

    db_handle.session.rollback()

def test_order_status_columns(db_handle):
    """
    Tests order status columns' restrictions.
    """

    order = _get_order()
    db_handle.session.add(order)
    db_order = Order.query.first()

    db_handle.session.commit()

    #test id not null
    order_status = _get_order_status(db_order.id)
    db_handle.session.add(order_status)
    db_order_status = OrderStatus.query.first()
    assert db_order_status.id is not None

    db_handle.session.delete(db_order_status)
    
    #test id unique
    order_status1 = _get_order_status(db_order.id)
    db_handle.session.add(order_status1)
    db_order_status1 = OrderStatus.query.first()
    order_status2 = _get_order_status(db_order.id)
    order_status2.id = db_order_status1.id
    db_handle.session.add(order_status2)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    #test order_id not null
    order_status = _get_order_status(None)
    db_handle.session.add(order_status)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    #test status not null
    order_status = _get_order_status(db_order.id)
    order_status.status = None
    db_handle.session.add(order_status)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

    db_handle.session.rollback()

    #test updated_at type
    order_status = _get_order_status(db_order.id)
    order_status.updated_at = str(order_status.updated_at) + "wrong"
    db_handle.session.add(order_status)
    with pytest.raises(StatementError):
        db_handle.session.commit()

    db_handle.session.rollback()

    #test updated_at sets default
    assert Order.query.first() is not None
    order_status = _get_order_status(db_order.id)
    order_status.updated_at = None
    db_handle.session.add(order_status)
    db_order_status = OrderStatus.query.first()
    assert db_order_status.updated_at is not None

    