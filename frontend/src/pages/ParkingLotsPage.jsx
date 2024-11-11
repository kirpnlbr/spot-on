function ParkingLotsPage() {
    const parkingLots = [
        {
            id: 1,
            name: "Central Mall Parking",
            distance: "2 mins away",
            spots: "12 spots"
        },
        {
            id: 2,
            name: "SM Southmall Parking",
            distance: "5 mins away",
            spots: "8 spots"
        },
        {
            id: 3,
            name: "Uptown Parking",
            distance: "8 mins away",
            spots: "34 spots"
        }
    ];

    return (
        <div class="flex flex-col bg-white">
            {/* Search */}
            <div class="p-4 shadow-sm border-b">
                <input
                    type="text"
                    placeholder="Search parking lot..."
                    class="border border-gray-200 bg-gray-50 w-full p-3 rounded-lg"
                />
            </div>

            {/* Parking Lots List */}
            <div class="flex-1">
                {parkingLots.map((lot) => (
                    <div
                        key={lot.id}
                        class="p-4 border-b last:border-b-0 hover:bg-gray-50"
                    >
                        <a href="/" class="flex flex-col gap-1">
                            <h2 class="font-medium text-gray-900">
                                {lot.name}
                            </h2>
                            <p class="text-sm text-gray-500">
                                {lot.distance} • {lot.spots}
                            </p>
                        </a>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ParkingLotsPage;