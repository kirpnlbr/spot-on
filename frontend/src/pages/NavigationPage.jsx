import { nearestSpot } from "../data/mockData"
import { ArrowLeftIcon } from "@radix-ui/react-icons";
import { Navigation } from 'lucide-react';
import { Map } from "../components/parking/Map"

function NavigationPage({ onBack, selectedLot }) {

    const spot = nearestSpot[0];

    return (
        <div class="flex flex-col space-y-4 bg-white min-h-screen">
            {/* Header */}
            <div class="flex flex-col space-y-6 p-4 border-b shadow-sm bg-[#068ef1]">
                <div class="flex items-center">
                    <button
                        onClick={onBack}
                        class="text-white"
                    >
                        <ArrowLeftIcon class="h-4 w-4" />
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
            <div class="px-4 rounded-xl">
                <Map />
            </div>

            {/* Path Info */}
            <div class="flex flex-col space-y-2 px-4">
                <div class="rounded-xl bg-gray-100 border border-gray-200 p-4 flex flex-col">
                    <span class="font-medium text-sm text-gray-500">Distance</span>
                    <span class="font-bold text-lg text-gray-800">{spot.distance}</span>
                </div>
                <div class="rounded-xl bg-gray-100 border border-gray-200 p-4 flex flex-col">
                    <span class="font-medium text-sm text-gray-500">Estimated time</span>
                    <span class="font-bold text-lg text-gray-800">{spot.estimatedTime}</span>
                </div>
                <button class="rounded-xl p-3 bg-[#068ef1] text-white font-medium w-full">I've Arrived</button>
            </div>
        </div>
    );
}

export default NavigationPage;