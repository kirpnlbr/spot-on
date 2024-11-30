import { House, FileClock, CircleUser } from 'lucide-react';

const BottomNav = () => {
    return (
        <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 pb-safe">
            <div class="max-w-sm mx-auto flex items-center justify-around h-16">
                {/* Home */}
                <div class="flex flex-col items-center active:scale-90 transition">
                    <House class="h-6 w-6 text-[#068ef1]" />
                    <span class="text-xs text-[#068ef1] font-medium mt-1">Home</span>
                </div>

                {/* Bookings */}
                <div class="flex flex-col items-center active:scale-90 transition">
                    <FileClock class="h-6 w-6 text-gray-400" />
                    <span class="text-xs text-gray-400 mt-1">Bookings</span>
                </div>

                {/* Profile */}
                <div class="flex flex-col items-center active:scale-90 transition">
                    <CircleUser class="h-6 w-6 text-gray-400" />
                    <span class="text-xs text-gray-400 mt-1">Profile</span>
                </div>
            </div>
        </div>
    );
};

export default BottomNav;