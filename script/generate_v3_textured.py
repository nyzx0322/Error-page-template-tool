import os
import re

# Directory
# 使用相对于脚本文件的路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
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
    'default': {
        'accent1': '#38bdf8', 'accent2': '#818cf8', 
        'pattern': PATTERNS['noise'], 'pattern_size': 'auto', 'animation': 'float', 'card_style': 'default'
    },
    'server_error': {
        'accent1': '#f43f5e', 'accent2': '#e11d48',
        'pattern': PATTERNS['stripes'], 'pattern_size': 'auto', 'animation': 'shake', 'card_style': 'thick'
    },
    'client_error': {
        'accent1': '#fbbf24', 'accent2': '#f59e0b',
        'pattern': PATTERNS['noise'], 'pattern_size': 'auto', 'animation': 'float', 'card_style': 'default'
    },
    'forbidden': {
        'accent1': '#c084fc', 'accent2': '#a855f7',
        'pattern': PATTERNS['grid'], 'pattern_size': '40px 40px', 'animation': 'static', 'card_style': 'solid'
    },
    'not_found': {
        'accent1': '#2dd4bf', 'accent2': '#0ea5e9',
        'pattern': PATTERNS['dots'], 'pattern_size': '30px 30px', 'animation': 'float', 'card_style': 'glass'
    },
    'timeout': {
        'accent1': '#f97316', 'accent2': '#ea580c',
        'pattern': PATTERNS['waves'], 'pattern_size': '60px 60px', 'animation': 'pulse', 'card_style': 'default'
    }
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

# 纹理模板：丰富的背景和动画
TEMPLATE = """<!doctype html>
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
      --pattern: {pattern}; --pattern-size: {pattern_size};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; height: 100vh; overflow: hidden;
      font-family: ui-sans-serif, system-ui, sans-serif;
      background: var(--bg0);
      background-image: radial-gradient(circle at 50% -20%, var(--accent1), transparent 70%), linear-gradient(135deg, var(--bg0), var(--bg1));
      color: var(--text); display: flex; align-items: center; justify-content: center; position: relative;
    }}
    body::before {{
      content: ""; position: absolute; inset: 0;
      background-image: var(--pattern); background-size: var(--pattern-size);
      pointer-events: none; opacity: 0.4;
      mask-image: radial-gradient(circle at center, black 40%, transparent 100%);
      -webkit-mask-image: radial-gradient(circle at center, black 40%, transparent 100%);
    }}
    .card {{
      position: relative; z-index: 10; width: 90%; max-width: 480px; padding: 40px;
      background: var(--card-bg); backdrop-filter: blur(20px); border: 1px solid var(--card-border-color);
      border-radius: 24px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
      text-align: center; animation: {animation} 6s ease-in-out infinite;
    }}
    .card.thick {{ border-top-width: 4px; border-top-color: var(--accent1); }}
    .card.solid {{ border: 2px solid var(--card-border-color); background: var(--bg1); box-shadow: none; }}
    .card.glass {{ background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); }}
    
    @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
    @keyframes shake {{ 0%, 100% {{ transform: translateX(0); }} 10%, 90% {{ transform: translateX(-2px); }} 20%, 80% {{ transform: translateX(2px); }} }}
    @keyframes pulse {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.02); }} }}
    @keyframes static {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY(0); }} }}

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
  <div class="card {card_style}">
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
  <!-- Data Preservation -->
  <div class="hidden-data">
    <div class="code-pill">HTTP {code}</div>
    <h1>{title}</h1>
    <p class="desc">{desc}</p>
    <div class="icon">{icon_svg}</div>
  </div>
</body>
</html>"""

# Textured Index Template
INDEX_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>错误页导航 (纹理版)</title>
  <style>
    :root {
      --bg-dark: #0f172a;
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0; min-height: 100vh; background: var(--bg-dark); color: var(--text-primary);
      font-family: ui-sans-serif, system-ui, sans-serif;
      position: relative;
    }
    body::before {
      content: ""; position: fixed; inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E");
      pointer-events: none; opacity: 0.5; z-index: 0;
    }
    .container { max-width: 1200px; margin: 0 auto; padding: 60px 24px; position: relative; z-index: 10; }
    header { margin-bottom: 60px; text-align: center; }
    h1 { font-size: 3rem; font-weight: 800; margin: 0 0 16px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 24px; }
    .card {
      background: rgba(255, 255, 255, 0.03); border-radius: 16px; padding: 24px;
      text-decoration: none; color: inherit; transition: all 0.3s; position: relative; overflow: hidden;
      border: 1px solid rgba(255,255,255,0.1);
      backdrop-filter: blur(10px);
    }
    .card:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.08); box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5); }
    .code { font-size: 2.5rem; font-weight: 800; margin-bottom: 8px; color: #fff; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }
    .title { font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; }
    .desc { font-size: 0.9rem; color: var(--text-secondary); line-height: 1.5; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Server Error Pages</h1>
      <p style="color: #94a3b8">Textured Edition</p>
    </header>
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
            <div class="code">${p.code}</div>
            <div class="title">${p.title}</div>
            <div class="desc">${p.desc}</div>
        `;
        grid.appendChild(card);
    });
  </script>
</body>
</html>"""

def get_content(filepath, filename):
    if not os.path.exists(filepath): return None
    with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
    
    hidden_match = re.search(r'<div class="hidden-data">([\s\S]*?)</div>', content)
    search_scope = hidden_match.group(1) if hidden_match else content

    code_match = re.search(r'(?:<div class="code-pill">HTTP\s*|<span class="error-code">|<div class="big-code">|<span class="code">ERROR CODE: )(\d+)', search_scope)
    file_code = filename.split('.')[0]
    code = code_match.group(1) if code_match else file_code

    title_match = re.search(r'<h1>\s*(.*?)\s*</h1>', search_scope)
    if not title_match: title_match = re.search(r'\[MSG\] (.*?)</div>', search_scope)
    
    desc_match = re.search(r'<p class="desc">\s*(.*?)\s*</p>', search_scope)
    if not desc_match: desc_match = re.search(r'>> (.*?)</div>', search_scope)

    icon_match = re.search(r'<svg[\s\S]*?</svg>', search_scope)

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
    print("已更新 index.html (纹理风格)")

def main():
    for filename in FILES:
        filepath = os.path.join(DIR, filename)
        data = get_content(filepath, filename)
        if data:
            theme = get_theme(data['code'])
            render_data = data.copy()
            render_data.update(theme)
            new_html = TEMPLATE.format(**render_data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"已更新 {filename} (纹理风格)")
        else:
            print(f"跳过 {filename}")
    update_index()

if __name__ == '__main__':
    main()
