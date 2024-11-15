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

export const getParkingGrid = (lotName) => {
    return axios.get(`${API_BASE_URL}parking_grid/${lotName}/`);
  };

export const getParkingLots = () => {
    return axios.get(`${API_BASE_URL}parking_lots/`);
  };
  