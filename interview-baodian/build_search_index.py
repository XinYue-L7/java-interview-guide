import os, re, json

d = r'D:\AiWordSpace'
files = sorted([f for f in os.listdir(d) if f.startswith('Java面试宝典_0') and f.endswith('.html')])

index = []
for f in files:
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as fh:
        s = fh.read()
    title_match = re.search(r'<h1>(.*?)</h1>', s)
    module = title_match.group(1) if title_match else f
    # 提取每个题目的标题和题号
    cards = re.findall(r'<div class="q-num">(\d+)</div>.*?<div class="q-title">(.*?)</div>', s, re.DOTALL)
    for num, title in cards:
        index.append({
            'module': module,
            'file': f,
            'num': int(num),
            'title': title.strip()
        })

with open(os.path.join(d, 'search_index.json'), 'w', encoding='utf-8') as fh:
    json.dump(index, fh, ensure_ascii=False, indent=2)

print(f'索引完成，共 {len(index)} 道题')
