import os
import re

# Directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.dirname(SCRIPT_DIR)

FILES = [
    '400.html', '401.html', '403.html', '404.html', '405.html', 
    '408.html', '413.html', '414.html', '429.html', '499.html',
    '500.html', '501.html', '502.html', '503.html', '504.html', 
    '505.html', '506.html', '507.html', '509.html', '510.html'
]

PAGES_DATA = [
    {'code': '400', 'title': 'Bad Request', 'desc': '请求参数或格式错误'},
    {'code': '401', 'title': 'Unauthorized', 'desc': '访问需要身份验证'},
    {'code': '403', 'title': 'Forbidden', 'desc': '服务器拒绝执行此请求'},
    {'code': '404', 'title': 'Not Found', 'desc': '请求的资源不存在'},
    {'code': '405', 'title': 'Method Not Allowed', 'desc': '请求方法不被允许'},
    {'code': '408', 'title': 'Request Timeout', 'desc': '服务器等待请求超时'},
    {'code': '413', 'title': 'Payload Too Large', 'desc': '请求实体过大'},
    {'code': '414', 'title': 'URI Too Long', 'desc': '请求 URL 长度超限'},
    {'code': '429', 'title': 'Too Many Requests', 'desc': '请求过于频繁，请稍后'},
    {'code': '499', 'title': 'Client Closed Request', 'desc': '客户端主动关闭连接'},
    {'code': '500', 'title': 'Internal Server Error', 'desc': '服务器内部错误'},
    {'code': '501', 'title': 'Not Implemented', 'desc': '服务器不支持此功能'},
    {'code': '502', 'title': 'Bad Gateway', 'desc': '网关错误，上游无效'},
    {'code': '503', 'title': 'Service Unavailable', 'desc': '服务暂时不可用'},
    {'code': '504', 'title': 'Gateway Timeout', 'desc': '网关请求超时'},
    {'code': '505', 'title': 'HTTP Version Not Supported', 'desc': 'HTTP 版本不支持'},
    {'code': '506', 'title': 'Variant Also Negotiates', 'desc': '服务器内部配置错误'},
    {'code': '507', 'title': 'Insufficient Storage', 'desc': '服务器存储空间不足'},
    {'code': '509', 'title': 'Bandwidth Limit Exceeded', 'desc': '带宽超出限制'},
    {'code': '510', 'title': 'Not Extended', 'desc': '获取资源需要更多策略'}
]

# Zen / Nature Style Template
TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{code} - {title}</title>
  <style>
    :root {{
      --bg: #fdfcf5;
      --text: #5d5c56;
      --accent: #8a9a5b; /* Moss green */
      --circle: #e6e4d8;
    }}
    body {{
      margin: 0;
      min-height: 100vh;
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Georgia', 'Times New Roman', serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      text-align: center;
    }}
    
    /* Breathing animation background */
    .bg-circle {{
      position: absolute;
      width: 600px;
      height: 600px;
      background: var(--circle);
      border-radius: 50%;
      z-index: -1;
      animation: breathe 8s ease-in-out infinite;
      opacity: 0.6;
    }}
    
    @keyframes breathe {{
      0%, 100% {{ transform: scale(1); opacity: 0.6; }}
      50% {{ transform: scale(1.1); opacity: 0.4; }}
    }}

    .content {{
      padding: 40px;
      max-width: 600px;
      position: relative;
    }}

    .icon-box {{
      margin-bottom: 30px;
    }}
    
    .icon-box svg {{
      width: 80px;
      height: 80px;
      fill: var(--accent);
      opacity: 0.8;
    }}

    h1 {{
      font-size: 5rem;
      font-weight: normal;
      margin: 0;
      color: var(--accent);
      font-style: italic;
    }}

    h2 {{
      font-size: 1.5rem;
      font-weight: normal;
      margin: 10px 0 30px;
      letter-spacing: 2px;
      text-transform: uppercase;
      font-size: 0.9rem;
    }}

    p {{
      font-size: 1.2rem;
      line-height: 1.8;
      margin-bottom: 50px;
      color: #7d7c76;
    }}

    .btn {{
      display: inline-block;
      border: 1px solid var(--text);
      color: var(--text);
      text-decoration: none;
      padding: 12px 30px;
      border-radius: 50px;
      transition: all 0.4s ease;
      font-size: 0.9rem;
      letter-spacing: 1px;
    }}

    .btn:hover {{
      background: var(--text);
      color: var(--bg);
      border-color: var(--text);
    }}

    .hidden-data {{ display: none; }}
  </style>
