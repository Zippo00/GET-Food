import React from 'react';
import Header from './components/Header';
import Banner from './components/Banner';
import HomePage from './pages/HomePage';
import AddItemPage from './pages/AddItemPage'; // AddItemPage as a new page
import { Routes, Route } from 'react-router-dom'; // Import Routes and Route components
import ManageItemsPage from './pages/ManageItemsPage';
import OrderStatusPage from './pages/OrderStatusPage';
import OrderPage from './pages/OrderPage';
function App() {
  return (
    <div className="App">
      <Header />

      {/* Define routes */}
      <Routes>
        {/* HomePage rendered with Banner */}
        <Route
          path="/"
          element={
            <div className="m-16">
              <Banner /> {/* Banner shown only on HomePage */}
              <HomePage />
            </div>
          }
        />
        {/* AddItemPage rendered as a separate page */}
        <Route path="/add-item" element={<AddItemPage />} />
        <Route path="/manage-item" element={<ManageItemsPage />} />
        <Route path="/order-status" element={<OrderStatusPage />} />
        <Route path="/orders" element={<OrderPage />} />
      </Routes>
    </div>
  );
}

export default App;
