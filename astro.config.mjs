import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.celebiyonetim.com.tr',
  vite: {
    plugins: [tailwindcss()],
  },
  compressHTML: true,
  build: {
    inlineStylesheets: 'always',
  },
});
