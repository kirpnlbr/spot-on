import { CircleParking } from 'lucide-react';

function ParkingLots({ onSelectLot, parkingLots }) {
    return (
        <div class="flex-1">

            {parkingLots.map((lot) => (
                <div
                    key={lot.id}
                    class="px-4 pt-4"
                    onClick={() => onSelectLot(lot)}
                >
                    <a class="flex flex-col gap-1 p-4 rounded-lg border-[1px] border-gray-200 hover:bg-gray-50 shadow-sm active:scale-95 transition">
                        <h2 class="font-medium text-gray-800 flex items-center">
                            <span class="bg-[#E5E3DD] bg-opacity-25 rounded-full p-1 mr-1.5"><CircleParking class="text-[#B4B3AF] h-4 w-4" /></span>
                            {lot.name}
                        </h2>
                        <p class="text-sm text-[#068ef1]">
                            {lot.distance} <span class="text-gray-600">• {lot.spots}</span>
                        </p>
                        <p class="text-xs mt-1 text-gray-500">
                            {lot.address}
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
