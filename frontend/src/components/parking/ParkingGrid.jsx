function ParkingGrid({ parkingGrid }) {
    if (!parkingGrid) return null;

    return (
        <div className="grid grid-cols-5 gap-3">
            {parkingGrid.map((spot) => (
                <div
                    key={spot.id}
                    className={`
                        aspect-square rounded-lg flex items-center justify-center
                        ${spot.is_occupied
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
