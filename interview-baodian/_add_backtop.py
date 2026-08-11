import os, re

d = r'D:\AiWordSpace'
files = [f for f in os.listdir(d) if f.startswith('Java面试宝典_0') and f.endswith('.html')]

for f in files:
    path = os.path.join(d, f)
    with open(path, 'r', encoding='utf-8') as fh:
        s = fh.read()

    # 添加 CSS 在 </style> 前
    css = """
.back-top{position:fixed;left:20px;bottom:40px;z-index:200;width:42px;height:42px;border-radius:50%;background:var(--primary);color:#fff;border:none;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,.2);opacity:0;visibility:hidden;transform:translateY(10px);transition:all .25s}
.back-top.show{opacity:1;visibility:visible;transform:translateY(0)}
.back-top:hover{transform:translateY(-3px);box-shadow:0 4px 14px rgba(0,0,0,.3)}
"""
    s = s.replace('</style>', css + '</style>')

    # 添加 HTML + JS 在 </body> 前
    html = """
<button class="back-top" id="backTop" onclick="window.scrollTo({top:0,behavior:'smooth'})" title="回到顶部">↑</button>
<script>
var bt=document.getElementById('backTop');
function onScroll(){if(window.scrollY>300){bt.classList.add('show');}else{bt.classList.remove('show');}}
window.addEventListener('scroll',onScroll);onScroll();
</script>
"""
    s = s.replace('</body>', html + '</body>')

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(s)

    print(f"OK: {f}")
