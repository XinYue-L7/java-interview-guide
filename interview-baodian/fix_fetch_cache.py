import os, re

d = r'D:\AiWordSpace'
files = [f for f in os.listdir(d) if f.endswith('.html')]

old_fetch = "fetch('search_index.json').then(function(r){return r.json();}).then(function(d){searchIndex=d;searchReady=true;}).catch(function(e){console.error('搜索索引加载失败',e);});"

new_fetch = "fetch('search_index.json?v=2').then(function(r){return r.json();}).then(function(d){searchIndex=d;searchReady=true;console.log('搜索索引加载成功，共'+d.length+'条');}).catch(function(e){console.error('搜索索引加载失败',e);});"

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
        print(f'  [SKIP] {f}')

print('全部完成')
