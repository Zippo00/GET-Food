import React, { useEffect, useState } from 'react';
import OrderStatusTable from '../components/OrderStatusTable';
import { fetchOrders, fetchOrderItems } from '../services/api';

const OrderStatusPage = () => {
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
      <h1 className="text-3xl font-bold mb-6">Order Status</h1>
      <OrderStatusTable orders={orders} setOrders={setOrders} />
    </div>
  );
};

export default OrderStatusPage;
