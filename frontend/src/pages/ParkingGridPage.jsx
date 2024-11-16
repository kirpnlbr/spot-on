import React, { useState, useEffect } from 'react';
import ParkingGrid from "../components/parking/ParkingGrid";
import { getParkingGrid } from "../services/api";
import { ArrowLeftIcon } from "@radix-ui/react-icons";

function ParkingGridPage({ lot, onBack }) {
    const [parkingGrid, setParkingGrid] = useState([]);
    const [selectedLevel, setSelectedLevel] = useState(1);

    const levels = [1, 2, 3, 4, 5]; // replace for kodi

    useEffect(() => {
        getParkingGrid(lot.name)
            .then(response => setParkingGrid(response.data.spots))
            .catch(error => console.error("Failed to fetch parking grid:", error));
    }, [lot]);

    return (
        <div class="flex flex-col space-y-4 bg-white min-h-screen">
            {/* Header */}
            <div class="flex p-4 items-center border-b shadow-sm">
                <button onClick={onBack}>
                    <ArrowLeftIcon />
                </button>
                <span class="ml-2 text-lg font-semibold text-gray-900">{lot.name}</span>
            </div>

            {/* Level Selector */}
            <div class="px-5">
                <p class="text-gray-500 text-sm font-medium mb-1.5">Current level</p>
                <div class="flex gap-2 p-1 bg-gray-100 rounded-lg overflow-x-auto shadow-sm">
                    {levels.map((level) => (
                        <button
                            key={level}
                            onClick={() => setSelectedLevel(level)}
                            class={`
                                flex-1 px-4 py-2 font-medium transition-colors rounded-md whitespace-nowrap
                                ${selectedLevel == level
                                    ? "bg-white text-blue-700"
                                    : "text-gray-500 hover:text-gray-900"
                                }
                            `}
                        >
                            L{level}
                        </button>
                    ))}

                </div>
            </div>

            {/* Parking Grid */}
            <div class="mx-4 p-5 rounded-xl border-[1.5px] border-gray-100 shadow-sm">
                <p class="text-gray-500 text-sm font-medium mb-2">Parking layout</p>
                <ParkingGrid parkingGrid={parkingGrid} />
            </div>

            {/* Navigate to Spot */}
            <div class="mx-4 p-4 rounded-xl bg-gray-100 border-[1.5px] border-gray-200 shadow-sm">
                <div class="flex flex-col">
                    <span class="font-medium text-sm text-gray-500">Nearest spot found!</span>
                    <span class="font-bold text-lg text-gray-800 pb-4">A4</span>
                    <button class="rounded-xl p-3 bg-blue-700 border-[1.5px] border-blue-500 text-white font-medium w-full hover:bg-blue-600">
                        Navigate to Spot
                    </button>
                </div>
            </div>

        </div>
    );
}

export default ParkingGridPage;
