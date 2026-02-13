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

# 颜色配置
THEMES = {
    'default': {'accent1': '#38bdf8', 'accent2': '#818cf8'},
    'server_error': {'accent1': '#f43f5e', 'accent2': '#e11d48'},
    'client_error': {'accent1': '#fbbf24', 'accent2': '#f59e0b'},
    'forbidden': {'accent1': '#c084fc', 'accent2': '#a855f7'},
    'not_found': {'accent1': '#2dd4bf', 'accent2': '#0ea5e9'},
    'timeout': {'accent1': '#f97316', 'accent2': '#ea580c'},
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

# 多彩模板：布局统一，颜色不同
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
      --card-border: rgba(148, 163, 184, 0.1);
      --btn-bg: rgba(255, 255, 255, 0.05);
      --btn-hover: rgba(255, 255, 255, 0.1);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; height: 100vh; overflow: hidden;
      font-family: ui-sans-serif, system-ui, sans-serif;
      background: radial-gradient(circle at 50% -20%, var(--accent1), transparent 70%),
                  radial-gradient(circle at 100% 100%, var(--accent2), transparent 70%),
                  linear-gradient(135deg, var(--bg0), var(--bg1));
      color: var(--text);
      display: flex; align-items: center; justify-content: center;
    }}
    .card {{
      background: var(--card-bg); border: 1px solid var(--card-border);
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
  <!-- Data Preservation -->
  <div class="hidden-data">
    <div class="code-pill">HTTP {code}</div>
    <h1>{title}</h1>
    <p class="desc">{desc}</p>
    <div class="icon">{icon_svg}</div>
  </div>
</body>
</html>"""

# Colorful Index Template
INDEX_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>错误页导航 (多彩版)</title>
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
    }
    .container { max-width: 1200px; margin: 0 auto; padding: 60px 24px; }
    header { margin-bottom: 60px; text-align: center; }
    h1 { font-size: 3rem; font-weight: 800; margin: 0 0 16px; background: linear-gradient(to right, #f43f5e, #fbbf24, #34d399, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 24px; }
    .card {
      background: rgba(30, 41, 59, 0.5); border-radius: 16px; padding: 24px;
      text-decoration: none; color: inherit; transition: all 0.3s; position: relative; overflow: hidden;
      border: 1px solid rgba(255,255,255,0.05);
    }
    .card::before {
      content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: var(--card-color, #ccc);
    }
    .card:hover { transform: translateY(-5px); background: rgba(30, 41, 59, 0.8); box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5); }
    .code { font-size: 2.5rem; font-weight: 800; margin-bottom: 8px; color: var(--card-color); }
    .title { font-size: 1.1rem; font-weight: 600; margin-bottom: 8px; }
    .desc { font-size: 0.9rem; color: var(--text-secondary); line-height: 1.5; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Server Error Pages</h1>
      <p style="color: #94a3b8">Colorful Edition</p>
    </header>
    <div class="grid" id="grid"></div>
  </div>
  <script>
    const pages = [
      { code: '400', title: 'Bad Request', desc: '请求参数或格式错误', color: '#fbbf24' },
      { code: '401', title: 'Unauthorized', desc: '访问需要身份验证', color: '#c084fc' },
      { code: '403', title: 'Forbidden', desc: '服务器拒绝执行此请求', color: '#c084fc' },
      { code: '404', title: 'Not Found', desc: '请求的资源不存在', color: '#2dd4bf' },
      { code: '405', title: 'Method Not Allowed', desc: '请求方法不被允许', color: '#fbbf24' },
      { code: '408', title: 'Request Timeout', desc: '服务器等待请求超时', color: '#f97316' },
      { code: '413', title: 'Payload Too Large', desc: '请求实体过大', color: '#fbbf24' },
      { code: '414', title: 'URI Too Long', desc: '请求 URL 长度超限', color: '#fbbf24' },
      { code: '429', title: 'Too Many Requests', desc: '请求过于频繁，请稍后', color: '#fbbf24' },
      { code: '499', title: 'Client Closed Request', desc: '客户端主动关闭连接', color: '#fbbf24' },
      { code: '500', title: 'Internal Server Error', desc: '服务器内部错误', color: '#f43f5e' },
      { code: '501', title: 'Not Implemented', desc: '服务器不支持此功能', color: '#f43f5e' },
      { code: '502', title: 'Bad Gateway', desc: '网关错误，上游无效', color: '#f97316' },
      { code: '503', title: 'Service Unavailable', desc: '服务暂时不可用', color: '#f43f5e' },
      { code: '504', title: 'Gateway Timeout', desc: '网关请求超时', color: '#f97316' },
      { code: '505', title: 'HTTP Version Not Supported', desc: 'HTTP 版本不支持', color: '#f43f5e' },
      { code: '506', title: 'Variant Also Negotiates', desc: '服务器内部配置错误', color: '#f43f5e' },
      { code: '507', title: 'Insufficient Storage', desc: '服务器存储空间不足', color: '#f43f5e' },
      { code: '509', title: 'Bandwidth Limit Exceeded', desc: '带宽超出限制', color: '#f43f5e' },
      { code: '510', title: 'Not Extended', desc: '获取资源需要更多策略', color: '#f43f5e' }
    ];
    const grid = document.getElementById('grid');
    pages.forEach(p => {
        const card = document.createElement('a');
        card.className = 'card';
        card.href = `${p.code}.html`;
        card.style.setProperty('--card-color', p.color);
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
    print("已更新 index.html (多彩风格)")

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
            print(f"已更新 {filename} (多彩风格)")
        else:
            print(f"跳过 {filename}")
    update_index()

if __name__ == '__main__':
    main()
