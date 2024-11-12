import ParkingLots from "../components/parking/ParkingLots";

function ParkingLotsPage() {

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
            <ParkingLots />
        </div>
    );
}

export default ParkingLotsPage;