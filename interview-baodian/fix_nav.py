import os, re

d = r'D:\AiWordSpace'

# Define correct nav content for each file
nav_fixes = {
    'Java面试宝典_01_Java基础.html': '''<a href="Java面试宝典_总目录.html">总目录</a>
    <a href="Java面试宝典_02_集合容器.html">集合容器 →</a>''',
    'Java面试宝典_02_集合容器.html': '''<a href="Java面试宝典_总目录.html">总目录</a>
    <a href="Java面试宝典_01_Java基础.html">← Java基础</a>
    <a href="Java面试宝典_03_JVM.html">JVM →</a>''',
    'Java面试宝典_03_JVM.html': '''<a href="Java面试宝典_总目录.html">总目录</a>
    <a href="Java面试宝典_02_集合容器.html">← 集合容器</a>
    <a href="Java面试宝典_04_并发编程.html">并发编程 →</a>''',
    'Java面试宝典_04_并发编程.html': '''<a href="Java面试宝典_总目录.html">总目录</a>
    <a href="Java面试宝典_03_JVM.html">← JVM</a>
    <a href="Java面试宝典_05_MySQL.html">MySQL →</a>''',
    'Java面试宝典_05_MySQL.html': '''<a href="Java面试宝典_总目录.html">总目录</a>
    <a href="Java面试宝典_04_并发编程.html">← 并发编程</a>
    <a href="Java面试宝典_06_Redis.html">Redis →</a>''',
    'Java面试宝典_06_Redis.html': '''<a href="Java面试宝典_总目录.html">总目录</a>
    <a href="Java面试宝典_05_MySQL.html">← MySQL</a>
    <a href="Java面试宝典_07_框架.html">框架 →</a>''',
    'Java面试宝典_07_框架.html': '''<a href="Java面试宝典_总目录.html">总目录</a>
    <a href="Java面试宝典_06_Redis.html">← Redis</a>
    <a href="Java面试宝典_08_分布式&其他.html">分布式&其他 →</a>''',
    'Java面试宝典_08_分布式&其他.html': '''<a href="Java面试宝典_总目录.html">总目录</a>
    <a href="Java面试宝典_07_框架.html">← 框架</a>''',
}

for f, new_nav in nav_fixes.items():
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as fh:
        s = fh.read()

    s = re.sub(
        r'(<div class="nav-row">)(.*?)(</div>)',
        r'\1\n    ' + new_nav + r'\n  \3',
        s,
        flags=re.DOTALL
    )

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(s)

    print(f"OK: {f}")
