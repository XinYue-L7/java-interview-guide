import os

d = r'D:\AiWordSpace'
files = [f for f in os.listdir(d) if f.endswith('.html')]

# 用更强的缓存破坏 - 加时间戳参数
old_fetch = "fetch('search_index.json?v=2')"
new_fetch = "fetch('search_index.json?t='+Date.now())"

for f in files:
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as fh:
        s = fh.read()
    if old_fetch in s:
        s = s.replace(old_fetch, new_fetch)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(s)
        print(f'  [OK] {f}')
    else:
        print(f'  [SKIP] {f} - not found')

print('全部完成')
