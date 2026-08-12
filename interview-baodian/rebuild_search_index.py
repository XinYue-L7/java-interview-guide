"""
从所有板块 HTML 重建 search_index.json
- 每条记录增加 content 字段（答案正文）
- 用于修复"搜索红黑树匹配 HashMap 答案"功能
"""
import re
import json
import os
import html as html_lib
from pathlib import Path

BASE = Path(r"D:\AiWordSpace\interview-baodian")

MODULE_NAMES = {
    "01_Java基础": "Java 基础",
    "02_集合容器": "Java 集合容器",
    "03_JVM": "JVM",
    "04_并发编程": "并发编程",
    "05_MySQL": "MySQL 数据库",
    "06_Redis": "Redis 缓存",
    "07_框架": "框架",
    "08_分布式&其他": "分布式 & 其他",
}

TAG_RE = re.compile(r'<span class="q-tag">([^<]+)</span>')
ANSWER_RE = re.compile(r'<div class="answer">(.*?)</div></div></div>', re.DOTALL)

# 通用：抓取一个 .card 块
CARD_BLOCK_RE = re.compile(r'<div class="card">(.*?)(?=<div class="card">|</div>\s*<div class="back|<script|<footer|</body)', re.DOTALL)

# 备用：用于行内简化的卡片（无 answer）
NUM_RE = re.compile(r'<div class="q-num">(\d+)</div>')
TITLE_RE = re.compile(r'<div class="q-title">([^<]+)</div>')

def strip_html(s):
    """去掉 HTML 标签，保留中文和基本标点"""
    s = re.sub(r'<style[^>]*>.*?</style>', '', s, flags=re.DOTALL)
    s = re.sub(r'<script[^>]*>.*?</script>', '', s, flags=re.DOTALL)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html_lib.unescape(s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def parse_cards(html_text, file_key, module_name):
    """从 HTML 中提取所有题目卡片"""
    items = []
    # 找出所有 .card ... </div></div></div> 块
    # 先用 Q编号 的位置分割
    # 简单策略：按 <div class="card"> 切分
    parts = re.split(r'<div class="card">', html_text)
    for part in parts[1:]:  # 跳过开头
        # 取到下一个 </div></div></div> 或下一个 card 之前
        end_match = re.search(r'</div>\s*<div class="back|<script|<footer|</body', part)
        if end_match:
            chunk = part[:end_match.start()]
        else:
            chunk = part

        num_m = NUM_RE.search(chunk)
        if not num_m:
            continue
        num = int(num_m.group(1))

        title_m = TITLE_RE.search(chunk)
        if not title_m:
            continue
        title = title_m.group(1).strip()

        tags = TAG_RE.findall(chunk)

        # 提取答案正文
        ans_m = ANSWER_RE.search(chunk)
        if ans_m:
            content = strip_html(ans_m.group(1))
        else:
            # 有些题目没有答案块
            content = ""

        items.append({
            "module": module_name,
            "file": f"Java面试宝典_{file_key}.html",
            "num": num,
            "title": title,
            "tags": tags,
            "content": content,
        })
    return items

def main():
    all_items = []
    for file_key, module_name in MODULE_NAMES.items():
        path = BASE / f"Java面试宝典_{file_key}.html"
        if not path.exists():
            print(f"[跳过] {path} 不存在")
            continue
        text = path.read_text(encoding="utf-8")
        items = parse_cards(text, file_key, module_name)
        print(f"[{module_name}] 解析 {len(items)} 题")
        all_items.extend(items)

    out_path = BASE / "search_index.json"
    out_path.write_text(
        json.dumps(all_items, ensure_ascii=False, indent=1),
        encoding="utf-8"
    )
    size_kb = out_path.stat().st_size / 1024
    print(f"\n[完成] 共 {len(all_items)} 题 → {out_path} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    main()