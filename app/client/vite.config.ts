import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { tanstackRouter } from '@tanstack/router-plugin/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    tanstackRouter({
      target: 'react',
      autoCodeSplitting: true,
    }),
    react(),
  ],
  build: {
    assetsDir: 'static/fe/assets'
  },
  server: {
    host: '0.0.0.0',  // Listen on all interfaces
    allowedHosts: ['host.docker.internal', 'localhost'],  // Allow Docker proxy
    watch: {
      usePolling: true,
    },
    port: 5173,  // Default Vite port
    strictPort: true,  // Fail if port is already in use
    hmr: {
      clientPort: 5173,  // Ensure HMR works correctly in Docker
    },
  },
})
