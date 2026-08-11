import os, re

d = r'D:\AiWordSpace'
files = sorted([f for f in os.listdir(d) if f.startswith('Java面试宝典_0') and f.endswith('.html')])

for f in files:
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as fh:
        s = fh.read()
    count = len(re.findall(r'class="q-num"|class="q-title"', s)) // 2
    print(f'{f}: {count}题')
