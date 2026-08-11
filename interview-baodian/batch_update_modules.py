import re
import os

BASE = r"D:\AiWordSpace"

NEW_STYLE = '''::root,[data-theme="green"]{--primary:#2d6a4f;--hero-from:#1b4332;--hero-mid:#2d6a4f;--hero-to:#40916c;--bg:#f8faf9;--card-bg:#fff;--text:#2c3e50;--muted:#6c757d;--border:#dde8e2;--tag-bg:#e8f5e9;--success:#2e7d32;--code-bg:#1e1e1e;--answer-bg:#f9fafb;--shadow:rgba(0,0,0,.04)}
[data-theme="gold"]{--primary:#c9a96e;--hero-from:#0d0d1a;--hero-mid:#1a1a2e;--hero-to:#0d0d1a;--bg:#fafaf8;--card-bg:#fff;--text:#1a1a2e;--muted:#888;--border:#e8e4dc;--tag-bg:#faf5ed;--success:#2d6a4f;--code-bg:#1a1a2e;--answer-bg:#f9fafb;--shadow:rgba(0,0,0,.04)}
[data-theme="purple"]{--primary:#5b4f8b;--hero-from:#2d2640;--hero-mid:#3f3556;--hero-to:#5b4f8b;--bg:#f9f8fb;--card-bg:#fff;--text:#2d2640;--muted:#7a7a8c;--border:#e4e0ee;--tag-bg:#f3f0f8;--success:#2d6a4f;--code-bg:#1e1b2e;--answer-bg:#f9fafb;--shadow:rgba(0,0,0,.04)}
[data-theme="light"]{--primary:#2563eb;--hero-from:#3b82f6;--hero-mid:#60a5fa;--hero-to:#93c5fd;--bg:#f0f4f8;--card-bg:#fff;--text:#1e293b;--muted:#64748b;--border:#e2e8f0;--tag-bg:#eff6ff;--success:#059669;--code-bg:#1e1e1e;--answer-bg:#f8fafc;--shadow:rgba(0,0,0,.04)}
[data-theme="dark"]{--primary:#60a5fa;--hero-from:#0f172a;--hero-mid:#1e293b;--hero-to:#334155;--bg:#0f172a;--card-bg:#1e293b;--text:#f1f5f9;--muted:#94a3b8;--border:#334155;--tag-bg:#334155;--success:#34d399;--code-bg:#0f172a;--answer-bg:#1e293b;--shadow:rgba(0,0,0,.2)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);line-height:1.75}
.hero{background:linear-gradient(135deg,var(--hero-from) 0%,var(--hero-mid) 40%,var(--hero-to) 100%);color:#fff;padding:32px 24px 24px;text-align:center;position:relative}
.hero h1{font-size:26px;font-weight:800;margin-bottom:4px}
.hero p{opacity:.85;font-size:14px}
.hero .nav-row{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-top:12px}
.nav-row a{font-size:12px;padding:3px 12px;border-radius:14px;text-decoration:none;color:#fff;border:1.5px solid rgba(255,255,255,.35);background:rgba(255,255,255,.08);cursor:pointer;transition:.2s}
.nav-row a:hover{background:rgba(255,255,255,.2)}
.container{max-width:860px;margin:0 auto;padding:24px 18px 50px}
.card{background:var(--card-bg);border-radius:12px;box-shadow:0 1px 4px var(--shadow);margin-bottom:16px;overflow:hidden;border:1px solid var(--border);transition:box-shadow .2s}
.card:hover{box-shadow:0 3px 14px var(--shadow)}
.card-header{display:flex;align-items:flex-start;gap:10px;padding:16px 18px 0}
.q-num{flex-shrink:0;width:30px;height:30px;background:var(--primary);color:#fff;border-radius:6px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px}
.q-meta{flex:1;min-width:0}
.q-title{font-size:16px;font-weight:700;color:var(--text)}
.q-tags{display:flex;gap:4px;flex-wrap:wrap;margin-top:4px}
.q-tag{font-size:11px;background:var(--tag-bg);color:var(--primary);padding:2px 9px;border-radius:10px;font-weight:500}
.card-body{padding:12px 18px 16px}
.toggle-btn{display:inline-flex;align-items:center;gap:4px;background:none;border:1.5px solid var(--primary);color:var(--primary);font-size:12px;font-weight:600;padding:4px 13px;border-radius:16px;cursor:pointer;margin-top:2px;transition:.2s}
.toggle-btn:hover,.toggle-btn.open{background:var(--primary);color:#fff}
.toggle-btn .arrow{font-size:10px;transition:transform .2s}
.toggle-btn.open .arrow{transform:rotate(180deg)}
.answer{display:none;margin-top:12px;padding:14px 16px;background:var(--answer-bg);border-radius:10px;border-left:4px solid var(--primary)}
.answer.show{display:block}
.answer p{margin-bottom:6px;font-size:14px}
.answer ul,.answer ol{padding-left:18px;margin-bottom:6px;font-size:14px}
.answer li{margin-bottom:3px}
.answer strong{color:var(--success)}
.code-block{background:var(--code-bg);color:#d4d4d4;border-radius:8px;padding:12px 14px;overflow-x:auto;font-family:"JetBrains Mono","Fira Code",Consolas,monospace;font-size:12px;line-height:1.6;margin:8px 0;white-space:pre}
.code-block .kw{color:#569cd6}.code-block .str{color:#ce9178}.code-block .co{color:#6a9955}.code-block .fn{color:#dcdcaa}.code-block .num{color:#b5cea8}
.table-wrap{overflow-x:auto;margin:6px 0}
.table-wrap table{width:100%;border-collapse:collapse;font-size:13px}
.table-wrap th{background:var(--tag-bg);text-align:left;padding:7px 10px;font-weight:600;border-bottom:2px solid var(--primary)}
.table-wrap td{padding:7px 10px;border-bottom:1px solid var(--border)}
.footer{text-align:center;font-size:13px;color:var(--muted);padding:16px 0 0}
.theme-fixed{position:fixed;top:16px;left:16px;z-index:1000}
.theme-toggle-btn{width:40px;height:40px;border-radius:10px;border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.15);color:#fff;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center;backdrop-filter:blur(4px);transition:.2s}
.theme-toggle-btn:hover{background:rgba(255,255,255,.3)}
.theme-dropdown{display:none;position:absolute;top:48px;left:0;background:var(--card-bg);border:1px solid var(--border);border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.12);padding:6px;min-width:140px}
.theme-dropdown.show{display:block}
.theme-dropdown button{display:block;width:100%;text-align:left;padding:8px 12px;border:none;background:none;color:var(--text);font-size:13px;border-radius:6px;cursor:pointer;transition:.2s}
.theme-dropdown button:hover{background:var(--tag-bg)}
.theme-dropdown button.active{color:var(--primary);font-weight:600}
.theme-dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:8px}
.dot-green{background:#2d6a4f}.dot-gold{background:#c9a96e}.dot-purple{background:#5b4f8b}.dot-light{background:#2563eb}.dot-dark{background:#334155}
.feedback-row{margin-top:10px;display:flex;gap:8px}
.feedback-btn{font-size:11px;padding:3px 10px;border:1px solid var(--border);background:transparent;color:var(--muted);border-radius:12px;cursor:pointer;transition:.2s}
.feedback-btn:hover{border-color:var(--primary);color:var(--primary);background:var(--tag-bg)}
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:2000;align-items:center;justify-content:center}
.modal-overlay.show{display:flex}
.modal-box{background:var(--card-bg);border-radius:14px;padding:24px;width:90%;max-width:460px;box-shadow:0 20px 60px rgba(0,0,0,.2);border:1px solid var(--border)}
.modal-box h3{margin-bottom:16px;font-size:17px}
.modal-box label{display:block;font-size:13px;color:var(--muted);margin-bottom:6px}
.modal-box select,.modal-box textarea{width:100%;padding:8px 10px;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text);font-size:13px;margin-bottom:14px;font-family:inherit}
.modal-box textarea{min-height:80px;resize:vertical}
.modal-actions{display:flex;gap:8px;justify-content:flex-end}
.modal-actions button{padding:6px 16px;border-radius:8px;border:none;cursor:pointer;font-size:13px}
.modal-cancel{background:var(--tag-bg);color:var(--muted)}
.modal-confirm{background:var(--primary);color:#fff}
.modal-output{background:var(--answer-bg);border:1px solid var(--border);border-radius:8px;padding:10px;font-size:12px;white-space:pre-wrap;word-break:break-all;margin-top:12px;max-height:120px;overflow-y:auto}'''

