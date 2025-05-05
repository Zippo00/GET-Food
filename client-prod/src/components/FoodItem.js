import React, { useState } from 'react';
import ImageSlider from './ImageSlider';
import { BASE_URL } from '../services/api'; // Import the BASE_URL/api url from api.js
const FoodItem = ({ id, name, price, description, images = [] }) => {
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [showModal, setShowModal] = useState(false); // To show modal for asking the customer name
  const [customerName, setCustomerName] = useState(''); // Store customer's name

  const defaultImage =
    'https://t3.ftcdn.net/jpg/01/50/94/64/360_F_150946471_HKE5KUHOv2gnV83HEb9Vw6IgUv67N7vV.jpg'; //if food items has no image then this will show as a default

  const getImageSrc = (imageData) => {
    if (imageData?.data) {
      const extension = imageData.name.split('.').pop().toLowerCase();
      const mimeType =
        extension === 'png'
          ? 'image/png'
          : extension === 'jpeg' || extension === 'jpg'
          ? 'image/jpeg'
          : 'image/png';
      return `data:${mimeType};base64,${imageData.data}`;
    }
    return defaultImage;
  };

  // Fetch order ID from backend
  const fetchOrderId = async (customerName) => {
    try {
      const response = await fetch(`${BASE_URL}/orders/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ customer_name: customerName }), // Send customer name
      });

      if (!response.ok) throw new Error('Failed to create order');

      const data = await response.json();
      return data.id;
    } catch (error) {
      console.error('Error fetching order ID:', error);
      return null;
    }
  };

  // Function to send an order request
  const handleOrderNow = async () => {
    if (quantity < 1) {
      setMessage('Quantity must be at least 1');
      return;
    }

    setShowModal(true); // Show modal to ask for customer's name
  };

  // Function to confirm the order
  const confirmOrder = async () => {
    if (!customerName.trim()) {
      setMessage('Please enter a valid name');
      return;
    }

    setLoading(true);
    setMessage('');

    const orderId = await fetchOrderId(customerName);
    if (!orderId) {
      setMessage('Failed to create order');
      setLoading(false);
      return;
    }

    const orderData = {
      order_id: orderId,
      item_id: id,
      quantity: quantity,
    };

    try {
      const response = await fetch(`${BASE_URL}/order-items/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData),
      });

      if (!response.ok) throw new Error('Failed to place order');

      const data = await response.json();
      setMessage(`Order placed! Order ID: ${data.order_id}`);
      setShowModal(false); // Close the modal after confirming the order
    } catch (error) {
      console.error('Error placing order:', error);
      setMessage('Error placing order. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Function to cancel the order
  const cancelOrder = () => {
    setShowModal(false);
  };

  return (
    <div className="flex space-x-4 border-2 border-gray-300 p-4 rounded-lg shadow-lg hover:shadow-xl transition-all">
      <div className="flex-1">
        <h3 className="text-2xl font-semibold text-gray-800 mb-2">{name}</h3>
        <p className="text-xl text-gray-700 mb-2">${price}</p>
        <p className="text-gray-500 mb-4">{description}</p>

        {/* Quantity Input */}
        <div className="flex items-center space-x-2">
          <label className="text-gray-700 font-semibold">Quantity:</label>
          <input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value)))}
            className="w-16 p-2 border rounded"
            min="1"
          />
        </div>

        {/* Order Now Button */}
        <button
          onClick={handleOrderNow}
          className="mt-4 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          disabled={loading}
        >
          {loading ? 'Ordering...' : 'Order Now'}
        </button>

        {/* Display Message */}
        {message && <p className="mt-2 text-sm text-green-600">{message}</p>}
      </div>

      <div className="flex-2">
        {images.length > 1 ? (
          <ImageSlider images={images.map((img) => getImageSrc(img))} />
        ) : (
          <img
            src={getImageSrc(images[0])}
            alt={name}
            className="w-72 h-48 object-cover rounded-lg"
          />
        )}
      </div>

      {/* Modal for Customer Name */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-6 rounded-lg w-1/3">
            <h2 className="text-2xl font-semibold mb-4">Enter your name</h2>
            <input
              type="text"
              value={customerName}
              onChange={(e) => setCustomerName(e.target.value)}
              className="w-full p-2 border rounded mb-4"
              placeholder="Your name"
            />
            <div className="flex space-x-4">
              <button
                onClick={cancelOrder}
                className="px-4 py-2 bg-gray-500 text-white rounded"
              >
                Cancel
              </button>
              <button
                onClick={confirmOrder}
                className="px-4 py-2 bg-blue-600 text-white rounded"
              >
                Confirm
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FoodItem;
