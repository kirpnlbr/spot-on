import React from 'react';

function ParkingLots({ onSelectLot, parkingLots }) {
    return (
        <div className="flex-1">
            {parkingLots.map((lot) => (
                <div
                    key={lot.id}
                    className="p-4 border-b last:border-b-0 hover:bg-gray-50"
                    onClick={() => onSelectLot(lot)}
                >
                    <a className="flex flex-col gap-1">
                        <h2 className="font-medium text-gray-900">
                            {lot.name}
                        </h2>
                        <p className="text-sm text-blue-500">
                            {lot.distance} <span className="text-gray-500">• {lot.spots}</span>
                        </p>
                        <p className="text-sm text-gray-500">
                            {lot.is_multi_level
                                ? `${lot.num_levels} Level${lot.num_levels > 1 ? 's' : ''}`
                                : 'Single Level'}
                        </p>
                    </a>
                </div>
            ))}
        </div>
    );
}

export default ParkingLots;
