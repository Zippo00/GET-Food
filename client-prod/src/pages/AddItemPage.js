import React from 'react';
import ItemForm from '../components/ItemForm';

const AddItemPage = () => {
  return (
    <div className="container mx-auto p-6">
      <ItemForm onItemAdded={() => {}} />
    </div>
  );
};

export default AddItemPage;
