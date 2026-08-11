import os

TARGET_DIR = r"D:\AiWordSpace"
FILES = [
    "Java面试宝典_总目录.html",
    "Java面试宝典_01_Java基础.html",
    "Java面试宝典_02_集合容器.html",
    "Java面试宝典_03_JVM.html",
    "Java面试宝典_04_并发编程.html",
    "Java面试宝典_05_MySQL.html",
    "Java面试宝典_06_Redis.html",
    "Java面试宝典_07_框架.html",
    "Java面试宝典_08_分布式&其他.html",
]

OLD_FETCH = "var searchIndex=[];\nfetch('search_index.json').then(r=>r.json()).then(d=>{searchIndex=d;});"
NEW_FETCH = "var searchIndex=[];\nvar searchReady=false;\nfetch('search_index.json').then(function(r){return r.json();}).then(function(d){searchIndex=d;searchReady=true;}).catch(function(e){console.error('搜索索引加载失败',e);});"

OLD_CHECK = "if(!searchIndex.length){dd.classList.remove('show');return;}"
NEW_CHECK = "if(!searchReady){dd.innerHTML='<div class=\"search-empty\">搜索索引加载中，请稍候...</div>';dd.classList.add('show');return;}"

success = 0
for fname in FILES:
    fpath = os.path.join(TARGET_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    
    content = content.replace(OLD_FETCH, NEW_FETCH)
    content = content.replace(OLD_CHECK, NEW_CHECK)
    
    if content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] {fname}")
        success += 1
    else:
        print(f"[SKIP] {fname}")

print(f"\n完成: 成功 {success} 个")
