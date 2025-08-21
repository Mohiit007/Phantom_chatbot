/**** Tailwind CSS Config ****/
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{js,jsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1d4ed8',
        accent: '#0ea5e9'
      }
    },
  },
  plugins: [],
}
