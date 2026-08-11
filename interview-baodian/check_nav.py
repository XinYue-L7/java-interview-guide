import os, re

d = r'D:\AiWordSpace'
files = sorted([f for f in os.listdir(d) if f.startswith('Java面试宝典_0') and f.endswith('.html')])

for f in files:
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as fh:
        s = fh.read()
    m = re.search(r'<div class="nav-row">(.*?)</div>', s, re.DOTALL)
    if m:
        content = m.group(1).strip()
        content = content.replace('\n', ' ')
        print(f + ': ' + content)
    else:
        print(f + ': (not found)')
