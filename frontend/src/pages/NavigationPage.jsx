import React, { useState, useEffect } from 'react';
import { Navigation, ArrowLeft } from 'lucide-react';
import { NavigationMap } from '../components/parking/Map';
import { getParkingGrid } from '../services/api';

function NavigationPage({ onBack, nearestSpotId, entryPoint, lotName, selectedLevel }) {
    const [currentNearestSpotId, setCurrentNearestSpotId] = useState(nearestSpotId);
    const [distance, setDistance] = useState('Calculating...');
    const [estimatedTime, setEstimatedTime] = useState('Calculating...');

    // Function to fetch the latest nearest spot
    const fetchNearestSpot = () => {
        getParkingGrid(lotName, selectedLevel)
            .then(response => {
                if (response.data.nearest_spot_id) {
                    setCurrentNearestSpotId(response.data.nearest_spot_id);
                } else {
                    setCurrentNearestSpotId('N/A');
                }
                // Update distance and estimated time if needed
                // For now, we'll mock these values
                setDistance('200 meters');
                setEstimatedTime('3 mins');
            })
            .catch(error => {
                console.error('Failed to fetch parking grid:', error);
            });
    };

    // Set up polling to fetch the nearest spot every 2 seconds
    useEffect(() => {
        fetchNearestSpot();
        const intervalId = setInterval(() => {
            fetchNearestSpot();
        }, 2000);

        return () => {
            clearInterval(intervalId);
        };
    }, [lotName, selectedLevel]);

    return (
        <div className="flex flex-col space-y-4 bg-white h-screen overflow-y-auto">
            {/* Header */}
            <div className="flex flex-col space-y-6 px-4 pt-4 pb-5 border-b shadow-sm bg-[#068ef1] sticky top-0 z-10 rounded-b-lg">
                <div className="flex items-center gap-3">
                    <button
                        onClick={onBack}
                        className="text-white hover:bg-white/10 p-2 rounded-full transition-colors"
                    >
                        <ArrowLeft />
                    </button>
                    <span className="ml-2 text-lg font-semibold text-white">Navigation</span>
                </div>
                <div className="flex justify-between items-center">
                    <div className="flex flex-col text-white">
                        <span className="font-medium text-sm">Your spot</span>
                        <span className="font-bold text-2xl">{currentNearestSpotId ? currentNearestSpotId.split('-')[1] : 'N/A'}</span>
                    </div>
                    <Navigation className="text-white h-6 w-6 mt-4" />
                </div>
            </div>

            {/* Map */}
            <div className="px-4 rounded-xl h-[400px]">
                <NavigationMap />
            </div>

            {/* Path Info */}
            <div className="flex flex-col px-4 pb-28">
                <div className="space-y-2">
                    <div className="rounded-xl bg-[#f8f8f7] border border-gray-200 p-4 flex flex-col">
                        <span className="font-medium text-sm text-gray-500">Distance</span>
                        <span className="font-bold text-lg text-gray-800">{distance}</span>
                    </div>
                    <div className="rounded-xl bg-[#f8f8f7] border border-gray-200 p-4 flex flex-col">
                        <span className="font-medium text-sm text-gray-500">Estimated time</span>
                        <span className="font-bold text-lg text-gray-800">{estimatedTime}</span>
                    </div>
                </div>
                <button className="rounded-xl p-3 bg-[#068ef1] hover:bg-[#1F9FFC] mt-4 text-white font-medium w-full active:scale-95 transition">I've Arrived</button>
            </div>
        </div>
    );
}

export default NavigationPage;
