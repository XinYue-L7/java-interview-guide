import os
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 删除临时文件
for f in ['fix_all.py', 'git_status.py']:
    if os.path.exists(f):
        os.remove(f)
        print(f'已删除: {f}')

# git add 和 commit
r = subprocess.run(['git', 'add', '-A'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('add:', r.returncode)

commit_msg = '统一拆分模块样式：修复CSS变量、card标签损坏、导航链、footer、回首页按钮，与旧模块展示样式一致'
r = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r.stdout)
print(r.stderr)
