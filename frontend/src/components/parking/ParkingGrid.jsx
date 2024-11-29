import React from 'react';

function ParkingGrid({ parkingGrid }) {
    console.log('Received parkingGrid in ParkingGrid Component:', parkingGrid);

    if (!parkingGrid || parkingGrid.length === 0) {
        return <div className="text-center text-gray-500">No parking spots available.</div>;
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
        <div className="flex flex-col space-y-2">
            {sortedRowLabels.map(rowLabel => (
                <div key={rowLabel} className="flex space-x-2">
                    {rows[rowLabel].map(spot => (
                        <div
                            key={spot.id}
                            className={`
                                aspect-square w-full rounded-lg flex items-center justify-center
                                ${spot.isOccupied
                                    ? 'bg-[#e3e2e2] text-gray-500' // Style for occupied spots
                                    : 'border-2 border-[#068ef1] text-[#068ef1]' // Style for available spots
                                }
                                transition-colors duration-200
                            `}
                            title={`Spot ID: ${spot.id} | ${spot.isOccupied ? 'Occupied' : 'Available'}`}
                        >
                            {spot.id.split('-')[1]}
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
}

export default ParkingGrid;
