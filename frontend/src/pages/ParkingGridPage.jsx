import { parkingGrid } from "../data/mockData"
import ParkingGrid from "../components/parking/ParkingGrid";
import { ArrowLeftIcon } from "@radix-ui/react-icons";

function ParkingGridPage() {

    const parkingLot = parkingGrid[0];

    return (
        <div class="flex flex-col space-y-4 bg-white">
            {/* Header */}
            <div class="flex p-4 items-center border-b shadow-sm">
                <button>
                    <ArrowLeftIcon />
                </button>
                <span class="ml-2 text-lg font-semibold text-gray-900">{parkingLot.name}</span>
            </div>

            {/* Parking Grid */}
            <div class="p-4 rounded-lg border-[1.5px] border-gray-100">
                <ParkingGrid />
            </div>

            {/* Navigate to Spot */}
            <div class="p-4 rounded-lg bg-blue-300 border-[1.5px] border-blue-200">
                <div class="flex flex-col">
                    <span class="font-medium text-sm text-gray-600">Nearest spot</span>
                    <span class="font-bold text-lg text-gray-800 pb-4">A4</span>
                    <button class="rounded-lg px-3 py-2 bg-blue-700 border border-blue-600 text-white font-medium w-full hover:bg-blue-600">Navigate to Spot</button>
                </div>
            </div>

        </div>
    );
}

export default ParkingGridPage;