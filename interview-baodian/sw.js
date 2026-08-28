// Service Worker v7 - Java面试宝典 PWA 离线缓存
// 策略：网络优先（避免缓存旧版本JS/JSON导致搜索不匹配），失败时用缓存兜底
// 这样保证用户总能拿到最新的搜索索引和代码

var CACHE_NAME = 'interview-baodian-v7';
var RUNTIME_CACHE = 'interview-baodian-runtime-v7';

// 需要缓存的关键静态资源（运行时按需缓存）
var ESSENTIAL_FILES = [];

// 安装：跳过等待，立即接管
self.addEventListener('install', function(e) {
  self.skipWaiting();
});

// 激活：清理所有旧版本缓存
self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(function(k) {
          return k !== CACHE_NAME && k !== RUNTIME_CACHE;
        }).map(function(k) {
          return caches.delete(k);
        })
      );
    })
  );
  self.clients.claim();
});

// 请求拦截：网络优先策略
self.addEventListener('fetch', function(e) {
  // 只处理同源 GET 请求
  if (e.request.method !== 'GET') return;
  if (!e.request.url.startsWith(self.location.origin)) return;

  var url = new URL(e.request.url);

  e.respondWith(
    // 1. 先尝试网络（拿最新版本）
    fetch(e.request).then(function(resp) {
      // 网络成功，缓存后返回
      if (resp && resp.status === 200) {
        var clone = resp.clone();
        // 只缓存 HTML 和 JSON 数据
        if (url.pathname.endsWith('.html') || url.pathname.endsWith('.json')) {
          caches.open(RUNTIME_CACHE).then(function(cache) {
            cache.put(e.request, clone);
          });
        }
      }
      return resp;
    }).catch(function() {
      // 2. 网络失败，使用缓存兜底（离线场景）
      return caches.match(e.request).then(function(cached) {
        if (cached) return cached;
        // 没有缓存的 HTML 请求 → 返回离线提示
        var accept = e.request.headers.get('accept') || '';
        if (accept.indexOf('text/html') !== -1 || e.request.mode === 'navigate') {
          return offlinePage();
        }
        return new Response('', { status: 504, statusText: 'Offline' });
      });
    })
  );
});

// 离线提示页面
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