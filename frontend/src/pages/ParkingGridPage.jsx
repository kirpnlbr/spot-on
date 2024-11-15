import React, { useState, useEffect } from 'react';
import ParkingGrid from "../components/parking/ParkingGrid";
import { getParkingGrid } from "../services/api"; // Import API function for the backend
import { ArrowLeftIcon } from "@radix-ui/react-icons";

function ParkingGridPage({ lot, onBack }) {
    const [parkingGrid, setParkingGrid] = useState([]);

    useEffect(() => {
        getParkingGrid(lot.name)
            .then(response => setParkingGrid(response.data.spots))
            .catch(error => console.error("Failed to fetch parking grid:", error));
    }, [lot]);

    return (
        <div className="flex flex-col space-y-4 bg-white min-h-screen">
            {/* Header */}
            <div className="flex p-4 items-center border-b shadow-sm">
                <button onClick={onBack}>
                    <ArrowLeftIcon />
                </button>
                <span className="ml-2 text-lg font-semibold text-gray-900">{lot.name}</span>
            </div>

            {/* Parking Grid */}
            <div className="p-5 rounded-xl border-[1.5px] border-gray-100 shadow-sm">
                <ParkingGrid parkingGrid={parkingGrid} />
            </div>

            {/* Navigate to Spot */}
            <div className="p-4 rounded-xl bg-gray-100 border-[1.5px] border-gray-200 shadow-sm">
                <div className="flex flex-col">
                    <span className="font-medium text-sm text-gray-500">Nearest spot found!</span>
                    <span className="font-bold text-lg text-gray-800 pb-4">A4</span>
                    <button className="rounded-xl p-3 bg-blue-700 border-[1.5px] border-blue-500 text-white font-medium w-full hover:bg-blue-600">
                        Navigate to Spot
                    </button>
                </div>
            </div>

        </div>
    );
}

export default ParkingGridPage;
