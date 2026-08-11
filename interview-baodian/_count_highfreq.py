import os, re

d = r'D:\AiWordSpace'
total = 0
for i in range(1,9):
    f = f'Java面试宝典_{i:02d}_'
    fname = [x for x in os.listdir(d) if x.startswith(f) and x.endswith('.html')]
    if not fname:
        continue
    content = open(os.path.join(d, fname[0]), encoding='utf-8').read()
    # count occurrences of >高频< in q-tag spans
    n = len(re.findall(r'<span class="q-tag">高频</span>', content))
    total += n
    print(f'{fname[0]}  → {n} 道高频')
print(f'\n总计高频题: {total} 道')
