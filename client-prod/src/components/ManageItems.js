import React, { useState } from 'react';
import ItemRow from './ItemRow';

const ManageItems = ({ foodItems }) => {
  const [items, setItems] = useState(foodItems); // Local state to manage updates

  // Delete item function
  const handleDelete = async (itemId) => {
    if (!window.confirm('Are you sure you want to delete this item?')) return;

    try {
      const response = await fetch(`http://localhost:5000/items/${itemId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error('Failed to delete item');
      }

      // Remove item from state after successful deletion
      setItems(items.filter((item) => item.id !== itemId));
      alert('Item deleted successfully!');
    } catch (error) {
      console.error('Error deleting item:', error);
      alert('Error deleting item!');
    }
  };

  // Modify item function (with API call)
  const handleModify = async (updatedItem) => {
    try {
      const response = await fetch(
        `http://localhost:5000/items/${updatedItem.id}`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(updatedItem),
        },
      );

      if (!response.ok) {
        throw new Error('Failed to update item');
      }

      const updatedItemData = await response.json(); // Assuming the updated item is returned in the response

      // Update the item in the local state after the successful API call
      setItems((prevItems) =>
        prevItems.map((item) =>
          item.id === updatedItemData.id
            ? { ...item, ...updatedItemData }
            : item,
        ),
      );

      alert('Item updated successfully!');
    } catch (error) {
      console.error('Error modifying item:', error);
      alert('Error modifying item!');
    }
  };

  return (
    <section className="mb-8 pl-16 pr-16">
      <div className="grid grid-cols-1 md:grid-cols-1">
        {items.length > 0 ? (
          items.map((item) => (
            <ItemRow
              key={item.id}
              itemId={item.id}
              name={item.name}
              price={item.price}
              description={item.description}
              images={item.images}
              onDelete={handleDelete}
              onModify={handleModify}
              onSave={handleModify}
            />
          ))
        ) : (
          <p className="text-center col-span-2 text-gray-500">
            No items available.
          </p>
        )}
      </div>
    </section>
  );
};

export default ManageItems;
