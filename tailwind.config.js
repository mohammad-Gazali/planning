/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/**/*.html",
        "node_modules/preline/dist/*.js"
    ],
    darkMode: "class",
    theme: {
      extend: {
        fontFamily: {
            "cairo": ["Cairo", "sans-serif"],
        }
      },
    },
    plugins: [
        require('preline/plugin'),
        require('@tailwindcss/forms'),
    ],
}