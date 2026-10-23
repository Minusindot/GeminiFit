// Gemini Fit Progressive Web App (PWA) Service Worker
const CACHE_NAME = 'geminifit-pwa-v1';

self.addEventListener('install', (e) => {
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
      );
    })
  );
  self.clients.claim();
});

// Network-first strategy with cache fallback
self.addEventListener('fetch', (e) => {
  // Only handle http/https requests
  if (!e.request.url.startsWith('http')) return;
  
  e.respondWith(
    fetch(e.request)
      .then((response) => {
        // Cache successful responses for offline / speed
        if (response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(e.request, clone);
          });
        }
        return response;
      })
      .catch(() => caches.match(e.request))
  );
});
