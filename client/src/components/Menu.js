import React, { useEffect, useState } from "react";
import { getMenu } from "../services/menuServices";

const Menu = () => {
  const [menuItems, setMenuItems] = useState([]);

  useEffect(() => {
    getMenu().then(setMenuItems);
  }, []);

  return (
    <div>
      <h2>Food Menu</h2>
      <ul>
        {menuItems.map((item) => (
          <li key={item.id}>
            {item.name} - ${item.price}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Menu;
