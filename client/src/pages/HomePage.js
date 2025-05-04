import React, { useEffect, useState } from 'react';
import FoodSection from '../components/FoodSection';
import { BASE_URL } from '../services/api'; // Import the BASE_URL/api url from api.js
const HomePage = () => {
  const [foodData, setFoodData] = useState([]); // State to hold fetched food items with images
  const [loading, setLoading] = useState(true); // To manage loading state
  const [error, setError] = useState(null); // To handle errors

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch food items
        const foodResponse = await fetch(`${BASE_URL}/items/`);
        if (!foodResponse.ok) {
          throw new Error('Failed to fetch food data');
        }
        const foodData = await foodResponse.json();

        // Fetch list of images
        const imageResponse = await fetch(`${BASE_URL}/images/`);
        if (!imageResponse.ok) {
          throw new Error('Failed to fetch images');
        }
        const imageList = await imageResponse.json();

        // Fetch actual image data one by one
        const imagePromises = imageList.map(async (image) => {
          const imageDetailResponse = await fetch(
            `${BASE_URL}/images/${image.id}`,
          );
          if (!imageDetailResponse.ok) {
            return null;
          }
          return imageDetailResponse.json();
        });

        // Wait for all image data to be fetched
        const imageDetails = await Promise.all(imagePromises);

        // Combine food items with images based on item_id
        const combinedData = foodData.map((foodItem) => {
          const itemImages = imageDetails
            .filter((image) => image && image.item_id === foodItem.id)
            .map((image) => ({
              id: image.id,
              name: image.name,
              data: image.data, // Base64 image data
            }));

          return {
            ...foodItem,
            images: itemImages.length > 0 ? itemImages : null,
          };
        });

        setFoodData(combinedData); // Set combined data to state
        setLoading(false); // Set loading to false when data is fetched
      } catch (error) {
        setError(error.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>; // Display loading text until data is fetched
  }

  if (error) {
    return <div>Error: {error}</div>; // Display error message if any error occurs
  }

  return (
    <div className="pt-24">
      <h1 className="text-3xl font-bold text-center mb-10">Our Special Menu</h1>
      <FoodSection title="" foodItems={foodData} />
    </div>
  );
};

export default HomePage;
