/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: false,
  content: [],
  theme: {
    extend: {
      colors: {
        'text': '#f2ecac',
        'background': '#143302',
        'primary': '#637462',
        'secondary': '#6d835c',
        'accent': '#00c203',
       },
    },
  },
  plugins: [],
}

