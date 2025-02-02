import React, { useState, useEffect } from "react";
import { placeOrder, getOrders } from "../services/orderService";

const Order = () => {
  const [orders, setOrders] = useState([]);
  const [orderItems, setOrderItems] = useState(["Margherita Pizza"]);

  useEffect(() => {
    getOrders().then(setOrders);
  }, []);

  /*   const handleOrder = async () => {
    const newOrder = await placeOrder(orderItems);
    setOrders([...orders, newOrder.order]);
  }; */

  return (
    <div>
      <h2>Orders</h2>
      {/*       <button onClick={handleOrder}>Place Order</button>
       */}{" "}
      <ul>
        {orders.map((order) => (
          <li key={order.id}>
            Order #{order.id} - {order.status}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Order;
