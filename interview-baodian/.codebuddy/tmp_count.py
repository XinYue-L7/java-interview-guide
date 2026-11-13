import json, sys
sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open(r"D:\AiWordSpace\interview-baodian\search_index.json", encoding="utf-8"))
print("total:", len(d))
hot = [x for x in d if "高频" in (x.get("tags") or [])]
print("hot count:", len(hot))
# 各模块题数
from collections import Counter
c = Counter(x["file"] for x in d)
for f, n in c.items():
    if "01_Java基础" in f:
        print("01 module count:", n)
# 01 模块高频数
one = [x for x in d if "01_Java基础" in x["file"]]
print("01 hot count:", sum(1 for x in one if "高频" in (x.get("tags") or [])))
