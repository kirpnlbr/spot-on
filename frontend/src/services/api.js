import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/';

/**
 * Initialize a specific parking lot with a new configuration.
 * @param {string} lotName - The name of the parking lot to initialize.
 */
export const initializeParkingLot = (lotName) => {
  return axios.get(`${API_BASE_URL}initialize/${encodeURIComponent(lotName)}/`);
};

/**
 * Park a vehicle in a specific parking lot.
 * @param {string} lotName - The name of the parking lot.
 * @param {string} vehicleId - The ID of the vehicle.
 * @param {number} preferredLevel - The preferred level for parking.
 */
export const parkVehicle = (lotName, vehicleId, preferredLevel) => {
  return axios.post(`${API_BASE_URL}park/`, {
    lot_name: lotName, // Include lot_name in the request data
    vehicle_id: vehicleId,
    preferred_level: preferredLevel,
  });
};

/**
 * Remove a vehicle from a specific parking lot.
 * @param {string} lotName - The name of the parking lot.
 * @param {string} vehicleId - The ID of the vehicle to remove.
 */
export const removeVehicle = (lotName, vehicleId) => {
  return axios.post(`${API_BASE_URL}remove/`, {
    lot_name: lotName, // Include lot_name in the request data
    vehicle_id: vehicleId,
  });
};

/**
 * Get the current status of a specific parking lot.
 * @param {string} lotName - The name of the parking lot.
 */
export const getStatus = (lotName) => {
  return axios.get(`${API_BASE_URL}status/${encodeURIComponent(lotName)}/`);
};

/**
 * Fetch the parking grid data for a specific lot and level.
 * @param {string} lotName - The name of the parking lot.
 * @param {number} level - The level number to fetch data for.
 */
export const getParkingGrid = async (lotName, level) => {
  try {
    console.log(`API call: Fetching parking grid for ${lotName}, Level: ${level}`);
    const response = await axios.get(`${API_BASE_URL}parking_grid/${encodeURIComponent(lotName)}/`, {
      params: { level },
    });
    console.log('Raw API Response:', response); // Debugging
    return response;
  } catch (error) {
    console.error('Error in getParkingGrid API call:', error);
    throw error;
  }
};

/**
 * Retrieve a list of all parking lots.
 */
export const getParkingLots = () => {
  return axios.get(`${API_BASE_URL}parking_lots/`);
};

/**
 * Start the simulation for a specific parking lot.
 * @param {string} lotName - The name of the parking lot.
 */
export const startSimulation = async (lotName) => {
  try {
    const response = await axios.post(`${API_BASE_URL}simulation/start/${encodeURIComponent(lotName)}/`);
    return response;
  } catch (error) {
    console.error('Error in startSimulation API call:', error);
    throw error;
  }
};

/**
 * Stop the simulation for a specific parking lot.
 * @param {string} lotName - The name of the parking lot.
 */
export const stopSimulation = async (lotName) => {
  try {
    const response = await axios.post(`${API_BASE_URL}simulation/stop/${encodeURIComponent(lotName)}/`);
    return response;
  } catch (error) {
    console.error('Error in stopSimulation API call:', error);
    throw error;
  }
};
