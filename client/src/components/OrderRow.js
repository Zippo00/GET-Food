import React, { useEffect } from 'react';
import { formatDate } from './formatDate';

const OrderRow = ({
  order,
  orderStatus,
  itemDetails,
  getImageForItem,
  customerName,
  itemQuantities,
}) => {
  useEffect(() => {
    console.log('ItemDetails:', itemDetails);
  }, [order, itemDetails]);

  const items = Array.isArray(order.items) ? order.items : [];

  return (
    <tr className="border-b border-gray-200 hover:bg-gray-50 transition-colors">
      {/* Order ID */}
      <td className="py-3 px-4 text-sm text-gray-700">{order.id}</td>

      {/* Customer Name */}
      <td className="py-3 px-4 text-sm text-gray-700">
        {customerName || 'N/A'}
      </td>

      {/* Item Names */}
      <td className="py-3 px-4 text-sm text-gray-700">
        {items.map((item) => {
          const itemName = itemDetails[item.item_id]?.name || 'Loading...';
          return (
            <div key={item.id}>
              <strong>{itemName}</strong>
            </div>
          );
        })}
      </td>

      {/* Item Images */}
      <td className="py-3 px-4 text-sm text-gray-700">
        {items.map((item) => {
          const itemImage = getImageForItem(item.item_id);
          return (
            <img
              key={item.id}
              src={itemImage}
              alt={itemDetails[item.item_id]?.name || 'Item Image'}
              className="w-16 h-16 object-cover rounded mb-1"
            />
          );
        })}
      </td>

      {/* Quantities (from itemQuantities prop) */}
      <td className="py-3 px-4 text-sm text-gray-700">
        {items.map((item) => {
          const quantity = itemQuantities?.[item.item_id] || 0;
          return <div key={item.id}>Qty: {quantity}</div>;
        })}
      </td>

      {/* Created At */}
      <td className="py-3 px-4 text-sm text-gray-700">
        {formatDate(order.created_at)}
      </td>

      {/* Updated At */}
      <td className="py-3 px-4 text-sm text-gray-700">
        {formatDate(orderStatus?.updated_at)}
      </td>

      {/* Status */}
      <td className="py-3 px-4 text-sm text-gray-700">
        {orderStatus?.status || 'Pending'}
      </td>
    </tr>
  );
};

export default OrderRow;
