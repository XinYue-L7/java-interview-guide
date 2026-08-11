import os, re, json

d = r'D:\AiWordSpace'
files = sorted([f for f in os.listdir(d) if f.startswith('Java面试宝典_0') and f.endswith('.html')])

# 模块标签映射（基于文件序号）
TAG_MAP = {
    '01': ['基础', '面向对象', 'String', '异常', '反射', 'IO', '泛型', '注解'],
    '02': ['集合', 'List', 'Map', 'Set', 'ArrayList', 'HashMap', 'ConcurrentHashMap', '红黑树'],
    '03': ['JVM', '垃圾回收', 'GC', '类加载', '内存模型', 'OOM', '调优'],
    '04': ['并发', '多线程', '线程', '锁', '线程池', 'JUC', 'volatile', 'CAS', '死锁'],
    '05': ['MySQL', 'SQL', '索引', '事务', '锁', '优化', 'B+树', 'InnoDB'],
    '06': ['Redis', '缓存', '分布式锁', '持久化', '数据结构', '集群'],
    '07': ['Spring', 'SpringBoot', 'SpringMVC', 'MyBatis', '框架', '中间件', 'IOC', 'AOP'],
    '08': ['分布式', '微服务', '消息队列', 'RocketMQ', 'Kafka', 'Zookeeper', 'Dubbo']
}

index = []
for f in files:
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as fh:
        s = fh.read()
    title_match = re.search(r'<h1>(.*?)</h1>', s)
    module = title_match.group(1) if title_match else f
    # 提取序号
    m = re.search(r'Java面试宝典_(\d+)', f)
    num_key = m.group(1) if m else ''
    tags = TAG_MAP.get(num_key, [])
    # 提取每个题目的标题和题号
    cards = re.findall(r'<div class="q-num">(\d+)</div>.*?<div class="q-title">(.*?)</div>', s, re.DOTALL)
    for num, title in cards:
        index.append({
            'module': module,
            'file': f,
            'num': int(num),
            'title': title.strip(),
            'tags': tags
        })

with open(os.path.join(d, 'search_index.json'), 'w', encoding='utf-8') as fh:
    json.dump(index, fh, ensure_ascii=False, indent=2)

print(f'索引完成，共 {len(index)} 道题')

# 批量修改所有页面的 doSearch，支持 tags 搜索
html_files = [f for f in os.listdir(d) if f.endswith('.html')]

old_match = '''  function match(item,term){
    var t=item.title.toLowerCase();
    var m=item.module.toLowerCase();
    return t.indexOf(term)!==-1 || m.indexOf(term)!==-1;
  }'''

new_match = '''  function match(item,term){
    var t=item.title.toLowerCase();
    var m=item.module.toLowerCase();
    var g=(item.tags||[]).join(' ').toLowerCase();
    return t.indexOf(term)!==-1 || m.indexOf(term)!==-1 || g.indexOf(term)!==-1;
  }'''

for f in html_files:
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as fh:
        s = fh.read()
    if old_match in s:
        s = s.replace(old_match, new_match)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(s)
        print(f'  [OK] {f}')
    else:
        print(f'  [SKIP] {f}')

print('全部完成')
