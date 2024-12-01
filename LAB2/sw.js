const CACHE_NAME = `password-manager-v1`;

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    cache.addAll([
      '/',
      '/index.html',
      '/style.css',
      '/app.js',
      '/icon.png',
      '/icon.ico',
      '/manifest.json',
      'https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css',
      'https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css',
      'https://code.jquery.com/jquery-3.5.1.slim.min.js',
      'https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js',
      'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js'
    ]);
  })());
});

self.addEventListener('install', (event) => {
    console.log('Service Worker is installing...', event);
});

self.addEventListener('fetch', event => {
    console.log('[Service Worker] fetching:', event.request.url);

  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);

    const cachedResponse = await cache.match(event.request);
    if (cachedResponse) {
      return cachedResponse;
    } else {
        try {
          const fetchResponse = await fetch(event.request);

          cache.put(event.request, fetchResponse.clone());
          return fetchResponse;
        } catch (e) {
          console.log(e);
        }
    }
  })());
});