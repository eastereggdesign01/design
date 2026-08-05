import { defineConfig } from 'vite';
import { fileURLToPath } from 'node:url';

// 멀티 페이지 빌드: / = 포트폴리오 랜딩, /hub/ = 브랜드 키트 허브
export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: fileURLToPath(new URL('./index.html', import.meta.url)),
        hub: fileURLToPath(new URL('./hub/index.html', import.meta.url)),
      },
    },
  },
});
