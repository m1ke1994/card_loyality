import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: "autoUpdate",
      manifest: {
        name: "Loyalty Client",
        short_name: "Loyalty",
        start_url: "/",
        display: "standalone",
        background_color: "#0f172a",
        theme_color: "#0ea5e9",
        icons: []
      }
    })
  ],
  server: {
    port: 5173
  }
});
