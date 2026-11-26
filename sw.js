// Gemini Fit Progressive Web App (PWA) Service Worker v4.7.12
const CACHE_NAME = 'geminifit-pwa-v4.7.12';

self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((k) => caches.delete(k)) // Purge all old caches on version bump
      );
    }).then(() => self.clients.claim())
  );
});

// Network-first strategy with cache fallback
self.addEventListener('fetch', (e) => {
  if (!e.request.url.startsWith('http')) return;

  // HTML and dynamic scripts: Always fetch fresh from network
  const url = new URL(e.request.url);
  const isHtmlOrScript = url.pathname.endsWith('.html') || url.pathname === '/' || url.pathname.endsWith('.js');

  if (isHtmlOrScript) {
    e.respondWith(
      fetch(e.request, { cache: 'no-cache' })
        .then((response) => {
          if (response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(e.request, clone));
          }
          return response;
        })
        .catch(() => caches.match(e.request))
    );
    return;
  }

  // Static media (images, audio, fonts): Cache-first for 0ms BG/CG/SCG playback
  const isStaticMedia = /\.(png|jpg|jpeg|webp|gif|svg|mp3|wav|ogg|woff2?)$/i.test(url.pathname);
  if (isStaticMedia) {
    e.respondWith(
      caches.match(e.request).then((cached) => {
        if (cached) return cached;
        return fetch(e.request).then((response) => {
          if (response && response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(e.request, clone));
          }
          return response;
        });
      })
    );
    return;
  }

  // Other assets: Network-first with cache fallback
  e.respondWith(
    fetch(e.request)
      .then((response) => {
        if (response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, clone));
        }
        return response;
      })
      .catch(() => caches.match(e.request))
  );
});
