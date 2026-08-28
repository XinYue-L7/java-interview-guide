# -*- coding: utf-8 -*-
import subprocess, sys, os
os.chdir(r'D:\AiWordSpace\interview-baodian')
# Delete temp files
for f in ['check_ends.py', 'final_verify.py', 'fix_structure.py']:
    if os.path.exists(f):
        os.remove(f)
        print(f'Removed {f}')
# Git add and commit
subprocess.run(['git', 'add', '-A'])
result = subprocess.run(['git', 'commit', '-m', 'fix: 修复框架模块HTML结构（main→div，清理Spring末尾残留脚本）'],
                        capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)
