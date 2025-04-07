//Home page banner - 3 images in a row, fetched from online
import React from 'react';

const Banner = () => {
  return (
    <div className="">
      <h2 className="text-center text-3xl font-semibold mb-6">
        Order Now and Satisfy Your Hunger!
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {/* Image 1 */}
        <div className="overflow-hidden rounded-lg shadow-lg">
          <img
            src="https://images.immediate.co.uk/production/volatile/sites/30/2020/08/chorizo-mozarella-gnocchi-bake-cropped-9ab73a3.jpg?quality=90&resize=556,505"
            alt="Banner Item 1"
            className="w-full h-64 object-cover transform hover:scale-105 transition duration-300 ease-in-out"
          />
        </div>

        {/* Image 2 */}
        <div className="overflow-hidden rounded-lg shadow-lg">
          <img
            src="https://designwomb.com/imager/uploadsnew/Work/69698/guju-indian-sauce-branding-food-packaging-design1_9e6859c5fc71dce906c7b05a9bb31189.jpg"
            alt="Banner Item 2"
            className="w-full h-64 object-cover transform hover:scale-105 transition duration-300 ease-in-out"
          />
        </div>

        {/* Image 3 */}
        <div className="overflow-hidden rounded-lg shadow-lg">
          <img
            src="https://saturo.com/cdn/shop/files/junkfood.jpg"
            alt="Banner Item 3"
            className="w-full h-64 object-cover transform hover:scale-105 transition duration-300 ease-in-out"
          />
        </div>
      </div>
    </div>
  );
};

export default Banner;
