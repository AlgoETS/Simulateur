/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#EC4149',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

