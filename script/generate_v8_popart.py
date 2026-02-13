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

# Pop Art / Memphis Style Template
TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{code} - {title}</title>
  <style>
    :root {{
      --yellow: #ffd700;
      --pink: #ff69b4;
      --blue: #00bfff;
      --black: #000000;
      --white: #ffffff;
    }}
    body {{
      margin: 0;
      height: 100vh;
      background-color: var(--yellow);
      background-image: radial-gradient(var(--black) 1px, transparent 1px);
      background-size: 20px 20px;
      font-family: 'Arial Black', 'Impact', sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--black);
    }}
    .card {{
      background: var(--white);
      border: 4px solid var(--black);
      padding: 40px;
      max-width: 500px;
      box-shadow: 10px 10px 0 var(--black);
      position: relative;
      text-align: center;
    }}
    .card::before {{
      content: "";
      position: absolute;
      top: -10px;
      left: -10px;
      width: 100%;
      height: 100%;
      background: var(--pink);
      z-index: -1;
      border: 4px solid var(--black);
    }}
    .code-box {{
      background: var(--blue);
      color: var(--white);
      display: inline-block;
      padding: 10px 20px;
      font-size: 60px;
      border: 4px solid var(--black);
      margin-bottom: 20px;
      transform: rotate(-5deg);
    }}
    h1 {{
      font-size: 32px;
      text-transform: uppercase;
      margin: 10px 0;
      text-decoration: underline;
      text-decoration-thickness: 4px;
      text-decoration-color: var(--pink);
    }}
    p {{
      font-family: 'Arial', sans-serif;
      font-weight: bold;
      font-size: 18px;
      margin-bottom: 30px;
    }}
    .btn {{
      background: var(--black);
      color: var(--white);
      text-decoration: none;
      padding: 15px 30px;
      font-size: 18px;
      display: inline-block;
      border: none;
      cursor: pointer;
      transition: transform 0.1s;
    }}
    .btn:hover {{
      transform: translate(-2px, -2px);
      box-shadow: 4px 4px 0 var(--pink);
    }}
    .btn:active {{
      transform: translate(0, 0);
      box-shadow: none;
    }}
    .icon {{
      display: none; /* Icons don't fit well with this specific raw style unless stylized */
    }}
    .hidden-data {{ display: none; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="code-box">{code}</div>
    <h1>{title}</h1>
    <p>{desc}</p>
    
    <div>
      <a href="javascript:location.reload()" class="btn">RETRY</a>
      <a href="./index.html" class="btn" style="background: var(--white); color: var(--black); border: 4px solid var(--black)">HOME</a>
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

# Pop Art Index
INDEX_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ERROR COLLECTION</title>
  <style>
    :root {
      --bg: #ff69b4;
      --card: #ffffff;
      --border: #000000;
      --shadow: #00bfff;
    }
    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      font-family: 'Arial Black', sans-serif;
      padding: 40px;
    }
    .container { max-width: 1200px; margin: 0 auto; }
    header {
      background: var(--card);
      border: 4px solid var(--border);
      padding: 20px;
      margin-bottom: 40px;
      box-shadow: 8px 8px 0 var(--border);
      text-align: center;
    }
    h1 { margin: 0; font-size: 40px; text-transform: uppercase; letter-spacing: -2px; }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 24px;
    }
    a.card {
      display: block;
      background: var(--card);
      border: 4px solid var(--border);
      padding: 20px;
      text-decoration: none;
      color: var(--border);
      box-shadow: 6px 6px 0 var(--border);
      transition: transform 0.2s;
      position: relative;
    }
    a.card:hover {
      transform: translate(-4px, -4px);
      box-shadow: 10px 10px 0 var(--shadow);
      z-index: 10;
    }
    .code { font-size: 40px; line-height: 1; margin-bottom: 10px; color: var(--border); }
    .title { font-size: 16px; text-transform: uppercase; background: var(--shadow); color: white; padding: 2px 5px; display: inline-block; }
    .desc { font-family: 'Arial', sans-serif; font-size: 14px; margin-top: 10px; font-weight: bold; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Error Page Collection</h1>
      <p style="font-family: Arial; font-weight: bold;">POP ART EDITION</p>
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
    print("已更新 index.html (波普艺术风格)")

def main():
    for filename in FILES:
        filepath = os.path.join(DIR, filename)
        data = get_content(filepath, filename)
        if data:
            new_html = TEMPLATE.format(**data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"已更新 {filename} (波普艺术风格)")
        else:
            print(f"跳过 {filename} (未找到)")
    update_index()

if __name__ == '__main__':
    main()