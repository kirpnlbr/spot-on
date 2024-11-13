import { MapPin } from 'lucide-react';

function LocationPage({ onEnableLocation, onSkip }) {
    return (
        <div class="min-h-screen px-4 justify-center items-center flex">
            <div class="flex flex-col space-y-5 rounded-xl border p-10 bg-white shadow border-gray-200">
                <div class="flex flex-col space-y-2 items-center">
                    <MapPin class="text-blue-600 w-10 h-10" />
                    <h1 class="text-2xl font-bold text-gray-800">Enable Location</h1>
                    <p class="text-gray-600 text-center">We need your location to find the nearest available parking spot!</p>
                </div>
                <div class="flex flex-col space-y-3 items-center">
                    <button onClick={onEnableLocation} class="rounded-xl p-3 bg-blue-700 border-[1.5px] border-blue-500 text-white font-medium w-full hover:bg-blue-600">Allow Location Access</button>
                    <button onClick={onSkip} class="text-blue-600 underline text-sm font-medium w-full ">Maybe Later</button>
                </div>
            </div>
        </div>
    )
}

export default LocationPage;