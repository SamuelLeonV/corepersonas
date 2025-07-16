/// <reference types="vitest" />
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: '0.0.0.0',
    open: false,
  },
  build: {
    outDir: 'build',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          // Separar Material UI en su propio chunk
          'mui': ['@mui/material', '@mui/icons-material', '@mui/lab'],
          // Separar React en su propio chunk
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          // Separar otras librerías
          'chart-vendor': ['chart.js', 'react-chartjs-2'],
          'form-vendor': ['react-hook-form', '@hookform/resolvers', 'yup'],
        },
      },
    },
  },
  define: {
    // Solo variables específicas de entorno para seguridad
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV),
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  // Variables de entorno con prefijo VITE_
  envPrefix: 'REACT_APP_',
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/setupTests.ts'],
  },
})
