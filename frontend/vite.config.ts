import basicSsl from "@vitejs/plugin-basic-ssl";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import path from "path"


export default defineConfig({
  plugins: [react(), basicSsl()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },

  base: '/WinterHackathon/',
  server: {
    https: {},
    proxy: {
      "/api/v1": {
        target: "https://winter-hack.fly.dev",
        changeOrigin: true,
        secure: true,
        followRedirects: true
      }
    }
  }
});
