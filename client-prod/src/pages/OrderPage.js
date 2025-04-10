import React, { useEffect, useState } from 'react';
import OrderTable from '../components/OrderTable';
import { fetchOrders, fetchOrderItems } from '../services/api';

const OrderPage = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const loadOrdersWithItems = async () => {
      const ordersData = await fetchOrders();
      if (!ordersData.length) return;

      // Fetch order items for each order
      const ordersWithItems = await Promise.all(
        ordersData.map(async (order) => {
          const items = await fetchOrderItems(order.id);
          return { ...order, items };
        }),
      );

      setOrders(ordersWithItems);
    };

    loadOrdersWithItems();
  }, []);

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">All Orders</h1>
      <OrderTable orders={orders} setOrders={setOrders} />
    </div>
  );
};

export default OrderPage;
