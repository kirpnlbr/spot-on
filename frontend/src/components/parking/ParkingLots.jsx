function ParkingLots({ onSelectLot, parkingLots }) {
    return (
        <div class="flex-1">
            {parkingLots.map((lot) => (
                <div
                    key={lot.id}
                    class="p-4 border-b last:border-b-0 hover:bg-gray-50"
                    onClick={() => onSelectLot(lot)}
                >
                    <a class="flex flex-col gap-1">
                        <h2 class="font-medium text-gray-900">
                            {lot.name}
                        </h2>
                        <p class="text-sm text-blue-500">
                            {lot.distance} <span class="text-gray-500">• {lot.spots}</span>
                        </p>
                    </a>
                </div>
            ))}
        </div>
    );
}

export default ParkingLots;
