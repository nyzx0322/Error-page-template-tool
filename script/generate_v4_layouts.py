import os
import re

# Directory
# 使用相对于脚本文件的路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 假设 HTML 文件在脚本目录的上一级目录
DIR = os.path.dirname(SCRIPT_DIR)

FILES = [
    '400.html', '401.html', '403.html', '404.html', '405.html', 
    '408.html', '413.html', '414.html', '429.html', '499.html',
    '500.html', '501.html', '502.html', '503.html', '504.html', 
    '505.html', '506.html', '507.html', '509.html', '510.html'
]

PATTERNS = {
    'noise': 'url("data:image/svg+xml,%3Csvg viewBox=\'0 0 200 200\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cfilter id=\'noise\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'0.65\' numOctaves=\'3\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'100%25\' height=\'100%25\' filter=\'url(%23noise)\' opacity=\'0.04\'/%3E%3C/svg%3E")',
    'dots': 'radial-gradient(var(--muted) 1px, transparent 1px)',
    'grid': 'linear-gradient(to right, var(--card-border-color) 1px, transparent 1px), linear-gradient(to bottom, var(--card-border-color) 1px, transparent 1px)',
    'stripes': 'repeating-linear-gradient(45deg, var(--card-border-color), var(--card-border-color) 10px, transparent 10px, transparent 20px)',
    'waves': 'radial-gradient(circle at 100% 50%, transparent 20%, var(--card-border-color) 21%, var(--card-border-color) 34%, transparent 35%, transparent), radial-gradient(circle at 0% 50%, transparent 20%, var(--card-border-color) 21%, var(--card-border-color) 34%, transparent 35%, transparent) 0 50px'
}

THEMES = {
    'default': {'accent1': '#38bdf8', 'accent2': '#818cf8', 'template': 'default'},
    'server_error': {'accent1': '#f43f5e', 'accent2': '#e11d48', 'template': 'terminal'},
    'client_error': {'accent1': '#fbbf24', 'accent2': '#f59e0b', 'template': 'default'},
    'forbidden': {'accent1': '#c084fc', 'accent2': '#a855f7', 'template': 'security'},
    'not_found': {'accent1': '#2dd4bf', 'accent2': '#0ea5e9', 'template': 'split'},
    'timeout': {'accent1': '#f97316', 'accent2': '#ea580c', 'template': 'default'},
}

def get_theme(code):
    try:
        c = int(code)
        if c == 404: return THEMES['not_found']
        if c in [401, 403]: return THEMES['forbidden']
        if c in [408, 504, 502]: return THEMES['timeout']
        if 400 <= c < 500: return THEMES['client_error']
        if 500 <= c < 600: return THEMES['server_error']
    except: pass
    return THEMES['default']

# ================= TEMPLATES (PLACEHOLDERS, ACTUAL CONTENT SAME AS update_pages.py) =================
# 为了保持脚本完整性，这里我完整复制了 v4 的模板内容

