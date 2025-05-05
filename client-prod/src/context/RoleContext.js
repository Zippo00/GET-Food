// src/context/RoleContext.js
import React, { createContext, useState, useEffect } from 'react';

export const RoleContext = createContext();

export const RoleProvider = ({ children }) => {
  const [role, setRole] = useState(null); // null | 'admin' | 'customer'

  useEffect(() => {
    const storedRole = localStorage.getItem('role');
    if (storedRole) setRole(storedRole);
  }, []);

  const loginAs = (selectedRole) => {
    localStorage.setItem('role', selectedRole);
    setRole(selectedRole);
  };

  const logout = () => {
    localStorage.removeItem('role');
    setRole(null);
  };

  return (
    <RoleContext.Provider value={{ role, loginAs, logout }}>
      {children}
    </RoleContext.Provider>
  );
};
