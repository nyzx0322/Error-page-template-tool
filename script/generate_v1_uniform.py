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

# 统一模板：简约磨砂玻璃
TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{code} - {title}</title>
  <style>
    :root {{
      --bg0: #0f172a; --bg1: #1e293b;
      --accent1: #38bdf8; --accent2: #818cf8; /* 统一使用蓝色系 */
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
      border-radius: 20px; color: #fff; box-shadow: 0 10px 20px -5px rgba(56, 189, 248, 0.4);
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
      text-decoration: none; transition: all 0.2s; display: inline-flex; align-items: center;
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

# 原始 Index 模板 (Uniform)
INDEX_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="robots" content="noindex,nofollow" />
  <title>错误页导航</title>
  <style>
    :root {
      --font-display: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      --bg-dark: #020617;
      --card-bg: rgba(30, 41, 59, 0.4);
      --card-border: rgba(148, 163, 184, 0.1);
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --accent: #38bdf8;
      --accent-glow: rgba(56, 189, 248, 0.2);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0; min-height: 100vh; background: var(--bg-dark); color: var(--text-primary);
      font-family: var(--font-display); overflow-x: hidden;
      background-image: 
        radial-gradient(circle at 15% 50%, rgba(56, 189, 248, 0.08), transparent 25%),
        radial-gradient(circle at 85% 30%, rgba(167, 139, 250, 0.08), transparent 25%);
    }
    body::after {
      content: ""; position: fixed; inset: 0;
      background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
      pointer-events: none; z-index: 999;
    }
    .container { max-width: 1200px; margin: 0 auto; padding: 60px 24px; }
    header { margin-bottom: 60px; text-align: center; position: relative; }
    h1 {
      font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 800; letter-spacing: -0.03em; margin: 0 0 16px 0;
      background: linear-gradient(135deg, #fff 0%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .subtitle { color: var(--text-secondary); font-size: 1.1rem; max-width: 600px; margin: 0 auto; line-height: 1.6; }
    .search-container { margin: 40px auto 0; max-width: 500px; position: relative; }
    .search-input {
      width: 100%; background: rgba(255, 255, 255, 0.03); border: 1px solid var(--card-border);
      padding: 16px 24px; border-radius: 99px; color: white; font-size: 16px; transition: all 0.3s ease; backdrop-filter: blur(10px);
    }
    .search-input:focus { outline: none; border-color: var(--accent); background: rgba(255, 255, 255, 0.05); box-shadow: 0 0 0 4px var(--accent-glow); }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; padding-top: 20px; }
    .card {
      background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 20px; padding: 24px;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden; text-decoration: none;
      display: flex; flex-direction: column; height: 100%;
    }
    .card:hover {
      transform: translateY(-4px); border-color: rgba(255, 255, 255, 0.15); background: rgba(30, 41, 59, 0.6);
      box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.3);
    }
    .card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
    .code { font-size: 2rem; font-weight: 700; color: var(--text-primary); line-height: 1; letter-spacing: -0.02em; }
    .tag { font-size: 12px; padding: 4px 10px; border-radius: 99px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .tag.client { background: rgba(244, 63, 94, 0.1); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.2); }
    .tag.server { background: rgba(168, 85, 247, 0.1); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.2); }
    .card-title { color: var(--text-primary); font-size: 1.1rem; font-weight: 600; margin: 0 0 8px 0; }
    .card-desc { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.5; margin: 0; }
    .card-actions { margin-top: auto; padding-top: 20px; display: flex; gap: 10px; opacity: 0; transform: translateY(10px); transition: all 0.3s ease; }
    .card:hover .card-actions { opacity: 1; transform: translateY(0); }
    .action-btn {
      padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 600; text-decoration: none;
      border: 1px solid rgba(255,255,255,0.1); color: var(--text-primary); background: rgba(255,255,255,0.05); transition: all 0.2s;
    }
    .action-btn:hover { background: rgba(255,255,255,0.1); }
    .empty-state { grid-column: 1 / -1; text-align: center; padding: 60px; color: var(--text-secondary); display: none; }
    @media (max-width: 640px) { .container { padding: 40px 20px; } h1 { font-size: 2rem; } .card-actions { opacity: 1; transform: none; } }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Server Error Pages</h1>
      <p class="subtitle">精心设计的错误页面集合。<br>无滚动条设计，适配所有屏幕尺寸。</p>
      <div class="search-container">
        <input type="text" class="search-input" placeholder="搜索错误码 (e.g. 404, 502)..." id="searchInput">
      </div>
    </header>
    <div class="grid" id="grid"></div>
    <div class="empty-state" id="emptyState"><p>未找到匹配的页面</p></div>
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
    const searchInput = document.getElementById('searchInput');
    const emptyState = document.getElementById('emptyState');
    function renderCards(filterText = '') {
      grid.innerHTML = '';
      const lowerFilter = filterText.toLowerCase();
      const filtered = pages.filter(p => p.code.includes(lowerFilter) || p.title.toLowerCase().includes(lowerFilter) || p.desc.toLowerCase().includes(lowerFilter));
      if (filtered.length === 0) { emptyState.style.display = 'block'; return; }
      emptyState.style.display = 'none';
      filtered.forEach(p => {
        const card = document.createElement('a');
        card.className = 'card';
        card.href = `${p.code}.html`;
        card.innerHTML = `
          <div class="card-header"><span class="code">${p.code}</span><span class="tag ${p.type}">${p.type === 'client' ? 'Client' : 'Server'}</span></div>
          <h3 class="card-title">${p.title}</h3><p class="card-desc">${p.desc}</p>
          <div class="card-actions"><span class="action-btn">查看预览</span><object class="action-btn" onclick="event.preventDefault(); window.open('${p.code}.html')">新窗口打开</object></div>
        `;
        grid.appendChild(card);
      });
    }
    searchInput.addEventListener('input', (e) => renderCards(e.target.value));
    renderCards();
  </script>
</body>
</html>"""

def get_content(filepath, filename):
    if not os.path.exists(filepath): return None
    with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
    
    # 优先从 hidden-data 提取，防止信息丢失
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
    print("已更新 index.html (统一风格)")

def main():
    for filename in FILES:
        filepath = os.path.join(DIR, filename)
        data = get_content(filepath, filename)
        if data:
            new_html = TEMPLATE.format(**data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"已更新 {filename} (统一风格)")
        else:
            print(f"跳过 {filename}")
    update_index()

if __name__ == '__main__':
    main()