THEME_BTN_HTML = '''  <div class="theme-fixed">
    <button class="theme-toggle-btn" onclick="toggleThemeMenu()" title="切换主题">🎨</button>
    <div class="theme-dropdown" id="themeDropdown">
      <button onclick="setTheme('green')" id="btn-green"><span class="theme-dot dot-green"></span>深绿色</button>
      <button onclick="setTheme('gold')" id="btn-gold"><span class="theme-dot dot-gold"></span>黑白金</button>
      <button onclick="setTheme('purple')" id="btn-purple"><span class="theme-dot dot-purple"></span>紫色</button>
      <button onclick="setTheme('light')" id="btn-light"><span class="theme-dot dot-light"></span>浅色模式</button>
      <button onclick="setTheme('dark')" id="btn-dark"><span class="theme-dot dot-dark"></span>深色模式</button>
    </div>
  </div>
'''

NEW_SCRIPT = '''<script>
function toggleAnswer(b){var a=b.nextElementSibling,c=a.classList.contains('show');a.classList.toggle('show');b.classList.toggle('open');b.innerHTML=c?'查看答案 <span class="arrow">▼</span>':'收起答案 <span class="arrow">▼</span>'}
function setTheme(t){document.documentElement.setAttribute('data-theme',t);document.querySelectorAll('.theme-dropdown button').forEach(b=>b.classList.remove('active'));var btn=document.getElementById('btn-'+t);if(btn)btn.classList.add('active');localStorage.setItem('interview-theme',t);document.getElementById('themeDropdown').classList.remove('show')}
function toggleThemeMenu(){document.getElementById('themeDropdown').classList.toggle('show')}
document.addEventListener('click',function(e){if(!e.target.closest('.theme-fixed'))document.getElementById('themeDropdown').classList.remove('show')});
(function(){var t=localStorage.getItem('interview-theme')||'gold';document.documentElement.setAttribute('data-theme',t);var btn=document.getElementById('btn-'+t);if(btn)btn.classList.add('active');})();
var currentQid='',currentQtitle='';
function openFeedback(qid,qtitle){currentQid=qid;currentQtitle=qtitle;document.getElementById('fb-qid').textContent=qid;document.getElementById('fb-qtitle').textContent=qtitle;document.getElementById('fb-type').value='';document.getElementById('fb-desc').value='';document.getElementById('fb-output').style.display='none';document.getElementById('feedbackModal').classList.add('show')}
function closeFeedback(){document.getElementById('feedbackModal').classList.remove('show')}
function genFeedback(){var type=document.getElementById('fb-type').value,desc=document.getElementById('fb-desc').value.trim();if(!type){alert('请选择问题类型');return}var out='【题目反馈】\\n模块：'+document.title+'\\n题号：'+currentQid+'\\n题目：'+currentQtitle+'\\n问题类型：'+type+(desc?'\\n详细描述：'+desc:'');document.getElementById('fb-output').textContent=out;document.getElementById('fb-output').style.display='block'}
</script>
<div class="modal-overlay" id="feedbackModal" onclick="if(event.target===this)closeFeedback()">
  <div class="modal-box">
    <h3>📝 题目反馈</h3>
    <p style="font-size:12px;color:var(--muted);margin-bottom:12px">题号 <span id="fb-qid"></span> · <span id="fb-qtitle"></span></p>
    <label>问题类型</label>
    <select id="fb-type"><option value="">请选择</option><option value="答案错误">答案错误</option><option value="答案不完整">答案不完整</option><option value="题目表述不清">题目表述不清</option><option value="其他">其他</option></select>
    <label>详细描述（可选）</label>
    <textarea id="fb-desc" placeholder="请描述具体问题..."></textarea>
    <div class="modal-actions"><button class="modal-cancel" onclick="closeFeedback()">取消</button><button class="modal-confirm" onclick="genFeedback()">生成反馈文本</button></div>
    <div class="modal-output" id="fb-output" style="display:none"></div>
  </div>
</div>'''


