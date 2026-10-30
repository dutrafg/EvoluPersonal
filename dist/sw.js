'use strict';

const CACHE_NAME = 'evolupersonal-md500-offline-v1';
const SCOPE_URL = self.registration.scope;
const SHELL = ['./index.html', './training-methods.js', './insights.js', './offline-assets.json', './OFFLINE_CREDITS.md'];

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    await cache.addAll(SHELL.map(path => new Request(new URL(path, SCOPE_URL))));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(key => key.startsWith('evolupersonal-md500-offline-') && key !== CACHE_NAME).map(key => caches.delete(key)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET' || new URL(request.url).origin !== self.location.origin) return;

  event.respondWith((async () => {
    const cache = await caches.open(CACHE_NAME);
    const isNavigation = request.mode === 'navigate';
    if (!isNavigation) {
      const cached = await cache.match(request, { ignoreSearch: true });
      if (cached) return cached;
    }
    try {
      const response = await fetch(request);
      if (response.ok && (isNavigation || request.destination === 'script' || request.destination === 'style' || request.destination === 'image' || request.url.includes('offline-assets.json'))) {
        cache.put(request, response.clone()).catch(() => {});
      }
      return response;
    } catch (error) {
      const fallback = await cache.match(request, { ignoreSearch: true })
        || (isNavigation ? await cache.match(new URL('./index.html', SCOPE_URL).href) : null);
      if (fallback) return fallback;
      return new Response('Este arquivo ainda não foi baixado para uso offline.', {
        status: 503,
        headers: { 'Content-Type': 'text/plain; charset=utf-8' }
      });
    }
  })());
});

self.addEventListener('message', event => {
  if (event.data?.type !== 'CACHE_LIBRARY' || !event.ports?.[0]) return;
  const port = event.ports[0];
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    let manifest;
    try {
      const response = await fetch(new URL('./offline-assets.json', SCOPE_URL));
      if (!response.ok) throw new Error('Não foi possível obter a lista de mídias.');
      manifest = await response.json();
    } catch (error) {
      port.postMessage({ type: 'ERROR', message: error.message || 'Falha ao ler a lista de mídias.' });
      return;
    }

    const assets = manifest.assets || [];
    const total = assets.length;
    let complete = 0;
    const failed = [];
    port.postMessage({ type: 'PROGRESS', total, complete, failed: 0, bytes: manifest.bytes || 0 });

    for (let offset = 0; offset < total; offset += 3) {
      const batch = assets.slice(offset, offset + 3);
      await Promise.all(batch.map(async path => {
        const url = new URL(path, SCOPE_URL).href;
        try {
          const existing = await cache.match(url);
          if (!existing) {
            const response = await fetch(url, { cache: 'reload' });
            if (!response.ok) throw new Error('HTTP ' + response.status);
            await cache.put(url, response);
          }
        } catch (error) {
          failed.push({ path, reason: error.message || 'falha de rede' });
        } finally {
          complete++;
          port.postMessage({ type: 'PROGRESS', total, complete, failed: failed.length, bytes: manifest.bytes || 0 });
        }
      }));
    }

    port.postMessage({
      type: 'DONE',
      total,
      complete,
      failedCount: failed.length,
      failed: failed.slice(0, 30),
      bytes: manifest.bytes || 0
    });
  })());
});
