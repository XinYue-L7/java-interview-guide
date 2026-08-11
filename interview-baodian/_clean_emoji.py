import os, re

d = r'D:\AiWordSpace'
files = [f for f in os.listdir(d) if f.startswith('Java面试宝典_0') and f.endswith('.html')]

for f in files:
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as fh:
        s = fh.read()

    # 去掉导航按钮里的 emoji
    s = s.replace('📚 总目录', '总目录')
    s = s.replace('🏠 总目录', '总目录')
    s = s.replace('→ ', '')
    s = s.replace('← ', '')

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(s)

    print(f"OK: {f}")
