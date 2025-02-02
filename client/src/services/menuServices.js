import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000/api/menu";

export const getMenu = async () => {
  try {
    const response = await axios.get(API_BASE_URL);
    return response.data;
  } catch (error) {
    console.error("Error fetching menu:", error);
    return [];
  }
};