def find_closing_div(html, start):
    depth = 1
    i = start
    while i < len(html) and depth > 0:
        open_pos = html.find('<div', i)
        close_pos = html.find('</div>', i)
        if close_pos == -1:
            break
        if open_pos != -1 and open_pos < close_pos:
            depth += 1
            i = open_pos + 4
        else:
            depth -= 1
            if depth == 0:
                return close_pos + 6
            i = close_pos + 6
    return -1


files = [f for f in os.listdir(BASE) if f.startswith('Java面试宝典_') and f.endswith('.html') and '总目录' not in f]
files.sort()

for fname in files:
    path = os.path.join(BASE, fname)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. 替换 style
    html = re.sub(r'<style>.*?</style>', f'<style>\n{NEW_STYLE}\n</style>', html, count=1, flags=re.DOTALL)

    # 2. 移除 theme-switcher
    html = re.sub(r'<div class="theme-switcher">.*?</div>\s*', '', html, count=1, flags=re.DOTALL)

    # 3. 移除 edit-toolbar
    html = re.sub(r'<div class="edit-toolbar">.*?</div>\s*', '', html, count=1, flags=re.DOTALL)

    # 4. 在 hero 开头插入主题按钮
    html = html.replace('<div class="hero">', f'<div class="hero">\n{THEME_BTN_HTML}')

    # 5. 移除 edit-answer.js
    html = re.sub(r'<script src="edit-answer\.js"></script>\s*', '', html)

    # 6. 替换 script（第一个内联 script）
    html = re.sub(r'<script>.*?</script>\s*', f'<script>\n{NEW_SCRIPT}\n', html, count=1, flags=re.DOTALL)

    # 7. 为每道题添加反馈按钮
    pos = 0
    new_html = ''
    while True:
        card_start = html.find('<div class="card">', pos)
        if card_start == -1:
            new_html += html[pos:]
            break

        new_html += html[pos:card_start]

        card_end = find_closing_div(html, card_start + len('<div class="card">'))
        if card_end == -1:
            new_html += html[card_start:]
            break

        card_html = html[card_start:card_end]

        # 提取题号
        qnum_match = re.search(r'<div class="q-num">(\d+)</div>', card_html)
        qnum = qnum_match.group(1) if qnum_match else '?'

        # 提取题目
        qtitle_match = re.search(r'<div class="q-title">(.*?)</div>', card_html)
        qtitle = qtitle_match.group(1).strip() if qtitle_match else ''
        qtitle = qtitle.replace("\\", "\\\\").replace("'", "\\'").replace('\n', ' ').replace('\r', '').strip()

        # 找到 card-body 并在其闭合前插入反馈
        body_start = card_html.find('<div class="card-body">')
        if body_start != -1:
            body_inner_start = body_start + len('<div class="card-body">')
            body_end = find_closing_div(card_html, body_inner_start)
            if body_end != -1:
                feedback_html = f'<div class="feedback-row"><button class="feedback-btn" onclick="openFeedback(\'{qnum}\',\'{qtitle}\')">📝 题目反馈</button></div>'
                card_html = card_html[:body_end] + feedback_html + card_html[body_end:]

        new_html += card_html
        pos = card_end

    html = new_html

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'Updated {fname}')
