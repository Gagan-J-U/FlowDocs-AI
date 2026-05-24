import typography from "@tailwindcss/typography";

/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      colors: {
        ink: "#070A12",
        panel: "#0D111C",
        line: "rgba(255,255,255,0.1)",
        brand: "#8FD3FF",
        mint: "#9BE7C7",
      },
      boxShadow: {
        glow: "0 22px 80px rgba(38, 132, 255, 0.18)",
        panel: "0 18px 70px rgba(0, 0, 0, 0.35)",
      },
    },
  },
  plugins: [typography],
};
