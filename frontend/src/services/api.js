import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const getParkingGrid = (lotName, level) => {
    const url = `${API_BASE_URL}/parking_grid/${encodeURIComponent(lotName)}/`;
    return axios.get(url, { params: { level } });
};

export const initializeParkingLot = (lotName) => {
    const url = `${API_BASE_URL}/initialize/${encodeURIComponent(lotName)}/`;
    return axios.get(url);
};

export const startSimulation = (lotName, duration_seconds, update_interval, arrival_rate, departure_rate) => {
    const url = `${API_BASE_URL}/simulation/start/${encodeURIComponent(lotName)}/`;
    return axios.post(url, {
        duration_seconds,
        update_interval,
        arrival_rate,
        departure_rate
    });
};

export const stopSimulation = (lotName) => {
    const url = `${API_BASE_URL}/simulation/stop/${encodeURIComponent(lotName)}/`;
    return axios.post(url);
};

export const parkVehicle = (lotName, vehicle_id, preferred_level) => {
    const url = `${API_BASE_URL}/park/`;
    return axios.post(url, {
        lot_name: lotName,
        vehicle_id,
        preferred_level
    });
};

export const removeVehicle = (lotName, vehicle_id) => {
    const url = `${API_BASE_URL}/remove/`;
    return axios.post(url, {
        lot_name: lotName,
        vehicle_id
    });
};

export const getParkingLots = () => {
    const url = `${API_BASE_URL}/parking_lots/`;
    return axios.get(url);
};
