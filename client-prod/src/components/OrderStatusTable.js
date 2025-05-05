import React, { useEffect, useState } from 'react';
import { BASE_URL } from '../services/api'; // Import the BASE_URL/api url from api.js

const statusOptions = [
  'All',
  'Pending',
  'Preparing',
  'Ready for Delivery',
  'Delivered',
];

const OrderStatusTable = ({ orders, setOrders }) => {
  const [itemNames, setItemNames] = useState({});
  const [orderStatuses, setOrderStatuses] = useState({});
  const [orderItems, setOrderItems] = useState({});
  const [isUpdating, setIsUpdating] = useState(false);
  const fetchedStatusSet = new Set();

  // Fetch item name
  const fetchItemName = async (itemId) => {
    if (itemNames[itemId]) return; // Prevent duplicate fetches
    try {
      const response = await fetch(`${BASE_URL}/items/${itemId}`);
      const data = await response.json();
      if (data?.name) {
        setItemNames((prev) => ({ ...prev, [itemId]: data.name }));
      }
    } catch (error) {
      console.error(`Error fetching item name for ID ${itemId}:`, error);
    }
  };

  // Fetch items for order
  const fetchItemsForOrder = async (orderId) => {
    try {
      const response = await fetch(`${BASE_URL}/order-items/${orderId}/items`);
      const data = await response.json();

      if (Array.isArray(data)) {
        setOrderItems((prev) => ({ ...prev, [orderId]: data }));

        // Fetch names for each item
        for (const item of data) {
          await fetchItemName(item.item_id);
        }
      }
    } catch (error) {
      console.error(`Error fetching items for order ${orderId}:`, error);
    }
  };

  // Fetch order status
  const fetchOrderStatus = async (orderId) => {
    if (fetchedStatusSet.has(orderId)) return;
    fetchedStatusSet.add(orderId);
    try {
      const response = await fetch(`${BASE_URL}/order-status/${orderId}`);
      const data = await response.json();

      if (data.length > 0) {
        const latestStatus = data[data.length - 1];
        setOrderStatuses((prev) => ({
          ...prev,
          [orderId]: {
            status: latestStatus.status,
            updated_at: latestStatus.updated_at,
          },
        }));
      } else {
        setOrderStatuses((prev) => ({
          ...prev,
          [orderId]: { status: 'Pending', updated_at: null },
        }));
      }
    } catch (error) {
      console.error(`Error fetching status for order ${orderId}:`, error);
    }
  };

  useEffect(() => {
    orders.forEach((order) => {
      fetchItemsForOrder(order.id);
      fetchOrderStatus(order.id);
    });
  }, [orders]);

  const handleStatusChange = async (orderId, newStatus) => {
    const confirmed = window.confirm(`Change status to "${newStatus}"?`);
    if (!confirmed) return;

    setIsUpdating(true);
    try {
      const response = await fetch(`${BASE_URL}/order-status/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_id: orderId, status: newStatus }),
      });

      if (!response.ok) throw new Error('Failed to update order status');

      setOrderStatuses((prev) => ({
        ...prev,
        [orderId]: {
          status: newStatus,
          updated_at: new Date().toISOString(),
        },
      }));

      alert('Order status updated successfully!');
    } catch (error) {
      console.error('Error updating order status:', error);
      alert('Error updating order status. Please try again.');
    } finally {
      setIsUpdating(false);
    }
  };

  return (
    <div className="overflow-x-auto shadow-lg rounded-lg bg-white">
      <table className="min-w-full table-auto">
        <thead>
          <tr className="bg-gray-100 border-b border-gray-300">
            <th className="py-3 px-4 text-left text-sm font-semibold text-gray-600">
              Order ID
            </th>
            <th className="py-3 px-4 text-left text-sm font-semibold text-gray-600">
              Customer Name
            </th>
            <th className="py-3 px-4 text-left text-sm font-semibold text-gray-600">
              Created At
            </th>
            <th className="py-3 px-4 text-left text-sm font-semibold text-gray-600">
              Updated At
            </th>
            <th className="py-3 px-4 text-left text-sm font-semibold text-gray-600">
              Items
            </th>
            <th className="py-3 px-4 text-left text-sm font-semibold text-gray-600">
              Status
            </th>
          </tr>
        </thead>
        <tbody>
          {orders.map((order) => (
            <tr
              key={order.id}
              className="border-b border-gray-200 hover:bg-gray-50 transition-colors"
            >
              <td className="py-3 px-4 text-sm text-gray-700">{order.id}</td>
              <td className="py-3 px-4 text-sm text-gray-700">
                {order.customer_name}
              </td>
              <td className="py-3 px-4 text-sm text-gray-700">
                {order.created_at
                  ? new Date(order.created_at).toLocaleString('en-US', {
                      timeZone: 'Europe/Helsinki',
                    })
                  : 'N/A'}
              </td>
              <td className="py-3 px-4 text-sm text-gray-700">
                {orderStatuses[order.id]?.updated_at
                  ? new Date(orderStatuses[order.id].updated_at).toLocaleString(
                      'en-US',
                      {
                        timeZone: 'Europe/Helsinki',
                      },
                    )
                  : 'N/A'}
              </td>
              <td className="py-3 px-4 text-sm text-gray-700">
                <ul>
                  {(orderItems[order.id] || []).map((item) => (
                    <li key={item.id}>
                      <strong>{itemNames[item.item_id] || 'Loading...'}</strong>{' '}
                      (Qty: {item.quantity})
                    </li>
                  ))}
                </ul>
              </td>
              <td className="py-3 px-4 text-sm">
                <select
                  value={orderStatuses[order.id]?.status || 'Pending'}
                  onChange={(e) => handleStatusChange(order.id, e.target.value)}
                  className="p-2 border rounded-lg text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  disabled={isUpdating}
                >
                  {statusOptions.slice(1).map((status) => (
                    <option key={status} value={status}>
                      {status}
                    </option>
                  ))}
                </select>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default OrderStatusTable;
