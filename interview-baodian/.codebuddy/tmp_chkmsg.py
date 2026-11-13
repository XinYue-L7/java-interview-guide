import subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
b = subprocess.run(["git", "-C", r"D:\AiWordSpace", "cat-file", "commit", "HEAD"],
                   capture_output=True).stdout
msg = b.split(b"\n\n", 1)[1].strip()
print("raw bytes head:", msg[:12])
print("valid utf-8:", True) if (lambda s: True)(msg.decode("utf-8")) else None
try:
    t = msg.decode("utf-8")
    print("decoded:", t[:30])
except UnicodeDecodeError as e:
    print("NOT valid utf-8:", e)
    print("as gbk:", msg[:30].decode("gbk", "replace"))
