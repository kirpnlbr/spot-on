import React, { useState } from 'react';
import ParkingLots from "../components/parking/ParkingLots";
import { parkingLots } from "../data/mockData"; // Import mock data

function ParkingLotsPage({ onSelectLot }) {
    const [parkingData] = useState(parkingLots); // Use mock data for parking lots

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
            <ParkingLots onSelectLot={onSelectLot} parkingLots={parkingData} />
        </div>
    );
}

export default ParkingLotsPage;
