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
                        <h2 class="font-medium text-gray-800">
                            {lot.name}
                        </h2>
                        <p class="text-sm text-[#068ef1]">
                            {lot.distance} <span class="text-gray-600">• {lot.spots}</span>
                        </p>
                        <p class="text-xs mt-3 font-medium bg-[#068ef1] text-white w-24 p-1 rounded-full text-center">
                            {lot.is_multi_level ? `${lot.num_levels} Levels` : 'Single Level'}
                        </p>
                    </a>
                </div>
            ))}
        </div>
    );
}

export default ParkingLots;
