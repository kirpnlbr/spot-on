import { MapPin } from 'lucide-react';

function LocationPage({ onEnableLocation, onSkip }) {
    return (
        <div class="min-h-screen px-4 justify-center items-center flex bg-white">
            <div class="flex flex-col space-y-5">
                <div class="flex flex-col space-y-2 items-center">
                    <MapPin class="text-[#068ef1] w-10 h-10 animate-bounce" />
                    <h1 class="text-2xl font-bold text-gray-800">Enable Location</h1>
                    <p class="text-gray-600 text-center">We need your location to find the nearest available parking spot!</p>
                </div>
                <div class="flex flex-col space-y-3 items-center">
                    <button onClick={onEnableLocation} class="rounded-xl p-3 bg-[#068ef1] hover:bg-[#1F9FFC] text-white font-medium w-3/4 active:scale-95 transition ease-out">Allow Location Access</button>
                    <button onClick={onSkip} class="text-[#068ef1] underline text-sm font-medium w-full ">Maybe Later</button>
                </div>
            </div>
        </div>
    )
}

export default LocationPage;