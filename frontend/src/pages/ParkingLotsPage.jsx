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
        <div class="flex flex-col h-screen">
            <div class="p-4 shadow-sm border-b border-[#E5E3DD]">
                <input
                    type="text"
                    placeholder="Search parking lot..."
                    class="border-[1px] border-gray-200 bg-gray-50 w-full p-3 rounded-lg"
                />
            </div>

            <div className="flex-1 overflow-y-auto pb-24">
                <ParkingLots onSelectLot={onSelectLot} parkingLots={parkingData} />
            </div>
        </div>
    );
}

export default ParkingLotsPage;
