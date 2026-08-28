// Service Worker v22 - Java面试宝典 PWA 离线缓存
// 策略：安装时预缓存全部页面（首访后完全离线可用），网络优先 + 缓存兜底
var CACHE_NAME = 'interview-baodian-v22';
var RUNTIME_CACHE = 'interview-baodian-runtime-v22';

// 预缓存清单（安装时下载）
var PAGES = ["Java面试宝典_01_Java基础.html", "Java面试宝典_02_集合容器.html", "Java面试宝典_03_JVM.html", "Java面试宝典_04_并发编程.html", "Java面试宝典_05_MySQL.html", "Java面试宝典_06_Redis.html", "Java面试宝典_07_MongoDB.html", "Java面试宝典_08_Elasticsearch.html", "Java面试宝典_Dubbo.html", "Java面试宝典_MyBatis.html", "Java面试宝典_Netty.html", "Java面试宝典_Spring.html", "Java面试宝典_SpringBoot.html", "Java面试宝典_SpringMVC.html", "Java面试宝典_Zookeeper.html", "Java面试宝典_分布式理论.html", "Java面试宝典_总目录.html", "Java面试宝典_汇丰银行面试题2026年8月.html", "Java面试宝典_消息队列.html", "Java面试宝典_系统设计.html", "Java面试宝典_网络协议.html", "Java面试宝典_设计模式.html"];

var EXTRA_FILES = ['manifest.json', 'search_index.json', 'icon.svg', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png', 'qrcode.min.js'];

// 生成绝对 URL 列表（相对 sw.js 所在目录）
var baseUrl = new URL('./', self.location.href);
function abs(f) { return new URL(f, baseUrl).href; }

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return Promise.all(
        PAGES.map(function(p) { return cache.add(abs(p)); })
          .concat(EXTRA_FILES.map(function(f) { return cache.add(abs(f)); }))
      );
    }).then(function() { self.skipWaiting(); })
  );
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(function(k) {
          return k !== CACHE_NAME && k !== RUNTIME_CACHE;
        }).map(function(k) { return caches.delete(k); })
      );
    }).then(function() { self.clients.claim(); })
  );
});

// 请求拦截：网络优先，失败用缓存兜底（离线场景）
self.addEventListener('fetch', function(e) {
  if (e.request.method !== 'GET') return;
  if (!e.request.url.startsWith(self.location.origin)) return;

  e.respondWith(
    fetch(e.request).then(function(resp) {
      if (resp && resp.status === 200) {
        var clone = resp.clone();
        var url = new URL(e.request.url);
        if (url.pathname.endsWith('.html') || url.pathname.endsWith('.json')) {
          caches.open(RUNTIME_CACHE).then(function(cache) { cache.put(e.request, clone); });
        }
      }
      return resp;
    }).catch(function() {
      return caches.match(e.request).then(function(cached) {
        if (cached) return cached;
        var accept = e.request.headers.get('accept') || '';
        if (accept.indexOf('text/html') !== -1 || e.request.mode === 'navigate') {
          return offlinePage();
        }
        return new Response('', { status: 504, statusText: 'Offline' });
      });
    })
  );
});

// 离线提示页面（仅在缓存为空时出现）
function offlinePage() {
  var html = '<!DOCTYPE html>' +
    '<html lang="zh-CN"><head><meta charset="UTF-8">' +
    '<meta name="viewport" content="width=device-width,initial-scale=1">' +
    '<title>离线</title>' +
    '<style>' +
    'body{font-family:sans-serif;display:flex;align-items:center;justify-content:center;' +
    'height:100vh;margin:0;background:#0d0d1a;color:#c9a96e;flex-direction:column;gap:12px}' +
    'h1{font-size:24px}' +
    'p{color:#888;font-size:14px;text-align:center;max-width:280px;line-height:1.6}' +
    '</style></head><body>' +
    '<h1>已离线</h1>' +
    '<p>请先联网访问一次面试宝典页面，之后即可离线使用。</p>' +
    '<p style="font-size:12px">当前缓存为空，需要首次联网加载。</p>' +
    '</body></html>';
  return new Response(html, { headers: { 'Content-Type': 'text/html;charset=UTF-8' } });
}