TEMPLATE_DEFAULT = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{code} - {title}</title>
  <style>
    :root {{
      --bg0: #0f172a; --bg1: #1e293b;
      --accent1: {accent1}; --accent2: {accent2};
      --text: #f1f5f9; --muted: #94a3b8;
      --card-bg: rgba(30, 41, 59, 0.7);
      --card-border-color: rgba(148, 163, 184, 0.1);
      --btn-bg: rgba(255, 255, 255, 0.05);
      --btn-hover: rgba(255, 255, 255, 0.1);
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg0: #f8fafc; --bg1: #e2e8f0;
        --text: #0f172a; --muted: #64748b;
        --card-bg: rgba(255, 255, 255, 0.8);
        --card-border-color: rgba(0, 0, 0, 0.05);
        --btn-bg: rgba(0, 0, 0, 0.05);
        --btn-hover: rgba(0, 0, 0, 0.08);
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; height: 100vh; overflow: hidden;
      font-family: ui-sans-serif, system-ui, sans-serif;
      background: var(--bg0);
      background-image: radial-gradient(circle at 50% -20%, var(--accent1), transparent 70%), linear-gradient(135deg, var(--bg0), var(--bg1));
      color: var(--text);
      display: flex; align-items: center; justify-content: center;
    }}
    .card {{
      background: var(--card-bg); border: 1px solid var(--card-border-color);
      border-radius: 24px; padding: 40px; width: 90%; max-width: 480px;
      text-align: center; backdrop-filter: blur(20px);
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
      animation: float 6s ease-in-out infinite;
    }}
    @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
    .icon {{ 
      width: 64px; height: 64px; margin: 0 auto 24px; display: grid; place-items: center;
      background: linear-gradient(135deg, var(--accent1), var(--accent2));
      border-radius: 20px; color: #fff; box-shadow: 0 10px 20px -5px rgba(0,0,0,0.1);
    }}
    .icon svg {{ width: 32px; height: 32px; }}
    h1 {{ margin: 0 0 16px; font-size: 32px; font-weight: 800; }}
    .code-pill {{ 
      display: inline-block; font-size: 13px; font-weight: 700; padding: 4px 12px;
      border-radius: 99px; background: var(--btn-bg); color: var(--muted); margin-bottom: 16px;
    }}
    .desc {{ color: var(--muted); line-height: 1.6; margin: 0 auto 32px; max-width: 320px; }}
    .actions {{ display: flex; gap: 12px; justify-content: center; }}
    .btn {{
      border: none; background: var(--btn-bg); color: var(--text);
      padding: 12px 20px; border-radius: 12px; font-weight: 600; cursor: pointer;
      text-decoration: none; transition: all 0.2s;
    }}
    .btn:hover {{ background: var(--btn-hover); transform: translateY(-2px); }}
    .btn.primary {{ background: var(--text); color: var(--bg0); }}
    .hidden-data {{ display: none; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="icon">{icon_svg}</div>
    <div class="code-pill">HTTP {code}</div>
    <h1>{title}</h1>
    <p class="desc">{desc}</p>
    <div class="actions">
      <button class="btn primary" onclick="location.reload()">刷新</button>
      <a class="btn" href="./index.html">首页</a>
      <button class="btn" onclick="history.back()">返回</button>
    </div>
  </div>
  <div class="hidden-data">
    <div class="code-pill">HTTP {code}</div>
    <h1>{title}</h1>
    <p class="desc">{desc}</p>
    <div class="icon">{icon_svg}</div>
  </div>
</body>
</html>"""

TEMPLATE_TERMINAL = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{code} - {title}</title>
  <style>
    :root {{
      --bg0: #0f172a; --accent1: {accent1}; --text: #f1f5f9; --muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; height: 100vh; overflow: hidden;
      font-family: 'Fira Code', 'Consolas', monospace;
      background: #020617; color: var(--text);
      display: flex; align-items: center; justify-content: center;
    }}
    .terminal {{
      width: 90%; max-width: 600px;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid #334155; border-radius: 12px;
      box-shadow: 0 0 50px rgba(0,0,0,0.5);
      overflow: hidden;
    }}
    .terminal-header {{
      background: #1e293b; padding: 12px 16px; display: flex; gap: 8px; align-items: center;
    }}
    .dot {{ width: 12px; height: 12px; border-radius: 50%; }}
    .red {{ background: #ef4444; }} .yellow {{ background: #f59e0b; }} .green {{ background: #22c55e; }}
    .terminal-title {{ margin-left: 12px; font-size: 12px; color: #94a3b8; }}
    .terminal-body {{ padding: 24px; font-size: 14px; line-height: 1.6; }}
    .prompt {{ color: #22c55e; margin-right: 8px; }}
    .path {{ color: #38bdf8; margin-right: 8px; }}
    .error-code {{ color: var(--accent1); font-weight: bold; }}
    .cursor {{ display: inline-block; width: 8px; height: 16px; background: var(--text); animation: blink 1s step-end infinite; vertical-align: middle; }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    .actions {{ margin-top: 24px; border-top: 1px solid #334155; padding-top: 16px; }}
    .btn {{
      background: transparent; border: 1px solid #475569; color: var(--text);
      padding: 8px 16px; border-radius: 4px; cursor: pointer; font-family: inherit;
      margin-right: 8px; text-decoration: none; display: inline-block; font-size: 12px;
    }}
    .btn:hover {{ background: #334155; }}
    .hidden-data {{ display: none; }}
  </style>
</head>
<body>
  <div class="terminal">
    <div class="terminal-header">
      <div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div>
      <div class="terminal-title">server_log.txt</div>
    </div>
    <div class="terminal-body">
      <div><span class="prompt">root@server:</span><span class="path">~</span>$ ./handle_request.sh</div>
      <div style="color: #94a3b8; margin: 8px 0;">[INFO] Processing request...</div>
      <div style="color: var(--accent1);">[ERROR] Critical System Failure: <span class="error-code">{code}</span></div>
      <div style="color: var(--accent1);">[MSG] {title}</div>
      <div style="margin-left: 16px; color: #94a3b8;">>> {desc}</div>
      <div style="margin-top: 16px;"><span class="prompt">root@server:</span><span class="path">~</span>$ <span class="cursor"></span></div>
      <div class="actions">
        <button class="btn" onclick="location.reload()">> retry --force</button>
        <a class="btn" href="./index.html">> cd /home</a>
      </div>
    </div>
  </div>
  <div class="hidden-data">
    <div class="code-pill">HTTP {code}</div>
    <h1>{title}</h1>
    <p class="desc">{desc}</p>
    <div class="icon">{icon_svg}</div>
  </div>
</body>
</html>"""

TEMPLATE_SPLIT = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{code} - {title}</title>
  <style>
    :root {{
      --bg: #0f172a; --text: #f8fafc; --accent: {accent1};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; height: 100vh; overflow: hidden;
      font-family: 'Plus Jakarta Sans', sans-serif;
      background: var(--bg); color: var(--text);
      display: flex; align-items: center; justify-content: center;
      background-image: radial-gradient(circle at 80% 20%, rgba(45, 212, 191, 0.1), transparent 40%);
    }}
    .container {{
      display: flex; align-items: center; gap: 60px;
      width: 80%; max-width: 1000px;
    }}
    .big-code {{
      font-size: 180px; font-weight: 900; line-height: 1;
      background: linear-gradient(180deg, #fff, rgba(255,255,255,0.1));
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      opacity: 0.8; letter-spacing: -0.05em;
    }}
    .content {{ flex: 1; }}
    .pill {{
      display: inline-block; padding: 6px 12px; background: rgba(45, 212, 191, 0.1);
      color: var(--accent); border-radius: 99px; font-weight: 600; font-size: 14px; margin-bottom: 24px;
    }}
    h1 {{ font-size: 48px; margin: 0 0 24px; font-weight: 800; line-height: 1.1; }}
    .desc {{ font-size: 18px; color: #94a3b8; line-height: 1.6; margin-bottom: 40px; max-width: 400px; }}
    .btn {{
      display: inline-block; background: var(--text); color: var(--bg);
      padding: 16px 32px; border-radius: 99px; text-decoration: none;
      font-weight: 700; transition: transform 0.2s;
    }}
    .btn:hover {{ transform: translateY(-2px); }}
    @media (max-width: 768px) {{
      .container {{ flex-direction: column; text-align: center; }}
      .big-code {{ font-size: 100px; }}
    }}
    .hidden-data {{ display: none; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="big-code">{code}</div>
    <div class="content">
      <div class="pill">Page Missing</div>
      <h1>{title}</h1>
      <p class="desc">{desc}</p>
      <a href="./index.html" class="btn">返回首页 &rarr;</a>
    </div>
  </div>
  <div class="hidden-data">
    <div class="code-pill">HTTP {code}</div>
    <div class="icon">{icon_svg}</div>
  </div>
</body>
</html>"""

TEMPLATE_SECURITY = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{code} - {title}</title>
  <style>
    :root {{ --accent: {accent1}; --bg: #1e1e2e; }}
    body {{
      margin: 0; height: 100vh; display: flex; align-items: center; justify-content: center;
      background: #11111b; font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      color: #cdd6f4;
    }}
    .badge {{
      background: #1e1e2e; border: 2px solid var(--accent); width: 400px;
      border-radius: 8px; overflow: hidden; position: relative;
      box-shadow: 0 0 40px rgba(192, 132, 252, 0.15);
    }}
    .stripe {{
      height: 24px; background: repeating-linear-gradient(45deg, var(--accent), var(--accent) 10px, #1e1e2e 10px, #1e1e2e 20px);
    }}
    .header {{
      background: var(--accent); color: #11111b; padding: 12px;
      text-align: center; font-weight: 900; letter-spacing: 2px;
    }}
    .body {{ padding: 40px 20px; text-align: center; }}
    .icon-box {{
      width: 80px; height: 80px; border: 2px solid var(--accent);
      border-radius: 50%; display: grid; place-items: center;
      margin: 0 auto 24px; color: var(--accent);
    }}
    .icon-box svg {{ width: 40px; height: 40px; }}
    h1 {{ margin: 0; font-size: 24px; text-transform: uppercase; }}
    .code {{ font-size: 14px; opacity: 0.7; margin: 8px 0 24px; display: block; }}
    .desc {{ font-size: 14px; line-height: 1.5; color: #a6adc8; }}
    .footer {{
      background: #181825; padding: 16px; display: flex; justify-content: space-between;
      border-top: 1px solid #313244; font-size: 12px;
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    .hidden-data {{ display: none; }}
  </style>
</head>
<body>
  <div class="badge">
    <div class="stripe"></div>
    <div class="header">SECURITY ALERT</div>
    <div class="body">
      <div class="icon-box">{icon_svg}</div>
      <h1>ACCESS DENIED</h1>
      <span class="code">ERROR CODE: {code}</span>
      <p class="desc">{desc}</p>
    </div>
    <div class="footer">
      <span>ID: {code}</span>
      <a href="./index.html">[ RETURN HOME ]</a>
    </div>
  </div>
  <div class="hidden-data">
    <div class="code-pill">HTTP {code}</div>
    <h1>{title}</h1>
    <div class="icon">{icon_svg}</div>
  </div>
</body>
</html>"""

# Dashboard Index Template
INDEX_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>错误页导航 (Dashboard)</title>
  <style>
    :root {
      --bg: #f1f5f9;
      --sidebar: #0f172a;
      --card-bg: #ffffff;
      --text: #334155;
      --primary: #3b82f6;
    }
    body {
      margin: 0; min-height: 100vh; background: var(--bg); color: var(--text);
      font-family: ui-sans-serif, system-ui, sans-serif;
      display: flex;
    }
    .sidebar {
      width: 250px; background: var(--sidebar); color: #fff; padding: 24px;
      display: flex; flex-direction: column;
    }
    .brand { font-size: 1.5rem; font-weight: bold; margin-bottom: 40px; color: #fff; }
    .nav-item { padding: 12px; margin-bottom: 8px; border-radius: 8px; background: rgba(255,255,255,0.1); cursor: pointer; }
    .nav-item.active { background: var(--primary); }
    .main { flex: 1; padding: 40px; overflow-y: auto; }
    .header { margin-bottom: 30px; }
    h1 { font-size: 2rem; margin: 0; color: #1e293b; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 24px; }
    .card {
      background: var(--card-bg); border-radius: 12px; padding: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1); transition: all 0.2s;
      text-decoration: none; color: inherit; display: block; border-left: 4px solid var(--primary);
    }
    .card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
    .code { font-size: 1.5rem; font-weight: 700; color: #1e293b; }
    .status { font-size: 0.75rem; padding: 2px 8px; border-radius: 99px; background: #e2e8f0; color: #64748b; font-weight: 600; }
    .card-title { font-weight: 600; margin-bottom: 4px; }
    .card-desc { font-size: 0.875rem; color: #64748b; }
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="brand">System Admin</div>
    <div class="nav-item active">Error Pages</div>
    <div class="nav-item">Logs</div>
    <div class="nav-item">Settings</div>
  </div>
  <div class="main">
    <div class="header">
      <h1>Error Pages Library</h1>
      <p>System response templates for various HTTP status codes.</p>
    </div>
    <div class="grid" id="grid"></div>
  </div>
  <script>
    const pages = [
      { code: '400', title: 'Bad Request', desc: '请求参数或格式错误', type: 'client' },
      { code: '401', title: 'Unauthorized', desc: '访问需要身份验证', type: 'client' },
      { code: '403', title: 'Forbidden', desc: '服务器拒绝执行此请求', type: 'client' },
      { code: '404', title: 'Not Found', desc: '请求的资源不存在', type: 'client' },
      { code: '405', title: 'Method Not Allowed', desc: '请求方法不被允许', type: 'client' },
      { code: '408', title: 'Request Timeout', desc: '服务器等待请求超时', type: 'client' },
      { code: '413', title: 'Payload Too Large', desc: '请求实体过大', type: 'client' },
      { code: '414', title: 'URI Too Long', desc: '请求 URL 长度超限', type: 'client' },
      { code: '429', title: 'Too Many Requests', desc: '请求过于频繁，请稍后', type: 'client' },
      { code: '499', title: 'Client Closed Request', desc: '客户端主动关闭连接', type: 'client' },
      { code: '500', title: 'Internal Server Error', desc: '服务器内部错误', type: 'server' },
      { code: '501', title: 'Not Implemented', desc: '服务器不支持此功能', type: 'server' },
      { code: '502', title: 'Bad Gateway', desc: '网关错误，上游无效', type: 'server' },
      { code: '503', title: 'Service Unavailable', desc: '服务暂时不可用', type: 'server' },
      { code: '504', title: 'Gateway Timeout', desc: '网关请求超时', type: 'server' },
      { code: '505', title: 'HTTP Version Not Supported', desc: 'HTTP 版本不支持', type: 'server' },
      { code: '506', title: 'Variant Also Negotiates', desc: '服务器内部配置错误', type: 'server' },
      { code: '507', title: 'Insufficient Storage', desc: '服务器存储空间不足', type: 'server' },
      { code: '509', title: 'Bandwidth Limit Exceeded', desc: '带宽超出限制', type: 'server' },
      { code: '510', title: 'Not Extended', desc: '获取资源需要更多策略', type: 'server' }
    ];
    const grid = document.getElementById('grid');
    pages.forEach(p => {
        const card = document.createElement('a');
        card.className = 'card';
        card.href = `${p.code}.html`;
        card.innerHTML = `
            <div class="card-header">
                <span class="code">${p.code}</span>
                <span class="status">${p.type.toUpperCase()}</span>
            </div>
            <div class="card-title">${p.title}</div>
            <div class="card-desc">${p.desc}</div>
        `;
        grid.appendChild(card);
    });
  </script>
</body>
</html>"""

def get_content(filepath, filename):
    if not os.path.exists(filepath): return None
    with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
    
    code_match = re.search(r'(?:<div class="code-pill">HTTP\s*|<span class="error-code">|<div class="big-code">|<span class="code">ERROR CODE: )(\d+)', content)
    file_code = filename.split('.')[0]
    code = code_match.group(1) if code_match else file_code

    title_match = re.search(r'<h1>\s*(.*?)\s*</h1>', content)
    if not title_match: title_match = re.search(r'\[MSG\] (.*?)</div>', content) 

    desc_match = re.search(r'<p class="desc">\s*(.*?)\s*</p>', content)
    if not desc_match: desc_match = re.search(r'>> (.*?)</div>', content)

    icon_match = re.search(r'<svg[\s\S]*?</svg>', content)

    return {
        'code': code,
        'title': title_match.group(1) if title_match else 'Error',
        'desc': desc_match.group(1) if desc_match else 'An unknown error occurred.',
        'icon_svg': icon_match.group(0) if icon_match else '<svg viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2z"/></svg>'
    }

def update_index():
    index_path = os.path.join(DIR, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(INDEX_TEMPLATE)
    print("已更新 index.html (仪表盘风格)")

def main():
    for filename in FILES:
        filepath = os.path.join(DIR, filename)
        data = get_content(filepath, filename)
        if data:
            theme = get_theme(data['code'])
            render_data = data.copy()
            render_data.update(theme)
            
            tpl_name = theme.get('template', 'default')
            if tpl_name == 'terminal': template = TEMPLATE_TERMINAL
            elif tpl_name == 'split': template = TEMPLATE_SPLIT
            elif tpl_name == 'security': template = TEMPLATE_SECURITY
            else: template = TEMPLATE_DEFAULT
            
            new_html = template.format(**render_data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"已更新 {filename} (使用 {tpl_name} 模板)")
        else:
            print(f"跳过 {filename} (未找到)")
    update_index()

if __name__ == '__main__':
    main()
