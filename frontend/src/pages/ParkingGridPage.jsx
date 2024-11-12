import { parkingGrid } from "../data/mockData"
import ParkingGrid from "../components/parking/ParkingGrid";
import { ArrowLeftIcon } from "@radix-ui/react-icons";

function ParkingGridPage() {
    return (
        <div class="flex flex-col space-y-4 bg-white">
            {/* Header */}
            <div class="flex p-4 items-center border-b shadow-sm">
                <button>
                    <ArrowLeftIcon />
                </button>
                <span class="ml-2 text-lg font-semibold text-gray-900">Central Mall Parking</span>
            </div>

            {/* Parking Grid */}
            <div class="p-4 rounded-md border-[1.5px] border-gray-200"></div>

            {/* Navigation Menu */}
            <div class="p-4 rounded-lg bg-blue-300">
                <div class="flex flex-col">
                    <span class="font-medium text-sm text-gray-600">Nearest spot</span>
                    <span class="font-bold text-lg text-gray-800 pb-4">A4</span>
                    <button class="rounded-md px-3 py-2 bg-blue-700 text-white font-medium w-full hover:bg-blue-600">Navigate to Spot</button>
                </div>
            </div>

        </div>
    );
}

export default ParkingGridPage;