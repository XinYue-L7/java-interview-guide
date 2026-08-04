# Java面试宝典 - 带缓存头的HTTP服务器
# 用法: python server.py
# 端口: 9876

import http.server
import socketserver
import os
import sys

PORT = 9876
DIR = os.path.dirname(os.path.abspath(__file__))

# 需要长期缓存的静态文件扩展名
CACHE_EXTS = {'.html', '.js', '.json', '.css', '.svg', '.png', '.jpg', '.ico', '.woff2', '.woff', '.ttf'}

class CachingHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def end_headers(self):
        path = self.path.split('?')[0]
        _, ext = os.path.splitext(path)
        ext = ext.lower()

        if ext in CACHE_EXTS:
            # 静态资源缓存24小时（离线可用）
            self.send_header('Cache-Control', 'max-age=86400, public, immutable')
        else:
            self.send_header('Cache-Control', 'no-cache')

        # 允许跨域（方便调试）
        self.send_header('Access-Control-Allow-Origin', '*')

        super().end_headers()

    def log_message(self, format, *args):
        # 简洁日志
        msg = "%s %s" % (self.address_string(), format % args)
        # 忽略 favicon 和探测请求
        if '/favicon.ico' in msg or 'Bad request' in msg:
            return
        sys.stderr.write(msg + '\n')


if __name__ == '__main__':
    os.chdir(DIR)
    with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), CachingHandler) as httpd:
        print("=" * 44)
        print("  Java面试宝典  本地服务启动中...")
        print("=" * 44)
        print()
        print("  本机访问:   http://localhost:%d/" % PORT)
        print()
        # 获取本机IP
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
            s.close()
            print("  局域网访问: http://%s:%d/" % (ip, PORT))
        except:
            print("  局域网访问: http://本机IP:%d/" % PORT)
        print()
        print("  Cache-Control 已启用 → 手机离线也能正常访问")
        print("  按 Ctrl+C 停止服务")
        print("=" * 44)
        print()
        httpd.serve_forever()
