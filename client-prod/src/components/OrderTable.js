import React, { useEffect, useState } from 'react';

const OrderTable = ({ orders, setOrders }) => {
  const [itemNames, setItemNames] = useState({});
  const [orderStatuses, setOrderStatuses] = useState({});

  const fetchedStatusSet = new Set(); // Track fetched statuses

  // Fetch item names
  const fetchItemName = async (itemId) => {
    try {
      const response = await fetch(`http://localhost:5000/items/${itemId}`);
      const data = await response.json();
      if (data && data.name) {
        setItemNames((prev) => ({ ...prev, [itemId]: data.name }));
      }
    } catch (error) {
      console.error('Error fetching item name:', error);
    }
  };

  // Fetch order status one by one
  const fetchOrderStatus = async (orderId) => {
    if (fetchedStatusSet.has(orderId)) return; // Prevent duplicate fetches
    fetchedStatusSet.add(orderId);
    try {
      const response = await fetch(
        `http://localhost:5000/order-status/${orderId}`,
      );
      const data = await response.json();

      if (data.length > 0) {
        const latestStatusEntry = data[data.length - 1];
        setOrderStatuses((prev) => ({
          ...prev,
          [orderId]: {
            status: latestStatusEntry.status,
            updated_at: latestStatusEntry.updated_at,
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
      setOrderStatuses((prev) => ({
        ...prev,
        [orderId]: { status: 'Pending', updated_at: null },
      }));
    }
  };

  useEffect(() => {
    orders.forEach((order) => {
      order.items.forEach((item) => {
        if (!itemNames[item.item_id]) {
          fetchItemName(item.item_id);
        }
      });

      if (orderStatuses[order.id] === undefined) {
        fetchOrderStatus(order.id);
      }
    });
  }, [orders]);

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
              Item
            </th>
            <th className="py-3 px-4 text-left text-sm font-semibold text-gray-600">
              Item ID
            </th>
            <th className="py-3 px-4 text-left text-sm font-semibold text-gray-600">
              Quantity
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

              {/* Item Names Column */}
              <td className="py-3 px-4 text-sm text-gray-700">
                <ul>
                  {order.items.map((item) => (
                    <li key={item.id}>
                      <strong>{itemNames[item.item_id] || 'Loading...'}</strong>
                    </li>
                  ))}
                </ul>
              </td>

              {/* Item IDs Column */}
              <td className="py-3 px-4 text-sm text-gray-700">
                <ul>
                  {order.items.map((item) => (
                    <li key={item.id}>{item.item_id}</li>
                  ))}
                </ul>
              </td>

              {/* Quantities Column */}
              <td className="py-3 px-4 text-sm text-gray-700">
                <ul>
                  {order.items.map((item) => (
                    <li key={item.id}>Qty: {item.quantity}</li>
                  ))}
                </ul>
              </td>

              {/* Status Column */}
              <td className="py-3 px-4 text-sm text-gray-700">
                {orderStatuses[order.id]?.status || 'Pending'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default OrderTable;
