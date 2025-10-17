import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': '/src',
      '@routes': '/src/routes',
      '@pages': '/src/pages',
      '@lib': '/src/lib',
      '@assets': '/src/assets',
      '@components': '/src/components',
    },
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
  },
})
