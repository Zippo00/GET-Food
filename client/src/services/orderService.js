import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000/api/order";

export const placeOrder = async (orderItems) => {
  try {
    const response = await axios.post(API_BASE_URL, { items: orderItems });
    return response.data;
  } catch (error) {
    console.error("Error placing order:", error);
    return { error: "Order failed" };
  }
};

export const getOrders = async () => {
  try {
    const response = await axios.get(API_BASE_URL);
    return response.data;
  } catch (error) {
    console.error("Error fetching orders:", error);
    return [];
  }
};
