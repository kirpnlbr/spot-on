import { nearestSpot } from "../data/mockData"
import { Navigation, ArrowLeft } from 'lucide-react';
import { NavigationMap } from "../components/parking/Map"

function NavigationPage({ onBack, selectedLot }) {

    const spot = nearestSpot[0];

    return (
        <div class="flex flex-col space-y-4 bg-white h-screen overflow-y-auto">
            {/* Header */}
            <div class="flex flex-col space-y-6 px-4 pt-4 pb-5 border-b shadow-sm bg-[#068ef1] sticky top-0 z-10 rounded-b-lg">
                <div class="flex items-center gap-3">
                    <button
                        onClick={onBack}
                        class="text-white hover:bg-white/10 p-2 rounded-full transition-colors"
                    >
                        <ArrowLeft />
                    </button>
                    <span class="ml-2 text-lg font-semibold text-white">Navigation</span>
                </div>
                <div class="flex justify-between items-center">
                    <div class="flex flex-col text-white">
                        <span class="font-medium text-sm">Your spot</span>
                        <span class="font-bold text-2xl">{spot.spot}</span>
                    </div>
                    <Navigation class="text-white h-6 w-6 mt-4" />
                </div>
            </div>

            {/* Map */}
            <div class="px-4 rounded-xl h-[400px]">
                <NavigationMap />
            </div>

            {/* Path Info */}
            <div class="flex flex-col px-4 pb-28">
                <div class="space-y-2">
                    <div class="rounded-xl bg-[#d3e4f0] p-4 flex flex-col">
                        <span class="font-medium text-sm text-gray-600">Distance</span>
                        <span class="font-bold text-lg text-gray-800">{spot.distance}</span>
                    </div>
                    <div class="rounded-xl bg-[#d3e4f0] p-4 flex flex-col">
                        <span class="font-medium text-sm text-gray-600">Estimated time</span>
                        <span class="font-bold text-lg text-gray-800">{spot.estimatedTime}</span>
                    </div>
                </div>
                <button class="rounded-xl p-3 bg-[#068ef1] mt-4 text-white font-medium w-full">I've Arrived</button>
            </div>
        </div>
    );
}

export default NavigationPage;