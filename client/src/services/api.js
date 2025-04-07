const BASE_URL = 'http://127.0.0.1:5000'; // our Backend base URL

export const fetchItems = async () => {
  const response = await fetch(`${BASE_URL}/items/`);
  return response.json();
};

export const fetchImages = async () => {
  const response = await fetch(`${BASE_URL}/images/`);
  const imageList = await response.json();

  // Fetch Base64 image data for each image
  const imageDataPromises = imageList.map(async (image) => {
    const imageResponse = await fetch(`${BASE_URL}/images/${image.id}`);
    if (!imageResponse.ok) {
      return null;
    }
    return imageResponse.json(); // Get Base64 data
  });

  const imagesWithData = await Promise.all(imageDataPromises);
  return imagesWithData.filter((image) => image !== null); // Remove failed requests
};

export const deleteItem = async (id) => {
  await fetch(`${BASE_URL}/items/${id}`, { method: 'DELETE' });
};

// Fetch all orders
export const fetchOrders = async () => {
  try {
    const response = await fetch(`${BASE_URL}/orders/`);
    if (!response.ok) throw new Error('Failed to fetch orders');
    return await response.json();
  } catch (error) {
    console.error('Error fetching orders:', error);
    return [];
  }
};

// Fetch order items for a given order ID
export const fetchOrderItems = async (orderId) => {
  try {
    const response = await fetch(`${BASE_URL}/order-items/${orderId}`);
    if (!response.ok)
      throw new Error(`Failed to fetch items for order ${orderId}`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching order items:', error);
    return [];
  }
};

// Fetch item details for a given item ID
export const fetchItemDetails = async (itemId) => {
  try {
    const response = await fetch(`${BASE_URL}/items/${itemId}`);
    if (!response.ok)
      throw new Error(`Failed to fetch item details for ${itemId}`);
    return await response.json();
  } catch (error) {
    console.error('Error fetching item details:', error);
    return null;
  }
};

// Update order status
export const updateOrderStatus = async (orderId, status) => {
  try {
    const response = await fetch(`${BASE_URL}/order-status/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_id: orderId, status }),
    });

    if (!response.ok) throw new Error('Failed to update order status');

    return await response.json();
  } catch (error) {
    console.error('Error updating order status:', error);
    return null;
  }
};
