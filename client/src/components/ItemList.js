import React, { useState } from 'react';
import axios from 'axios';

const ImageUpload = ({ itemId }) => {
  const [imageName, setImageName] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!imageFile || !imageName) {
      setError('Please provide an image name and file.');
      return;
    }

    const reader = new FileReader();
    reader.readAsDataURL(imageFile);
    reader.onloadend = async () => {
      const base64Image = reader.result.split(',')[1]; // Removing the data URL prefix

      const imageData = {
        name: imageName,
        item_id: itemId,
        data: base64Image,
      };

      try {
        await axios.post('/api/images', imageData);
        setSuccess(true);
        setError('');
      } catch (err) {
        setError('Failed to upload image');
        setSuccess(false);
      }
    };
  };

  return (
    <div className="p-6 bg-white rounded shadow-md">
      <h2 className="text-xl font-bold mb-4">Upload Image</h2>
      {success && (
        <p className="text-green-500">Image uploaded successfully!</p>
      )}
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleSubmit}>
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

        <div className="mb-4">
          <label className="block text-sm font-medium">Choose Image</label>
          <input
            type="file"
            className="mt-1 p-2 border rounded w-full"
            onChange={handleFileChange}
            required
          />
        </div>

        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Upload Image
        </button>
      </form>
    </div>
  );
};

export default ImageUpload;
