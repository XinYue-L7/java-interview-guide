import os
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

for f in ['git_check.py', 'git_final.py']:
    if os.path.exists(f):
        os.remove(f)
        print(f'已删除: {f}')

r = subprocess.run(['git', 'add', '-A'], capture_output=True, text=True, encoding='utf-8', errors='replace')
r = subprocess.run(['git', 'commit', '-m', '清理临时脚本'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r.stdout)
r = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('status:', r.stdout if r.stdout.strip() else '(工作区干净)')
