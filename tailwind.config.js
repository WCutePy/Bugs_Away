/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./FSApp/templates/**/*.html",
      "./FSApp/static/js/**/*.js",
  ],
    theme: {
      extend: {},

  },
    plugins: [
      require('@tailwindcss/forms'),
    ],
}

