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

# Neumorphism / Soft UI Template
TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{code} - {title}</title>
  <style>
    :root {{
      --bg: #e0e5ec;
      --text: #4a5568;
      --shadow-light: #ffffff;
      --shadow-dark: #a3b1c6;
    }}
    body {{
      margin: 0;
      min-height: 100vh;
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .card {{
      width: 400px;
      max-width: 90%;
      padding: 50px 40px;
      border-radius: 30px;
      background: var(--bg);
      box-shadow: 20px 20px 60px var(--shadow-dark),
                  -20px -20px 60px var(--shadow-light);
      text-align: center;
    }}
    .icon-circle {{
      width: 100px;
      height: 100px;
      margin: 0 auto 30px;
      border-radius: 50%;
      background: var(--bg);
      box-shadow: inset 6px 6px 12px var(--shadow-dark),
                  inset -6px -6px 12px var(--shadow-light);
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .icon-circle svg {{
      width: 50px;
      height: 50px;
      fill: var(--text);
    }}
    h1 {{
      font-size: 4rem;
      margin: 0;
      color: var(--text);
      text-shadow: 2px 2px 4px var(--shadow-dark), -2px -2px 4px var(--shadow-light);
    }}
    h2 {{
      font-size: 1.5rem;
      font-weight: 600;
      margin: 10px 0 20px;
    }}
    p {{
      color: #718096;
      margin-bottom: 40px;
      line-height: 1.6;
    }}
    .btn {{
      display: inline-block;
      text-decoration: none;
      color: var(--text);
      font-weight: 600;
      padding: 15px 40px;
      border-radius: 50px;
      background: var(--bg);
      box-shadow: 6px 6px 12px var(--shadow-dark),
                  -6px -6px 12px var(--shadow-light);
      transition: all 0.2s ease;
    }}
    .btn:hover {{
      transform: translateY(-2px);
    }}
    .btn:active {{
      transform: translateY(1px);
      box-shadow: inset 4px 4px 8px var(--shadow-dark),
                  inset -4px -4px 8px var(--shadow-light);
    }}
    .hidden-data {{ display: none; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="icon-circle">
      {icon_svg}
    </div>
    <h1>{code}</h1>
    <h2>{title}</h2>
    <p>{desc}</p>
    <a href="./index.html" class="btn">返回首页</a>
  </div>

  <div class="hidden-data">
    <div class="code-pill">HTTP {code}</div>
    <h1>{title}</h1>
    <p class="desc">{desc}</p>
    <div class="icon">{icon_svg}</div>
  </div>
</body>
</html>"""

# Neumorphism Index
INDEX_TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Soft UI Dashboard</title>
  <style>
    :root {
      --bg: #e0e5ec;
      --text: #4a5568;
      --shadow-light: #ffffff;
      --shadow-dark: #a3b1c6;
    }
    body {
      margin: 0;
      min-height: 100vh;
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, sans-serif;
      padding: 40px;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
    }
    header {
      text-align: center;
      margin-bottom: 60px;
    }
    h1 {
      font-size: 2.5rem;
      margin-bottom: 10px;
      color: var(--text);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 30px;
    }
    a.card {
      display: flex;
      flex-direction: column;
      text-decoration: none;
      color: var(--text);
      padding: 30px;
      border-radius: 20px;
      background: var(--bg);
      box-shadow: 9px 9px 16px var(--shadow-dark),
                  -9px -9px 16px var(--shadow-light);
      transition: all 0.3s ease;
    }
    a.card:hover {
      transform: translateY(-5px);
      box-shadow: 12px 12px 20px var(--shadow-dark),
                  -12px -12px 20px var(--shadow-light);
    }
    a.card:active {
      box-shadow: inset 6px 6px 12px var(--shadow-dark),
                  inset -6px -6px 12px var(--shadow-light);
    }
    .code {
      font-size: 2rem;
      font-weight: 700;
      color: var(--text);
      margin-bottom: 5px;
    }
    .title {
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 10px;
    }
    .desc {
      font-size: 0.9rem;
      color: #718096;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>System Status</h1>
      <p>Neumorphism Design System</p>
    </header>
    <div class="grid" id="grid"></div>
  </div>
  <script>
    const pages = [
      { code: '400', title: 'Bad Request', desc: '请求参数或格式错误' },
      { code: '401', title: 'Unauthorized', desc: '访问需要身份验证' },
      { code: '403', title: 'Forbidden', desc: '服务器拒绝执行此请求' },
      { code: '404', title: 'Not Found', desc: '请求的资源不存在' },
      { code: '405', title: 'Method Not Allowed', desc: '请求方法不被允许' },
      { code: '408', title: 'Request Timeout', desc: '服务器等待请求超时' },
      { code: '413', title: 'Payload Too Large', desc: '请求实体过大' },
      { code: '414', title: 'URI Too Long', desc: '请求 URL 长度超限' },
      { code: '429', title: 'Too Many Requests', desc: '请求过于频繁，请稍后' },
      { code: '499', title: 'Client Closed Request', desc: '客户端主动关闭连接' },
      { code: '500', title: 'Internal Server Error', desc: '服务器内部错误' },
      { code: '501', title: 'Not Implemented', desc: '服务器不支持此功能' },
      { code: '502', title: 'Bad Gateway', desc: '网关错误，上游无效' },
      { code: '503', title: 'Service Unavailable', desc: '服务暂时不可用' },
      { code: '504', title: 'Gateway Timeout', desc: '网关请求超时' },
      { code: '505', title: 'HTTP Version Not Supported', desc: 'HTTP 版本不支持' },
      { code: '506', title: 'Variant Also Negotiates', desc: '服务器内部配置错误' },
      { code: '507', title: 'Insufficient Storage', desc: '服务器存储空间不足' },
      { code: '509', title: 'Bandwidth Limit Exceeded', desc: '带宽超出限制' },
      { code: '510', title: 'Not Extended', desc: '获取资源需要更多策略' }
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
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(INDEX_TEMPLATE)
    print("已更新 index.html (新拟态风格)")

def main():
    for filename in FILES:
        filepath = os.path.join(DIR, filename)
        data = get_content(filepath, filename)
        if data:
            new_html = TEMPLATE.format(**data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"已更新 {filename} (新拟态风格)")
        else:
            print(f"跳过 {filename} (未找到)")
    update_index()

if __name__ == '__main__':
    main()