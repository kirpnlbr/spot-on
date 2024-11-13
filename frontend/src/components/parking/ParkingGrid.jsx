import { parkingGrid } from "../../data/mockData"

function ParkingGrid({ selectedLot }) {

    const parkingLot = parkingGrid.find(grid => grid.name === selectedLot.name);

    if (!parkingLot) return null;

    return (
        <div class="grid grid-cols-5 gap-3">
            {parkingLot.spots.map((spot) => (
                <div
                    key={spot.id}
                    class={`
                        aspect-square rounded-lg flex items-center justify-center
                        ${spot.isOccupied
                            ? 'bg-gray-200 text-gray-500' // Occupied spot
                            : 'border-[1.5px] border-blue-600 text-blue-600'} // Available spot
            `}
                >
                    {spot.id}
                </div>
            ))}
        </div>
    );
}

export default ParkingGrid;