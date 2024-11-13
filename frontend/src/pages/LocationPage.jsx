import { MapPin } from 'lucide-react';

function LocationPage() {
    return (
        <div class="min-h-screen flex flex-col space-y-8 justify-center items-center px-4">
            <div class="flex flex-col space-y-2 items-center">
                <MapPin class="text-blue-500 w-10 h-10" />
                <h1 class="text-2xl font-bold text-gray-900">Enable Location</h1>
                <p class="text-gray-600 text-center">SpotOn needs your location to find the nearest available parking spot.</p>
            </div>
            <div class="flex flex-col space-y-3 items-center">
                <button class="rounded-xl p-3 bg-blue-700 border-[1.5px] border-blue-500 text-white font-medium w-full hover:bg-blue-600">Allow Location Access</button>
                <button class="text-blue-700 underline text-sm font-medium w-full ">Maybe Later</button>
            </div>
        </div>
    )
}

export default LocationPage;