import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      'vue-i18n': 'vue-i18n/dist/vue-i18n.esm-bundler.js',
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    headers: {
      'Content-Security-Policy': "script-src 'self' 'unsafe-eval'; object-src 'self'"
    }
  }
})

