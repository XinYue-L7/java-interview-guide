import os
import re

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

# 新的 doSearch 函数：支持 title+module 搜索，支持多关键词 AND，支持模糊回退
NEW_DOSEARCH = """function doSearch(q){
  q=q.trim().toLowerCase();
  var dd=document.getElementById('searchDropdown');
  if(!q){showHistory();return;}
  if(!searchIndex.length){dd.classList.remove('show');return;}
  var keywords=q.split(/\\s+/).filter(function(x){return x.length>0;});
  function match(item,term){
    var t=item.title.toLowerCase();
    var m=item.module.toLowerCase();
    return t.indexOf(term)!==-1 || m.indexOf(term)!==-1;
  }
  // 1. 精确 AND 匹配（每个关键词都要命中）
  var results=searchIndex.filter(function(item){
    return keywords.every(function(term){return match(item,term);});
  });
  // 2. 如果没有结果且关键词>2个字，尝试去掉第一个字再匹配
  if(!results.length){
    var fallback=keywords.map(function(k){return k.length>2?k.substring(1):k;});
    results=searchIndex.filter(function(item){
      return fallback.every(function(term){return match(item,term);});
    });
  }
  // 3. 如果还没有结果，尝试 OR 匹配（至少命中一个词）
  if(!results.length){
    results=searchIndex.filter(function(item){
      return keywords.some(function(term){return match(item,term);});
    });
  }
  addHistory(q);
  if(!results.length){dd.innerHTML='<div class="search-empty">未找到相关题目</div>';dd.classList.add('show');return;}
  dd.innerHTML=results.slice(0,20).map(function(item){
    return '<a class="search-item" href="'+item.file+'?q='+item.num+'" target="_blank"><div class="search-item-title">'+escapeHtml(item.title)+'</div><div class="search-item-module">'+escapeHtml(item.module)+' · 第 '+item.num+' 题</div></a>';
  }).join('');
  dd.classList.add('show');
}"""

# 旧函数的正则匹配模式（提取旧函数以便替换）
OLD_PATTERN = re.compile(
    r'function doSearch\(q\)\{[^}]+\}[^}]+\}[^}]+\}[^}]+\}'
)

success = 0
for fname in FILES:
    fpath = os.path.join(TARGET_DIR, fname)
    if not os.path.exists(fpath):
        print(f"[SKIP] {fname} — 不存在")
        continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    
    # 尝试匹配并替换旧的 doSearch
    # 由于旧函数格式在不同文件中可能略有不同，用更灵活的方式
    # 找到 "function doSearch(q){" 开头，到第一个匹配的闭合 "}" 结束
    start = content.find('function doSearch(q){')
    if start == -1:
        print(f"[WARN] {fname} — 未找到 doSearch")
        continue
    
    # 找到这个函数的结束位置（考虑嵌套大括号）
    brace_count = 0
    i = start
    found_open = False
    while i < len(content):
        if content[i] == '{':
            brace_count += 1
            found_open = True
        elif content[i] == '}':
            brace_count -= 1
            if found_open and brace_count == 0:
                break
        i += 1
    end = i + 1  # 包含闭合 }
    
    content = content[:start] + NEW_DOSEARCH + content[end:]
    
    if content != original:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] {fname}")
        success += 1
    else:
        print(f"[SKIP] {fname} — 未改变")

print(f"\n完成: 成功 {success} 个")
