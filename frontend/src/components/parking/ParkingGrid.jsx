import React from 'react';

function ParkingGrid({ parkingGrid, nearestSpotId }) {
    console.log('Received parkingGrid in ParkingGrid Component:', parkingGrid);

    if (!parkingGrid || parkingGrid.length === 0) {
        return <div class="text-center text-gray-500">No parking spots available.</div>;
    }

    // Group spots by rows (assuming spot IDs contain row labels like 'A1', 'B2', etc.)
    const rows = {};
    parkingGrid.forEach(spot => {
        // Extract the row label (e.g., 'A' from 'L1-A1')
        const spotIdParts = spot.id.split('-'); // ['L1', 'A1']
        if (spotIdParts.length < 2) return; // Invalid ID format

        const rowLabel = spotIdParts[1][0]; // 'A' from 'A1'
        if (!rows[rowLabel]) {
            rows[rowLabel] = [];
        }
        rows[rowLabel].push(spot);
    });

    // Sort the rows alphabetically
    const sortedRowLabels = Object.keys(rows).sort();

    // Sort the spots within each row numerically
    sortedRowLabels.forEach(rowLabel => {
        rows[rowLabel].sort((a, b) => {
            const aNumberMatch = a.id.match(/\d+/);
            const bNumberMatch = b.id.match(/\d+/);
            const aNumber = aNumberMatch ? parseInt(aNumberMatch[0], 10) : 0;
            const bNumber = bNumberMatch ? parseInt(bNumberMatch[0], 10) : 0;
            return aNumber - bNumber;
        });
    });

    return (
        <div class="space-y-4">
            {/* Legend */}
            <div class="flex gap-4 text-sm text-gray-600">
                <span class="flex items-center gap-1">
                    <div class="w-3 h-3 rounded-full bg-[#068ef1] text-white"></div>
                    Nearest
                </span>
                <span class="flex items-center gap-1">
                    <div class="w-3 h-3 border-2 rounded-full text-gray-500 bg-white"></div>
                    Available
                </span>
                <span class="flex items-center gap-1">
                    <div class="w-3 h-3 rounded-full bg-[#e3e2e2]"></div>
                    Occupied
                </span>
            </div>

            {/* Grid */}
            <div class="flex flex-col space-y-2">
                {sortedRowLabels.map(rowLabel => (
                    <div key={rowLabel} class="flex space-x-2">
                        {rows[rowLabel].map(spot => {
                            const isNearest = nearestSpotId === spot.id;
                            return (
                                <div
                                    key={spot.id}
                                    class={`
                                        aspect-square w-full rounded-lg flex items-center justify-center
                                        ${spot.isOccupied
                                            ? 'bg-[#e3e2e2] text-gray-500'
                                            : isNearest
                                                ? 'bg-[#068ef1] text-white'
                                                : 'border-2 text-gray-500 bg-white'
                                        }
                                        transition-colors duration-200
                                    `}
                                    title={`Spot ID: ${spot.id} | ${spot.isOccupied ? 'Occupied' : 'Available'}`}
                                >
                                    {spot.id.split('-')[1]}
                                </div>
                            );
                        })}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ParkingGrid;