</head>
<body>
  <div class="bg-circle"></div>
  
  <div class="content">
    <div class="icon-box">
      {icon_svg}
    </div>
    <h1>{code}</h1>
    <h2>{title}</h2>
    <p>
      The path you seek cannot be found.<br>
      Take a breath. Return to the center.<br>
      {desc}
    </p>
    <a href="./index.html" class="btn">Return Home</a>
  </div>

  <div class="hidden-data">
    <div class="code-pill">HTTP {code}</div>
    <h1>{title}</h1>
    <p class="desc">{desc}</p>
    <div class="icon">{icon_svg}</div>
  </div>
</body>
</html>"""

# Zen Index
INDEX_TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Peaceful Collection</title>
  <style>
    :root {
      --bg: #fdfcf5;
      --text: #5d5c56;
      --accent: #8a9a5b;
      --card-bg: #ffffff;
    }
    body {
      margin: 0;
      min-height: 100vh;
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Georgia', serif;
      padding: 60px 20px;
    }
    .container {
      max-width: 1000px;
      margin: 0 auto;
    }
    header {
      text-align: center;
      margin-bottom: 80px;
    }
    h1 {
      font-size: 2.5rem;
      font-weight: normal;
      color: var(--accent);
      margin-bottom: 10px;
      font-style: italic;
    }
    p.subtitle {
      color: #999;
      font-size: 0.9rem;
      letter-spacing: 2px;
      text-transform: uppercase;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 40px;
    }
    a.card {
      display: block;
      text-decoration: none;
      color: var(--text);
      text-align: center;
      transition: opacity 0.3s;
    }
    a.card:hover {
      opacity: 0.6;
    }
    .code {
      font-size: 2.5rem;
      color: var(--accent);
      display: block;
      margin-bottom: 10px;
    }
    .title {
      font-size: 0.9rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      display: block;
      margin-bottom: 5px;
    }
    .desc {
      font-size: 0.8rem;
      color: #999;
      font-style: italic;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>State of Being</h1>
      <p class="subtitle">Error Pages Collection</p>
    </header>
    <div class="grid" id="grid">
      <!-- GRID_CONTENT -->
    </div>
  </div>
</body>
</html>"""

def get_content(filepath, filename):
    if not os.path.exists(filepath): return None
    with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
    
    code_match = re.search(r'(?:<div class="code-pill">HTTP\s*|<span class="error-code">|<div class="big-code">|<span class="code">ERROR CODE: |<div class="code">|<div class="code-display">ERROR |<div class="code-box">|<div class="glitch" data-text=")(\d+)', content)
    file_code = filename.split('.')[0]
    code = code_match.group(1) if code_match else file_code

    title_match = re.search(r'<h1>(?:SYSTEM ERROR: )?\s*(.*?)\s*</h1>', content)
    if not title_match: title_match = re.search(r'\[MSG\] (.*?)</div>', content) 
    if not title_match: title_match = re.search(r'Exception .*? has occurred at (.*?)\.</p>', content)
    if not title_match: title_match = re.search(r'<h2>(.*?)</h2>', content)
    
    desc_match = re.search(r'<p(?: class="desc")?>\s*(?:>> )?(.*?)\s*</p>', content)
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
    
    # Generate Grid HTML
    grid_html = ""
    for p in PAGES_DATA:
        card = f"""
        <a href="{p['code']}.html" class="card">
            <span class="code">{p['code']}</span>
            <span class="title">{p['title']}</span>
            <span class="desc">{p['desc']}</span>
        </a>
        """
        grid_html += card

    final_html = INDEX_TEMPLATE.replace('<!-- GRID_CONTENT -->', grid_html)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print("已更新 index.html (禅意风格)")

def main():
    for filename in FILES:
        filepath = os.path.join(DIR, filename)
        data = get_content(filepath, filename)
        if data:
            new_html = TEMPLATE.format(**data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"已更新 {filename} (禅意风格)")
        else:
            print(f"跳过 {filename} (未找到)")
    update_index()

if __name__ == '__main__':
    main()
