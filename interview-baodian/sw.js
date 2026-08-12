// Service Worker v4 - Java面试宝典 PWA离线缓存
// 策略：运行时缓存（不预缓存），避免中文URL编码不一致问题
// 配合服务器 Cache-Control 头，双重保障离线可用

var CACHE_NAME = 'interview-baodian-v5';

// 安装：立即接管，不等待旧SW
self.addEventListener('install', function(e) {
  self.skipWaiting();
});

// 激活：清理旧缓存，接管所有页面
self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(function(k) { return k !== CACHE_NAME; })
             .map(function(k) { return caches.delete(k); })
      );
    })
  );
  self.clients.claim();
});

// 请求拦截：运行时缓存
self.addEventListener('fetch', function(e) {
  // 只处理同源GET请求
  if (e.request.method !== 'GET') return;
  if (!e.request.url.startsWith(self.location.origin)) return;

  e.respondWith(
    caches.match(e.request).then(function(cached) {
      if (cached) {
        // 缓存命中，直接返回
        return cached;
      }

      // 缓存未命中，走网络
      return fetch(e.request).then(function(resp) {
        // 只缓存成功响应（200）
        if (resp.status === 200) {
          var clone = resp.clone();
          caches.open(CACHE_NAME).then(function(cache) {
            cache.put(e.request, clone);
          });
        }
        return resp;
      }).catch(function() {
        // 网络完全失败时的兜底
        var accept = e.request.headers.get('accept') || '';

        // HTML页面请求 → 返回离线提示页
        if (accept.indexOf('text/html') !== -1 || e.request.mode === 'navigate') {
          // 尝试返回任意已缓存的HTML页面
          return caches.keys().then(function(keys) {
            if (keys.length === 0) {
              return offlinePage();
            }
            // 优先找总目录页
            for (var i = 0; i < keys.length; i++) {
              if (keys[i].indexOf('面试宝典_总目录') !== -1 ||
                  keys[i].indexOf('E6%80%BB%E7%9B%AE') !== -1) {
                return caches.match(keys[i]);
              }
            }
            // 返回任意HTML页面
            return caches.match(keys[0]);
          }).then(function(r) {
            return r || offlinePage();
          });
        }

        // 非HTML请求 → 直接返回空
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
    '<h1>📴 已离线</h1>' +
    '<p>请先联网访问一次面试宝典页面，之后即可离线使用。</p>' +
    '<p style="font-size:12px">当前缓存为空，需要首次联网加载。</p>' +
    '</body></html>';
  return new Response(html, { headers: { 'Content-Type': 'text/html;charset=UTF-8' } });
}
