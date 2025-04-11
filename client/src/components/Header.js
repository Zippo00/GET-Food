// Header component
import React from 'react';
import { Link } from 'react-router-dom'; // For navigation

const Header = () => {
  return (
    <header className="bg-gray-900 text-white p-4">
      <div className="container mx-auto flex items-center justify-between">
        {/* Logo */}
        <div className="text-2xl font-bold">
          <Link to="/" className="text-white">
            GetFood
          </Link>
        </div>

        {/* Navigation Bar */}
        <nav className="flex space-x-6">
          <Link to="/" className="hover:text-gray-400">
            Home
          </Link>

          <Link to="/add-item" className="hover:text-gray-400">
            Add Items
          </Link>
          <Link to="/manage-item" className="hover:text-gray-400">
            Manage Items
          </Link>
          <Link to="/orders" className="hover:text-gray-400">
            Orders
          </Link>
          <Link to="/order-status" className="hover:text-gray-400">
            Order Status
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
