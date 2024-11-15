import React, { useState, useEffect } from 'react';
import ParkingGrid from "../components/parking/ParkingGrid";
import { getStatus } from "../services/api"; // Fetch parking lot status
import { ArrowLeftIcon } from "@radix-ui/react-icons";

function ParkingGridPage({ lot, onBack }) {
    const [parkingGrid, setParkingGrid] = useState([]);

    useEffect(() => {
        // Fetch and filter data for the selected lot/level
        getStatus()
            .then(response => {
                const selectedLevelData = response.data.spots_by_level[lot.level];
                setParkingGrid(selectedLevelData);
            })
            .catch(error => {
                console.error("Failed to fetch parking grid:", error);
            });
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
        </div>
    );
}

export default ParkingGridPage;
