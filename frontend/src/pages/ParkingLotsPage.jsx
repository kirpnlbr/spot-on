import React, { useEffect, useState } from 'react';
import ParkingLots from "../components/parking/ParkingLots";
import { getParkingLots } from "../services/api";

function ParkingLotsPage({ onSelectLot }) {
    const [parkingData, setParkingData] = useState([]);

    useEffect(() => {
        getParkingLots()
            .then(response => {
                console.log("Fetched Parking Lots:", response.data);
                setParkingData(response.data);
            })
            .catch(error => console.error("Failed to fetch parking lots:", error));
    }, []);

    return (
        <div className="flex flex-col bg-white min-h-screen">
            <div className="p-4 shadow-sm border-b">
                <input
                    type="text"
                    placeholder="Search parking lot..."
                    className="border-[1.5px] border-gray-200 bg-gray-50 w-full p-3 rounded-lg"
                />
            </div>

            <ParkingLots onSelectLot={onSelectLot} parkingLots={parkingData} />
        </div>
    );
}

export default ParkingLotsPage;
