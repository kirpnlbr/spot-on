function ParkingLots({ onSelectLot, parkingLots }) {
    return (
        <div className="flex-1">
            {parkingLots.map((lot, index) => (
                <div
                    key={index}
                    className="p-4 border-b last:border-b-0 hover:bg-gray-50"
                    onClick={() => onSelectLot(lot)}
                >
                    <a className="flex flex-col gap-1">
                        <h2 className="font-medium text-gray-900">
                            Level {index + 1}
                        </h2>
                        <p className="text-sm text-blue-500">
                            Total Spots: {lot.length}
                            <span className="text-gray-500"> • Occupied: {lot.filter(spot => spot.is_occupied).length}</span>
                        </p>
                    </a>
                </div>
            ))}
        </div>
    );
}

export default ParkingLots;
