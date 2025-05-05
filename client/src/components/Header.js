import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { RoleContext } from '../context/RoleContext';

const Header = () => {
  const { role, logout } = useContext(RoleContext);

  return (
    <header className="bg-gray-900 text-white p-4">
      <div className="container mx-auto flex items-center justify-between">
        <div className="text-2xl font-bold">
          <Link to="/" className="text-white">
            GetFood
          </Link>
        </div>

        <nav className="flex items-center space-x-6">
          <Link to="/" className="hover:text-gray-400">
            Home
          </Link>

          {role === 'admin' && (
            <>
              <Link to="/add-item" className="hover:text-gray-400">
                Add Items
              </Link>
              <Link to="/manage-item" className="hover:text-gray-400">
                Manage Items
              </Link>
              <Link to="/order-status" className="hover:text-gray-400">
                Order Status
              </Link>
            </>
          )}

          <Link to="/orders" className="hover:text-gray-400">
            Orders
          </Link>

          <button
            onClick={logout}
            className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded text-white text-sm"
          >
            Logout
          </button>
        </nav>
      </div>
    </header>
  );
};

export default Header;
