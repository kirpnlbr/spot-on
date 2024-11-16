import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/';

export const initializeParkingLot = (spots) => {
  return axios.post(`${API_BASE_URL}initialize/`, spots);
};

export const parkVehicle = (vehicleId, preferredLevel) => {
  return axios.post(`${API_BASE_URL}park/`, {
    vehicle_id: vehicleId,
    preferred_level: preferredLevel,
  });
};

export const removeVehicle = (vehicleId) => {
  return axios.post(`${API_BASE_URL}remove/`, {
    vehicle_id: vehicleId,
  });
};

export const getStatus = () => {
  return axios.get(`${API_BASE_URL}status/`);
};

export const getParkingGrid = async (lotName, level) => {
  try {
    console.log(`API call: Fetching parking grid for ${lotName}, Level: ${level}`);
    const response = await axios.get(`${API_BASE_URL}parking_grid/${encodeURIComponent(lotName)}/?level=${level}`);
    console.log('Raw API Response:', response); // Debugging
    return response;
  } catch (error) {
    console.error('Error in getParkingGrid API call:', error);
    throw error;
  }
};


export const getParkingLots = () => {
    return axios.get(`${API_BASE_URL}parking_lots/`);
  };
  