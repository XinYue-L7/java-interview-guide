// Service Worker - Java面试宝典 PWA离线缓存
var CACHE_NAME = 'interview-baodian-v3';
var ASSETS = [
  '/Java%E9%9D%A2%E8%AF%95%E5%AE%9D%E5%85%B8_%E6%80%BB%E7%9B%AE%E5%BD%95.html',
  '/Java%E9%9D%A2%E8%AF%95%E5%AE%9D%E5%85%B8_01_Java%E5%9F%BA%E7%A1%80.html',
  '/Java%E9%9D%A2%E8%AF%95%E5%AE%9D%E5%85%B8_02_%E9%9B%86%E5%90%88%E5%AE%B9%E5%99%A8.html',
  '/Java%E9%9D%A2%E8%AF%95%E5%AE%9D%E5%85%B8_03_JVM.html',
  '/Java%E9%9D%A2%E8%AF%95%E5%AE%9D%E5%85%B8_04_%E5%B9%B6%E5%8F%91%E7%BC%96%E7%A8%8B.html',
  '/Java%E9%9D%A2%E8%AF%95%E5%AE%9D%E5%85%B8_05_MySQL.html',
  '/Java%E9%9D%A2%E8%AF%95%E5%AE%9D%E5%85%B8_06_Redis.html',
  '/Java%E9%9D%A2%E8%AF%95%E5%AE%9D%E5%85%B8_07_%E6%A1%86%E6%9E%B6.html',
  '/Java%E9%9D%A2%E8%AF%95%E5%AE%9D%E5%85%B8_08_%E5%88%86%E5%B8%83%E5%BC%8F%26%E5%85%B6%E4%BB%96.html',
  '/%E6%89%AB%E7%A0%81%E8%AE%BF%E9%97%AE.html',
  '/search_index.json',
  '/qrcode_lan.png',
  '/manifest.json',
  '/icon.svg'
];

// 安装：预缓存所有资源
self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return Promise.all(
        ASSETS.map(function(url) {
          return cache.add(url).catch(function() {
            // 单个文件失败不影响其他缓存
          });
        })
      );
    })
  );
  // 立即激活，不等待旧SW
  self.skipWaiting();
});

// 请求拦截：缓存优先，缓存未命中才走网络
self.addEventListener('fetch', function(e) {
  // 只拦截同源请求
  if (!e.request.url.startsWith(self.location.origin)) return;

  e.respondWith(
    caches.match(e.request).then(function(cached) {
      if (cached) return cached;

      return fetch(e.request).then(function(resp) {
        // 只缓存成功的GET请求
        if (resp.status === 200) {
          var clone = resp.clone();
          caches.open(CACHE_NAME).then(function(cache) {
            cache.put(e.request, clone);
          });
        }
        return resp;
      }).catch(function() {
        // 网络失败且无缓存时，HTML请求返回离线提示
        if (e.request.headers.get('accept') && e.request.headers.get('accept').indexOf('text/html') !== -1) {
          return new Response(
            '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>离线</title><style>body{font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;background:#0d0d1a;color:#c9a96e;flex-direction:column;gap:12px}h1{font-size:24px}p{color:#888;font-size:14px}</style></head><body><h1>📴 当前离线</h1><p>请联网访问一次后即可离线使用</p></body></html>',
            {headers:{'Content-Type':'text/html;charset=UTF-8'}}
          );
        }
      });
    })
  );
});

// 激活：清理旧缓存
self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(function(k) { return k !== CACHE_NAME; }).map(function(k) {
          return caches.delete(k);
        })
      );
    })
  );
  self.clients.claim();
});
