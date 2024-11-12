import { parkingGrid } from "../data/mockData"
import ParkingGrid from "../components/parking/ParkingGrid";
import { ArrowLeftIcon } from "@radix-ui/react-icons";

function ParkingGridPage() {
    return (
        <div class="flex flex-col bg-white">
            {/* Header */}
            <div class="flex p-4 items-center">
                <button>
                    <ArrowLeftIcon />
                </button>
                <span class="ml-2 text-lg font-semibold text-gray-900">Central Mall Parking</span>
            </div>

            {/* Parking Grid */}
            <ParkingGrid />

            {/* Navigation Menu */}
            <div class="flex flex-col p-4 rounded-lg bg-blue-300">
                <span class="font-medium text-sm text-gray-600">Nearest spot</span>
                <span class="font-bold text-lg text-gray-800 pb-4">A4</span>
                <button class="rounded-md px-3 py-2 bg-blue-700 text-white font-medium w-full hover:bg-blue-600">Navigate to Spot</button>
            </div>

        </div>
    );
}

export default ParkingGridPage;