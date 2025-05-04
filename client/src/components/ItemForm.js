import React, { useState } from 'react';
import axios from 'axios';
import { BASE_URL } from '../services/api'; // Import the BASE_URL/api url from api.js

const ItemForm = () => {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [description, setDescription] = useState('');
  const [imageName, setImageName] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(''); // State to store success message

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const itemData = {
      name,
      price: parseFloat(price),
      description,
    };

    try {
      const response = await axios.post(`${BASE_URL}/items/`, itemData);
      const itemId = response.data.id; // Assume the backend returns the item ID

      // After item is successfully created, upload the image
      if (imageFile) {
        const reader = new FileReader();
        reader.readAsDataURL(imageFile);
        reader.onloadend = async () => {
          const base64Image = reader.result.split(',')[1]; // Remove the data URL prefix

          const imageData = {
            name: imageName,
            item_id: itemId, // Use the itemId from the created item
            data: base64Image,
          };

          try {
            await axios.post(`${BASE_URL}/images/`, imageData);
            setSuccess('Item and image successfully added!');
          } catch (err) {
            setError('Failed to upload image');
            setSuccess('');
          }
        };
      }

      // Clear form fields after successful item addition
      setName('');
      setPrice('');
      setDescription('');
      setImageName('');
      setImageFile(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Error occurred while adding item');
      setSuccess(''); // Clear success message on error
    }
  };

  return (
    <div className="p-6 bg-white rounded shadow-md">
      <h2 className="text-xl font-bold mb-4">Add New Item</h2>
      {error && <p className="text-red-500">{error}</p>}
      {success && <p className="text-green-500">{success}</p>}
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-sm font-medium">Item Name</label>
          <input
            type="text"
            className="mt-1 p-2 border rounded w-full"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium">Price</label>
          <input
            type="number"
            className="mt-1 p-2 border rounded w-full"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            required
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium">Description</label>
          <textarea
            className="mt-1 p-2 border rounded w-full"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium">Choose Image</label>
          <input
            type="file"
            className="mt-1 p-2 border rounded w-full"
            onChange={handleFileChange}
            required
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium">Image Name</label>
          <input
            type="text"
            className="mt-1 p-2 border rounded w-full"
            value={imageName}
            onChange={(e) => setImageName(e.target.value)}
            required
          />
        </div>

        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Add Item and Upload Image
        </button>
      </form>
    </div>
  );
};

export default ItemForm;
