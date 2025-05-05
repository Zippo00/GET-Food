// src/components/RoleModal.js
import React, { useContext } from 'react';
import { RoleContext } from '../context/RoleContext';

const RoleModal = () => {
  const { loginAs } = useContext(RoleContext);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
      <div className="bg-white p-8 rounded-lg text-center">
        <h2 className="text-xl font-bold mb-4">Login As</h2>
        <div className="flex justify-center space-x-4">
          <button
            className="px-4 py-2 bg-green-600 text-white rounded"
            onClick={() => loginAs('customer')}
          >
            Customer
          </button>
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded"
            onClick={() => loginAs('admin')}
          >
            Admin
          </button>
        </div>
      </div>
    </div>
  );
};

export default RoleModal;
