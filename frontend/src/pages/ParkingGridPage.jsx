import React, { useState, useEffect, useRef } from 'react';
import ParkingGrid from '../components/parking/ParkingGrid';
import { getParkingGrid, startSimulation, stopSimulation } from '../services/api';
import { ArrowLeftIcon } from '@radix-ui/react-icons';

function ParkingGridPage({ lot, onBack, onNavigate }) {
    const [parkingGrid, setParkingGrid] = useState([]);
    const [selectedLevel, setSelectedLevel] = useState(1);
    const [levels, setLevels] = useState([1]);
    const [simulationRunning, setSimulationRunning] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    // useRef to keep track of the latest selectedLevel
    const selectedLevelRef = useRef(selectedLevel);

    // Update the ref whenever selectedLevel changes
    useEffect(() => {
        selectedLevelRef.current = selectedLevel;
    }, [selectedLevel]);

    // Function to fetch parking grid data
    const fetchParkingGrid = () => {
        setIsLoading(true);
        getParkingGrid(lot.name, selectedLevelRef.current)
            .then(response => {
                console.log('Parking grid data:', response.data);
                if (response.data.spots) {
                    setParkingGrid(response.data.spots);
                    // Update levels based on the parking lot's number of levels
                    const numLevels = Object.keys(response.data.level_layouts).length;
                    setLevels(Array.from({ length: numLevels }, (_, i) => i + 1));
                } else {
                    console.error('No spots key in API response:', response.data);
                }
            })
            .catch(error => {
                console.error('Failed to fetch parking grid:', error);
            })
            .finally(() => {
                setIsLoading(false);
            });
    };

    // Effect to handle lot changes: initialize level and start simulation
    useEffect(() => {
        if (lot) {
            // If not multi-level, set selectedLevel to 1 once
            if (!lot.is_multi_level) {
                setSelectedLevel(1);
            } else {
                // If multi-level and current selectedLevel exceeds available levels, reset to 1
                if (levels.length > 0 && selectedLevel > levels.length) {
                    setSelectedLevel(1);
                }
            }

            // Fetch initial parking grid data
            fetchParkingGrid();

            // Start the simulation when the page loads
            startSimulation(lot.name)
                .then(response => {
                    console.log('Simulation started:', response.data);
                    setSimulationRunning(true);
                })
                .catch(error => {
                    console.error('Failed to start simulation:', error);
                });
        }

        // Cleanup function to stop simulation when the component unmounts or lot changes
        return () => {
            if (simulationRunning) { // Only attempt to stop if running
                stopSimulation(lot.name)
                    .then(response => {
                        console.log('Simulation stopped:', response.data);
                        setSimulationRunning(false);
                    })
                    .catch(error => {
                        console.error('Failed to stop simulation:', error);
                    });
            }
        };
    }, [lot]); // Runs when 'lot' changes

    // Effect to handle polling when simulation is running
    useEffect(() => {
        let intervalId;
        if (simulationRunning) {
            // Set up polling to fetch parking grid data every 2 seconds
            intervalId = setInterval(() => {
                fetchParkingGrid();
            }, 2000);
        }

        // Cleanup interval on component unmount or when simulation stops
        return () => {
            if (intervalId) {
                clearInterval(intervalId);
            }
        };
    }, [simulationRunning]); // Runs when 'simulationRunning' changes

    // Effect to handle level changes: fetch new data when level changes
    useEffect(() => {
        if (lot) {
            fetchParkingGrid();
        }
    }, [selectedLevel]); // Runs when 'selectedLevel' changes

    return (
        <div className="flex flex-col space-y-4 bg-gray-100 min-h-screen">
            {/* Header */}
            <div className="bg-white flex p-4 items-center border-b shadow-sm">
                <button onClick={onBack}>
                    <ArrowLeftIcon />
                </button>
                <span className="ml-2 text-lg font-semibold text-gray-900">{lot.name}</span>
            </div>

            {/* Level Selector */}
            {lot.is_multi_level && (
                <div className="px-5">
                    <p className="text-gray-500 text-sm font-medium mb-1.5">Current level</p>
                    <div className="flex gap-2 p-1 bg-gray-200 rounded-lg overflow-x-auto shadow-sm">
                        {levels.map(level => (
                            <button
                                key={level}
                                onClick={() => setSelectedLevel(level)}
                                className={`flex-1 px-4 py-2 font-medium transition-colors rounded-md whitespace-nowrap ${
                                    selectedLevel === level
                                        ? 'bg-white text-blue-700'
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
            <div className="bg-white mx-3 p-5 rounded-xl border-[1.5px] border-gray-100 shadow-sm">
                <p className="text-gray-500 text-sm font-medium mb-2">Parking layout</p>
                {isLoading ? (
                    <div className="text-center text-gray-500">Loading parking grid...</div>
                ) : (
                    <ParkingGrid parkingGrid={parkingGrid} />
                )}
            </div>

            {/* Navigate to Spot */}
            <div className="mx-3 p-4 rounded-xl bg-white border-[1.5px] border-gray-100 shadow-sm">
                <div className="flex flex-col">
                    <span className="font-medium text-sm text-gray-500">Nearest spot found!</span>
                    <span className="font-bold text-lg text-gray-800 pb-4">A4</span>
                    <button
                        onClick={onNavigate}
                        className="rounded-xl p-3 bg-blue-700 border-[1.5px] border-blue-500 text-white font-medium w-full hover:bg-blue-600"
                    >
                        Navigate to Spot
                    </button>
                </div>
            </div>
        </div>
    );

}

export default ParkingGridPage;
