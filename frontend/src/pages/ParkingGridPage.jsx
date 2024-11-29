import React, { useState, useEffect } from 'react';
import ParkingGrid from '../components/parking/ParkingGrid';
import { getParkingGrid } from '../services/api';
import { ArrowLeftIcon } from '@radix-ui/react-icons';

function ParkingGridPage({ lot, onBack, onNavigate }) {
    const [parkingGrid, setParkingGrid] = useState([]);
    const [selectedLevel, setSelectedLevel] = useState(1);
    const [levels, setLevels] = useState([1]);

    useEffect(() => {
        if (lot) {
            fetchParkingGrid();
        }
    }, [lot, selectedLevel]);

    const fetchParkingGrid = () => {
        getParkingGrid(lot.name, selectedLevel)
            .then(response => {
                if (response.data.spots) {
                    setParkingGrid(response.data.spots);
                    // Update levels based on the parking lot's number of levels
                    const numLevels = Object.keys(response.data.level_layouts).length;
                    setLevels(Array.from({ length: numLevels }, (_, i) => i + 1));
                    // If the parking lot is not multi-level, set selectedLevel to 1
                    if (!lot.is_multi_level) {
                        setSelectedLevel(1);
                    }
                } else {
                    console.error('No spots key in API response:', response.data);
                }
            })
            .catch(error => {
                console.error('Failed to fetch parking grid:', error);
            });
    };

    return (
        <div class="flex flex-col space-y-4 bg-[#f7f7f5] min-h-screen">
            {/* Header */}
            <div class="bg-white flex p-4 items-center border-b shadow-sm">
                <button onClick={onBack}>
                    <ArrowLeftIcon />
                </button>
                <span class="ml-2 text-lg font-semibold text-gray-900">{lot.name}</span>
            </div>

            {/* Level Selector */}
            {lot.is_multi_level && (
                <div class="px-5">
                    <p class="text-gray-500 text-sm font-medium mb-1.5">Current level</p>
                    <div class="flex gap-2 p-1 bg-[#e3e2e2] rounded-lg overflow-x-auto shadow-sm">
                        {levels.map(level => (
                            <button
                                key={level}
                                onClick={() => setSelectedLevel(level)}
                                class={`flex-1 px-4 py-2 font-medium transition-colors rounded-md whitespace-nowrap ${selectedLevel === level
                                    ? 'bg-white text-[#068ef1]'
                                    : 'text-gray-500 hover:text-gray-900'
                                    }`}
                            >
                                L{level}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Parking Grid */}
            <div class="bg-white mx-3 p-5 rounded-xl border-[1.5px] border-gray-100 shadow-sm">
                <p class="text-gray-500 text-sm font-medium mb-2">Parking layout</p>
                <ParkingGrid parkingGrid={parkingGrid} />
            </div>

            {/* Navigate to Spot */}
            <div class="mx-3 p-4 rounded-xl bg-white border-[1.5px] border-gray-100 shadow-sm">
                <div class="flex flex-col">
                    <span class="font-medium text-sm text-gray-500">Nearest spot found!</span>
                    <span class="font-bold text-lg text-gray-800 pb-4">A4</span>
                    <button
                        onClick={onNavigate}
                        class="rounded-xl p-3 bg-[#068ef1] text-white font-medium w-full"
                    >
                        Navigate to Spot
                    </button>
                </div>
            </div>

        </div>
    );
}

export default ParkingGridPage;
