import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Proxy API requests to the FastAPI backend when running locally
      '/services': 'http://localhost:8000',
      '/health': 'http://localhost:8000'
    }
  }
});