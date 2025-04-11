import React, { useState } from 'react';
import ImageSlider from './ImageSlider';
import ModifyItemModal from './ModifyItemModal';

const ItemRow = ({
  name,
  price,
  description,
  itemId,
  images = [],
  onDelete,
  onSave,
}) => {
  const [isModifyOpen, setIsModifyOpen] = useState(false);

  const defaultImage =
    'https://t3.ftcdn.net/jpg/01/50/94/64/360_F_150946471_HKE5KUHOv2gnV83HEb9Vw6IgUv67N7vV.jpg';

  // Get image source in Base64 format
  const getImageSrc = (imageData) => {
    if (!imageData || !imageData.data) return defaultImage;

    const extension = imageData.name?.split('.').pop().toLowerCase();
    const mimeType =
      extension === 'png'
        ? 'image/png'
        : extension === 'jpeg' || extension === 'jpg'
        ? 'image/jpeg'
        : 'image/png';

    return `data:${mimeType};base64,${imageData.data}`;
  };

  return (
    <>
      <div className="flex items-center border-2 border-gray-300 p-4 rounded-lg shadow-lg hover:shadow-xl transition-all mb-12 ml-12 mr-12">
        {/* Left: Image */}
        <div className="w-32 h-32 flex-shrink-0 mr-4">
          {images.length > 1 ? (
            <ImageSlider images={images.map(getImageSrc)} />
          ) : (
            <img
              src={getImageSrc(images[0])}
              alt={images[0]?.name || name}
              className="w-full h-full object-cover rounded-lg"
            />
          )}
        </div>

        {/* Middle: Item details */}
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-800">{name}</h3>
          <p className="text-sm text-gray-500">ID: {itemId}</p>
          <p className="text-lg text-gray-700">${price}</p>
          <p className="text-gray-500">{description}</p>
        </div>

        {/* Right: Buttons */}
        <div className="flex flex-col space-y-2">
          <button
            onClick={() => setIsModifyOpen(true)}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Modify
          </button>
          <button
            onClick={() => onDelete(itemId)}
            className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-700 transition"
          >
            Delete
          </button>
        </div>
      </div>

      {/* Modify Modal */}
      <ModifyItemModal
        item={{ id: itemId, name, price, description }}
        isOpen={isModifyOpen}
        onClose={() => setIsModifyOpen(false)}
        onSave={(updatedItem) => {
          onSave(updatedItem);
          setIsModifyOpen(false);
        }}
      />
    </>
  );
};

export default ItemRow;
