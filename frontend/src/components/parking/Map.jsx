export const Map = () => {
    return (
        <div className="w-full aspect-square bg-gray-50 rounded-lg overflow-hidden">
            <svg
                viewBox="0 0 100 100"
                className="w-full h-full opacity-30"
                preserveAspectRatio="none"
            >
                <pattern
                    id="grid"
                    width="20"
                    height="20"
                    patternUnits="userSpaceOnUse"
                    patternTransform="rotate(45)"
                >
                    <path
                        d="M 20 0 L 0 0 0 20"
                        fill="none"
                        stroke="white"
                        strokeWidth="2"
                    />
                </pattern>

                <rect
                    width="100"
                    height="100"
                    fill="#E5E7EB"
                />
                <rect
                    width="100"
                    height="100"
                    fill="url(#grid)"
                />
            </svg>
        </div>
    );
};
