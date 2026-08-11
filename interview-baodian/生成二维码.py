import qrcode
import socket

def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

ip = get_lan_ip()
port = 9876
url = f"http://{ip}:{port}/Java面试宝典_总目录.html"

img = qrcode.make(url)
img.save("qrcode_lan.png")

print(f"二维码已生成: qrcode_lan.png")
print(f"访问地址: {url}")
print(f"\n请在手机/平板上用浏览器打开上述地址，或扫描 qrcode_lan.png 图片中的二维码。")
