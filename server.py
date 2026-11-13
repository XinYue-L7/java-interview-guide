# -*- coding: utf-8 -*-
"""Java 面试宝典本地预览服务
- http://localhost:9876/Java面试宝典_总目录.html
- 双栈监听（IPv4+IPv6）+ HTTP/1.1 keep-alive，毫秒级响应
- 旧地址 301 兼容、友好 404、SW 自动注销
- 不做 live-reload（SSE 长连接会占满浏览器并发配额导致页面卡死）
"""
import os
import http.server
import socketserver

PORT = 9876
DIR = r"D:\AiWordSpace\interview-baodian"

MIME = {".html": "text/html; charset=utf-8", ".json": "application/json; charset=utf-8",
        ".js": "text/javascript; charset=utf-8", ".svg": "image/svg+xml",
        ".png": "image/png", ".md": "text/plain; charset=utf-8"}

# 旧地址 → 新地址（文件改名后兼容旧链接/旧缓存）
REDIRECTS = {
    "/Java面试宝典_Docker容器化.html": "/Java面试宝典_Docker.html",
}

NOT_FOUND_HTML = """<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="3;url=/Java面试宝典_总目录.html">
<title>页面不存在 · Java 面试宝典</title>
<style>body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#0d0d1a;color:#eee;
display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:100vh;margin:0;text-align:center}
h1{font-size:48px;margin:0 0 12px}p{opacity:.75;margin:6px 0}
a{color:#d6b38a;text-decoration:none;border:1.5px solid #d6b38a;padding:8px 22px;border-radius:20px;display:inline-block;margin-top:16px}</style></head>
<body><h1>404</h1><p>页面不存在或已改名</p><p>3 秒后自动返回总目录…</p>
<a href="/Java面试宝典_总目录.html">立即返回总目录</a></body></html>"""


class Handler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # keep-alive 复用连接，避免反复建连

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def log_message(self, *args):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self):
        clean = self.path.split("?")[0].split("#")[0]
        from urllib.parse import unquote
        if "%" in clean:
            clean = unquote(clean)
        # 旧 live-reload 端点：204 让 EventSource 彻底停止重连（清理旧页面残留）
        if clean.rstrip("/").endswith("/_reload"):
            self.send_response(204)
            self.end_headers()
            self.close_connection = True
            return
        if clean in ("", "/"):
            clean = "/Java面试宝典_总目录.html"
        # 改名兼容：301 重定向
        if clean in REDIRECTS:
            from urllib.parse import quote
            self.send_response(301)
            self.send_header("Location", quote(REDIRECTS[clean]))
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        fp = os.path.join(DIR, clean.lstrip("/"))
        if clean.lower().endswith(".html") and os.path.isfile(fp):
            body = open(fp, "rb").read()
            self.send_response(200)
            self.send_header("Content-Type", MIME[".html"])
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if clean.lower().endswith(".html"):
            body = NOT_FOUND_HTML.encode("utf-8")
            self.send_response(404)
            self.send_header("Content-Type", MIME[".html"])
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


class DualStackServer(socketserver.ThreadingTCPServer):
    """同时监听 IPv6 与 IPv4，消除 localhost 的 IPv6 回退延迟"""
    allow_reuse_address = True
    daemon_threads = True
    request_queue_size = 128
    address_family = __import__("socket").AF_INET6

    def server_bind(self):
        import socket
        try:
            IPPROTO_IPV6 = getattr(socket, "IPPROTO_IPV6", 41)
            IPV6_V6ONLY = getattr(socket, "IPV6_V6ONLY", 27)
            self.socket.setsockopt(IPPROTO_IPV6, IPV6_V6ONLY, 0)
        except OSError:
            pass
        super().server_bind()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True
    request_queue_size = 128


if __name__ == "__main__":
    try:
        httpd = DualStackServer(("::", PORT), Handler)
    except OSError:
        httpd = Server(("127.0.0.1", PORT), Handler)  # IPv6 不可用时回退
    with httpd:
        print(f"服务已启动: http://localhost:{PORT}/Java面试宝典_总目录.html")
        httpd.serve_forever()
