function ParkingGrid({ parkingGrid }) {
    console.log('Received parkingGrid in ParkingGrid Component:', parkingGrid);
  
    return (
      <div class="grid grid-cols-5 gap-3">
        {parkingGrid.map(spot => (
          <div
            key={spot.id}
            class={`
              aspect-square rounded-lg flex items-center justify-center
              ${
                spot.isOccupied
                  ? 'bg-gray-300 text-gray-500' // Style for occupied spots
                  : 'border-2 border-blue-600 text-blue-600' // Style for available spots
              }
            `}
          >
            {spot.id}
          </div>
        ))}
      </div>
    );
  }
  
  export default ParkingGrid;
  