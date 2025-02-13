/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        geist: ["Geist", "sans-serif"],
        lexend: ["Lexend", "sans-serif"],
      },
    },
  },
  plugins: [],
}

