import React from "react";
import Menu from "./components/Menu";
import Order from "./components/Order";

const App = () => {
  return (
    <div>
      <h1>Restaurant Menu & Orders</h1>
      <Menu />
      <Order />
    </div>
  );
};

export default App;
