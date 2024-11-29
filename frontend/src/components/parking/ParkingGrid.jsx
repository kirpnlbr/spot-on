function ParkingGrid({ parkingGrid }) {
    console.log('Received parkingGrid in ParkingGrid Component:', parkingGrid);

    // Group spots by rows (assuming spot IDs contain row labels like 'A1', 'B2', etc.)
    const rows = {};
    parkingGrid.forEach(spot => {
        const rowLabel = spot.id.split('-')[1][0]; // Extract the row label (e.g., 'A')
        if (!rows[rowLabel]) {
            rows[rowLabel] = [];
        }
        rows[rowLabel].push(spot);
    });

    // Sort the rows and spots within each row
    const sortedRowLabels = Object.keys(rows).sort();
    sortedRowLabels.forEach(rowLabel => {
        rows[rowLabel].sort((a, b) => {
            const aNumber = parseInt(a.id.match(/\d+/)[0], 10);
            const bNumber = parseInt(b.id.match(/\d+/)[0], 10);
            return aNumber - bNumber;
        });
    });

    return (
        <div class="flex flex-col space-y-2">
            {sortedRowLabels.map(rowLabel => (
                <div key={rowLabel} class="flex space-x-2">
                    {rows[rowLabel].map(spot => (
                        <div
                            key={spot.id}
                            class={`
                                aspect-square w-full rounded-lg flex items-center justify-center
                                ${spot.isOccupied
                                    ? 'bg-[#e3e2e2] text-gray-500' // Style for occupied spots
                                    : 'border-2 border-[#068ef1] text-[#068ef1]' // Style for available spots
                                }
                            `}
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
