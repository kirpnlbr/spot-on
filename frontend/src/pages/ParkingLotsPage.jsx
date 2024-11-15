// frontend/src/pages/ParkingLotsPage.jsx

import React, { useEffect, useState } from 'react';
import ParkingLots from "../components/parking/ParkingLots";
import { getStatus } from "../services/api"; // Import getStatus from api.js

function ParkingLotsPage({ onSelectLot }) {
    const [parkingLots, setParkingLots] = useState([]);

    useEffect(() => {
        // Fetch parking lots data from the backend when the component mounts
        getStatus()
            .then(response => {
                setParkingLots(response.data.spots_by_level); // Assume spots_by_level is grouped by level
            })
            .catch(error => {
                console.error("Failed to fetch parking lots:", error);
            });
    }, []);

    return (
        <div className="flex flex-col bg-white min-h-screen">
            {/* Search */}
            <div className="p-4 shadow-sm border-b">
                <input
                    type="text"
                    placeholder="Search parking lot..."
                    className="border-[1.5px] border-gray-200 bg-gray-50 w-full p-3 rounded-lg"
                />
            </div>

            {/* Parking Lots List */}
            <ParkingLots onSelectLot={onSelectLot} parkingLots={parkingLots} />
        </div>
    );
}

export default ParkingLotsPage;
