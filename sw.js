// نسخه را با هر انتشار عوض کنید تا فایل‌های تازه گرفته شوند
const V='v-20261001070458';
const FILES=['./','./index.html','./manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png','./assets/fonts/Vazirmatn-Regular.woff2','./assets/fonts/Vazirmatn-Bold.woff2','./assets/fonts/Lalezar-Regular.woff2','./assets/img/contact-cat.webp','./physics/simple-machines/'];
self.addEventListener('install',e=>{self.skipWaiting();e.waitUntil(caches.open(V).then(c=>c.addAll(FILES)));});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));});
// اول از شبکه، اگر نبود از حافظه؛ پس بی‌اینترنت هم باز می‌شود
self.addEventListener('fetch',e=>{if(e.request.method!=='GET')return;e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();caches.open(V).then(c=>c.put(e.request,cp));return r;}).catch(()=>caches.match(e.request,{ignoreSearch:true})));});
