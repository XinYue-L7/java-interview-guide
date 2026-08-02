// Service Worker - Java面试宝典 PWA离线缓存
const CACHE_NAME = 'interview-baodian-v1';
const ASSETS = [
  '/Java面试宝典_总目录.html',
  '/Java面试宝典_01_Java基础.html',
  '/Java面试宝典_02_集合容器.html',
  '/Java面试宝典_03_JVM.html',
  '/Java面试宝典_04_并发编程.html',
  '/Java面试宝典_05_MySQL.html',
  '/Java面试宝典_06_Redis.html',
  '/Java面试宝典_07_框架.html',
  '/Java面试宝典_08_分布式&其他.html',
  '/扫码访问.html',
  '/search_index.json',
  '/qrcode_lan.png',
  '/manifest.json',
  '/icon.svg'
];

// 安装：预缓存所有资源
self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return Promise.allSettled(
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
