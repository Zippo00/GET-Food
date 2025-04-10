import React from 'react';
import FoodItem from './FoodItem';

const FoodSection = ({ foodItems }) => {
  return (
    <section className="mb-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {foodItems.map((item) => (
          <FoodItem
            key={item.id}
            id={item.id}
            name={item.name}
            price={item.price}
            description={item.description}
            images={item.images}
          />
        ))}
      </div>
    </section>
  );
};

export default FoodSection;
