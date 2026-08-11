import json

data = json.load(open(r'D:\AiWordSpace\search_index.json', 'r', encoding='utf-8'))

q = '多线程'

# 模拟前端 match 函数
def match(item, term):
    t = item['title'].lower()
    m = item['module'].lower()
    g = ' '.join(item.get('tags', [])).lower()
    return term in t or term in m or term in g

# 精确匹配
results = [x for x in data if match(x, q)]
print(f'搜索"{q}": {len(results)}条')
for x in results[:5]:
    print(f'  - [{x["module"]}] {x["title"]}')

# 检查 tags
print(f'\n检查第一条并发编程数据的tags:')
concurrent = [x for x in data if '并发' in x['module']]
if concurrent:
    c = concurrent[0]
    print(f'  tags: {c.get("tags")}')
    g = ' '.join(c.get('tags', [])).lower()
    print(f'  tags字符串: "{g}"')
    print(f'  "多线程" in tags: {"多线程" in g}')
