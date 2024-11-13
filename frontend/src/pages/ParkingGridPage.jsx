import { parkingGrid } from "../data/mockData"
import ParkingGrid from "../components/parking/ParkingGrid";
import { ArrowLeftIcon } from "@radix-ui/react-icons";

function ParkingGridPage({ lot, onBack }) {

    const parkingLot = parkingGrid[0];

    return (
        <div class="flex flex-col space-y-4 bg-white min-h-screen">
            {/* Header */}
            <div class="flex p-4 items-center border-b shadow-sm">
                <button onClick={onBack}>
                    <ArrowLeftIcon />
                </button>
                <span class="ml-2 text-lg font-semibold text-gray-900">{lot.name}</span>
            </div>

            {/* Parking Grid */}
            <div class="p-5 rounded-xl border-[1.5px] border-gray-100 shadow-sm">
                <ParkingGrid selectedLot={lot} />
            </div>

            {/* Navigate to Spot */}
            <div class="p-4 rounded-xl bg-gray-100 border-[1.5px] border-gray-200 shadow-sm">
                <div class="flex flex-col">
                    <span class="font-medium text-sm text-gray-500">Nearest spot found!</span>
                    <span class="font-bold text-lg text-gray-800 pb-4">A4</span>
                    <button class="rounded-xl p-3 bg-blue-700 border-[1.5px] border-blue-500 text-white font-medium w-full hover:bg-blue-600">Navigate to Spot</button>
                </div>
            </div>

        </div>
    );
}

export default ParkingGridPage;