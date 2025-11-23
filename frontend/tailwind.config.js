module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  theme: {
    extend: {
      colors: {
        luxePurple: "#3b0b6f",
        luxeGradientStart: "#4b0fb0",
        luxeGradientEnd: "#7a2be6",
        gold: "#D6A24B"
      },
      boxShadow: {
        'soft-glass': '0 8px 30px rgba(31, 41, 55, 0.12), inset 0 1px 0 rgba(255,255,255,0.02)'
      },
      borderRadius: {
        'xl-2': '18px'
      }
    }
  },
  plugins: []
};
