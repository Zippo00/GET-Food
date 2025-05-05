import React, { useContext } from 'react';
import Header from './components/Header';
import Banner from './components/Banner';
import HomePage from './pages/HomePage';
import AddItemPage from './pages/AddItemPage';
import ManageItemsPage from './pages/ManageItemsPage';
import OrderStatusPage from './pages/OrderStatusPage';
import OrderPage from './pages/OrderPage';
import RoleModal from './components/RoleModal'; // 👈 Add this
import { RoleContext } from './context/RoleContext';
import { Routes, Route } from 'react-router-dom';

function App() {
  const { role } = useContext(RoleContext);

  if (!role) return <RoleModal />; // Show modal if not logged in

  return (
    <div className="App">
      <Header />
      <Routes>
        <Route
          path="/"
          element={
            <div className="m-16">
              <Banner />
              <HomePage />
            </div>
          }
        />
        <Route path="/add-item" element={<AddItemPage />} />
        <Route path="/manage-item" element={<ManageItemsPage />} />
        <Route path="/order-status" element={<OrderStatusPage />} />
        <Route path="/orders" element={<OrderPage />} />
      </Routes>
    </div>
  );
}

export default App;
