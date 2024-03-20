/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./FSApp/templates/**/*.html",
      "./FSApp/static/js/**/*.js",
      "./node_modules/flowbite/**/*.js",
  ],
    theme: {
      extend: {},

  },
    plugins: [
        require('@tailwindcss/forms'),
        require('flowbite/plugin'),
    ],
}

