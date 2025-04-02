import axios from "axios";

const API_BASE_URL = "http://192.168.1.59:5000/api/categories";

export const getCategories = async () => {
  try {
    const response = await axios.get(API_BASE_URL);
    return response.data;
  } catch (error) {
    console.error("Error fetching categories:", error);
    return [];
  }
};
