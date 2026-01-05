/** @type {import('tailwindcss').Config} */
module.exports = {
 content: [
  "./index.html",
  "./apps/**/index.html",
  "./apps/**/src/**/*.{js,ts,jsx,tsx,vue}",
  "./packages/**/src/**/*.{js,ts,jsx,tsx,vue}",
],

  theme: {
    extend: {
      colors: {
        primary: "#3b82f6",
        accent: "#8b5cf6",
        glass: "rgba(255,255,255,0.08)"
      },
      boxShadow: {
        soft: "0 10px 30px rgba(0,0,0,0.12)"
      },
      backgroundImage: {
        gradient: "linear-gradient(135deg, #1e3a8a 0%, #0ea5e9 50%, #14b8a6 100%)"
      }
    }
  },
  plugins: []
};
