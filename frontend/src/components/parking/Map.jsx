export function NavigationMap() {
    return (
        <div class="relative w-full h-full overflow-hidden rounded-xl bg-[#f8f9fa]">
            {/* Background */}
            <div
                class="absolute inset-0"
                style={{
                    backgroundImage: `url("data:image/svg+xml,%3Csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3Cpattern id='cityGrid' x='0' y='0' width='50' height='50' patternUnits='userSpaceOnUse'%3E%3Crect width='50' height='50' fill='%23f8f9fa'/%3E%3Cpath d='M0 0 L50 0 M0 10 L50 10 M0 20 L50 20 M0 30 L50 30 M0 40 L50 40 M0 50 L50 50' stroke='%23e9ecef' stroke-width='0.5'/%3E%3Cpath d='M0 0 L0 50 M10 0 L10 50 M20 0 L20 50 M30 0 L30 50 M40 0 L40 50 M50 0 L50 50' stroke='%23e9ecef' stroke-width='0.5'/%3E%3C/pattern%3E%3C/defs%3E%3Crect width='100%25' height='100%25' fill='url(%23cityGrid)'/%3E%3C/svg%3E")`,
                    backgroundSize: '50px 50px',
                }}
            />

            {/* Navigation Line */}
            <div class="absolute inset-0 flex items-center justify-center">
                <div class="w-0.5 h-32 bg-[#068ef1]/30 animate-pulse" />
            </div>

            {/* Current Location Indicator */}
            <div class="absolute bottom-10 left-1/2 -translate-x-1/2">
                <div class="w-4 h-4 bg-[#068ef1] rounded-full animate-ping opacity-50" />
                <div class="w-4 h-4 bg-[#068ef1] rounded-full absolute inset-0" />
            </div>

            {/* Destination Indicator */}
            <div class="absolute top-10 left-1/2 -translate-x-1/2">
                <div class="w-6 h-6 border-2 border-[#068ef1] rounded-full">
                    <div class="w-2 h-2 bg-[#068ef1] rounded-full absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
                </div>
            </div>
        </div>
    );
}

export default NavigationMap;