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

# Swiss Style / International Typographic Style Template
TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{code} - {title}</title>
  <style>
    :root {{
      --bg: #f0f0f0;
      --red: #ff3300;
      --black: #111111;
    }}
    body {{
      margin: 0;
      min-height: 100vh;
      background-color: var(--bg);
      color: var(--black);
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      display: grid;
      grid-template-columns: 1fr 1fr;
      align-items: center;
      overflow: hidden;
    }}
    .left-panel {{
      padding: 60px;
      height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      border-right: 4px solid var(--black);
      background: var(--bg);
    }}
    .right-panel {{
      background-color: var(--red);
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      position: relative;
    }}
    h1 {{
      font-size: 12vw;
      line-height: 0.8;
      margin: 0;
      font-weight: 700;
      letter-spacing: -0.04em;
    }}
    .title-box {{
      margin-top: 40px;
    }}
    h2 {{
      font-size: 2.5rem;
      font-weight: 700;
      margin: 0 0 20px 0;
      text-transform: uppercase;
    }}
    p {{
      font-size: 1.2rem;
      line-height: 1.4;
      max-width: 80%;
      font-weight: 400;
      margin: 0 0 40px 0;
    }}
    .meta {{
      font-weight: 700;
      font-size: 1rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      border-top: 4px solid var(--black);
      padding-top: 20px;
    }}
    .circle {{
      width: 40vw;
      height: 40vw;
      background-color: var(--bg);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .icon svg {{
      width: 20vw;
      height: 20vw;
      fill: var(--black);
    }}
    .btn {{
      display: inline-block;
      background: var(--black);
      color: var(--bg);
      padding: 15px 40px;
      text-decoration: none;
      font-weight: 700;
      font-size: 1rem;
      transition: background 0.3s;
    }}
    .btn:hover {{
      background: var(--red);
      color: var(--bg);
    }}
    
    @media (max-width: 768px) {{
      body {{ grid-template-columns: 1fr; grid-template-rows: auto 1fr; }}
      .left-panel {{ height: auto; padding: 40px; border-right: none; border-bottom: 4px solid var(--black); }}
      .right-panel {{ height: 300px; }}
      .circle {{ width: 200px; height: 200px; }}
      .icon svg {{ width: 100px; height: 100px; }}
      h1 {{ font-size: 20vw; }}
    }}
    .hidden-data {{ display: none; }}
  </style>
</head>
<body>
  <div class="left-panel">
    <div>
      <h1>{code}</h1>
      <div class="title-box">
        <h2>{title}</h2>
        <p>{desc}</p>
        <a href="./index.html" class="btn">RETURN HOME</a>
      </div>
    </div>
    <div class="meta">
      System Status: Critical<br>
      Error Type: HTTP Response
    </div>
  </div>
  <div class="right-panel">
    <div class="circle">
      <div class="icon">{icon_svg}</div>
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

# Swiss Index
INDEX_TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Typographic Gallery</title>
  <style>
    :root {
      --bg: #f0f0f0;
      --red: #ff3300;
      --black: #111111;
    }
    body {
      margin: 0;
      min-height: 100vh;
      background-color: var(--bg);
      color: var(--black);
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      padding: 60px;
    }
    header {
      margin-bottom: 80px;
      border-bottom: 8px solid var(--black);
      padding-bottom: 20px;
    }
    h1 {
      font-size: 5rem;
      font-weight: 700;
      letter-spacing: -0.04em;
      margin: 0;
      line-height: 0.9;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
      gap: 40px;
    }
    .card {
      display: block;
      text-decoration: none;
      color: var(--black);
      border-top: 2px solid var(--black);
      padding-top: 10px;
      transition: all 0.3s;
    }
    .card:hover {
      border-top: 10px solid var(--red);
      transform: translateY(-5px);
    }
    .code {
      font-size: 4rem;
      font-weight: 700;
      line-height: 1;
      margin-bottom: 10px;
      display: block;
    }
    .title {
      font-size: 1.2rem;
      font-weight: 700;
      text-transform: uppercase;
      margin-bottom: 5px;
      display: block;
    }
    .desc {
      font-size: 0.9rem;
      color: #555;
      line-height: 1.4;
    }
  </style>
</head>
<body>
  <header>
    <h1>ERROR<br>PAGES.<br>COLLECTION.</h1>
  </header>
  <div class="grid" id="grid"></div>
  
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
            <span class="code">${p.code}</span>
            <span class="title">${p.title}</span>
            <span class="desc">${p.desc}</span>
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
    print("已更新 index.html (瑞士风格)")

def main():
    for filename in FILES:
        filepath = os.path.join(DIR, filename)
        data = get_content(filepath, filename)
        if data:
            new_html = TEMPLATE.format(**data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"已更新 {filename} (瑞士风格)")
        else:
            print(f"跳过 {filename} (未找到)")
    update_index()

if __name__ == '__main__':
    main()