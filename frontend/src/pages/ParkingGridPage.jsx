import React, { useState, useEffect } from 'react';
import ParkingGrid from '../components/parking/ParkingGrid';
import { getParkingGrid, startSimulation, stopSimulation } from '../services/api';
import { ArrowLeft } from 'lucide-react';
import { motion } from 'framer-motion';

function ParkingGridPage({ lot, onBack, onNavigate }) {
    const [parkingGrid, setParkingGrid] = useState([]);
    const [selectedLevel, setSelectedLevel] = useState(1);
    const [levels, setLevels] = useState([1]);
    const [isLoading, setIsLoading] = useState(false);
    const [nearestSpotId, setNearestSpotId] = useState(null);
    const [entryPoint, setEntryPoint] = useState(null);

    // Function to fetch parking grid data
    const fetchParkingGrid = () => {
        setIsLoading(true);
        getParkingGrid(lot.name, selectedLevel)
            .then(response => {
                console.log('Parking grid data:', response.data);

                // Set parking grid if available
                if (response.data.spots) {
                    setParkingGrid(response.data.spots);
                } else {
                    console.error('No spots key in API response:', response.data);
                }

                // Set nearest spot ID
                if (response.data.nearest_spot_id && response.data.nearest_spot_id !== "N/A") {
                    setNearestSpotId(response.data.nearest_spot_id);
                } else {
                    setNearestSpotId(null);
                    console.warn('No nearest_spot_id in API response.');
                }

                // Set entry point
                if (response.data.entry_point && Array.isArray(response.data.entry_point)) {
                    setEntryPoint(response.data.entry_point);
                } else {
                    setEntryPoint(null);
                    console.warn('No entry_point in API response.');
                }

                // Update levels based on the parking lot's number of levels
                if (response.data.level_layouts) {
                    const numLevels = Object.keys(response.data.level_layouts).length;
                    setLevels(Array.from({ length: numLevels }, (_, i) => i + 1));
                } else {
                    console.warn('No level_layouts in API response.');
                }
            })
            .catch(error => {
                console.error('Failed to fetch parking grid:', error);
            })
            .finally(() => {
                setIsLoading(false);
            });
    };

    // Effect to handle lot changes
    useEffect(() => {
        if (lot) {
            // Start the simulation when the page loads
            startSimulation(lot.name)
                .then(response => {
                    console.log('Simulation started:', response.data);
                })
                .catch(error => {
                    console.error('Failed to start simulation:', error);
                });

            // Fetch initial parking grid data
            fetchParkingGrid();

            // Set up polling to fetch parking grid data every 2 seconds
            const intervalId = setInterval(() => {
                fetchParkingGrid();
            }, 2000);

            // Cleanup function to stop simulation when the component unmounts
            return () => {
                stopSimulation(lot.name)
                    .then(response => {
                        console.log('Simulation stopped:', response.data);
                    })
                    .catch(error => {
                        console.error('Failed to stop simulation:', error);
                    });

                // Clear the interval
                clearInterval(intervalId);
            };
        }
    }, [lot, selectedLevel]); // Added selectedLevel to dependencies

    return (
        <div className="flex flex-col space-y-4 h-screen overflow-y-auto pb-24">
            {/* Header */}
            <div className="bg-white flex p-4 items-center border-b shadow-sm">
                <button onClick={onBack} className="hover:bg-gray-800/10 p-2 rounded-full transition-colors">
                    <ArrowLeft />
                </button>
                <span className="ml-2 text-lg font-semibold text-gray-900">{lot.name}</span>
            </div>

            {/* Level Selector */}
            {lot.is_multi_level && (
                <div className="px-5 mb-4">
                    <div className="flex p-1 bg-[#e3e2e2] rounded-lg relative shadow-sm">
                        <motion.div
                            className="absolute inset-[4px] bg-white rounded-md"
                            initial={false}
                            animate={{
                                x: selectedLevel === 2 ? 'calc(100% - 8px)' : '0%',
                                width: '50%'
                            }}
                            transition={{
                                type: "spring",
                                stiffness: 360,
                                damping: 30
                            }}
                        />
                        {levels.map(level => (
                            <motion.button
                                key={level}
                                onClick={() => setSelectedLevel(level)}
                                className={`relative flex-1 px-4 py-1.5 font-medium text-sm rounded-md whitespace-nowrap ${selectedLevel === level
                                    ? 'text-[#068ef1]'
                                    : 'text-gray-500 hover:text-gray-900'
                                    }`}
                                whileTap={{ scale: 0.95 }}
                            >
                                Level {level}
                            </motion.button>
                        ))}
                    </div>
                </div>
            )}


            {/* Parking Grid */}
            <div className="bg-white mx-3 p-5 rounded-xl border-[1.5px] border-gray-100 shadow-sm">
                {isLoading ? (
                    <div className="text-center text-gray-500">Loading parking grid...</div>
                ) : (
                    <ParkingGrid parkingGrid={parkingGrid} nearestSpotId={nearestSpotId} />
                )}
            </div>

            {/* Navigate to Spot */}
            <div className="mx-3 p-4 rounded-xl bg-[#d3e4f0] shadow-sm">
                <div className="flex flex-col">
                    <span className="font-medium text-sm text-gray-600">Nearest spot found!</span>
                    <span className="font-bold text-xl text-gray-800 pb-4">
                        {nearestSpotId ? nearestSpotId.split('-')[1] : 'N/A'}
                    </span>
                    <button
                        onClick={() => {
                            if (nearestSpotId && entryPoint) {
                                onNavigate(nearestSpotId, entryPoint, lot.name, selectedLevel);
                            } else {
                                alert('No available spot to navigate.');
                            }
                        }}
                        className={`rounded-xl p-3 text-white font-medium w-full active:scale-95 transition
                            ${nearestSpotId
                                ? 'bg-[#068ef1] hover:bg-[#1F9FFC]'
                                : 'bg-gray-400 cursor-not-allowed'
                            }`}
                        disabled={!nearestSpotId}
                        title={nearestSpotId ? `Spot ID: ${nearestSpotId}` : 'No available spot'}
                    >
                        Navigate to Spot
                    </button>

                    {/* Debug Information */}
                    <div className="mt-4 text-xs text-gray-400">
                        <p>Nearest Spot ID: {nearestSpotId || 'N/A'}</p>
                        <p>Entry Point: {entryPoint ? `(${entryPoint[0]}, ${entryPoint[1]})` : 'N/A'}</p>
                    </div>
                </div>
            </div>
        </div>
    );

}

export default ParkingGridPage;
