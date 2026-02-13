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

# Blueprint / Engineering Template
TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{code} - {title}</title>
  <style>
    :root {{
      --blue: #0f52ba;
      --white: #ffffff;
      --line: rgba(255, 255, 255, 0.3);
    }}
    body {{
      margin: 0;
      min-height: 100vh;
      background-color: var(--blue);
      color: var(--white);
      font-family: 'Courier New', Courier, monospace;
      background-image: 
        linear-gradient(var(--line) 1px, transparent 1px),
        linear-gradient(90deg, var(--line) 1px, transparent 1px);
      background-size: 40px 40px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .blueprint-container {{
      border: 4px solid var(--white);
      padding: 40px;
      max-width: 600px;
      width: 90%;
      position: relative;
      background: rgba(15, 82, 186, 0.9);
      box-shadow: 10px 10px 0 rgba(0,0,0,0.2);
    }}
    /* Corner marks */
    .blueprint-container::before, .blueprint-container::after {{
      content: "+";
      position: absolute;
      font-size: 30px;
      line-height: 0;
    }}
    .blueprint-container::before {{ top: -5px; left: -9px; }}
    .blueprint-container::after {{ bottom: -5px; right: -9px; }}

    .tech-header {{
      border-bottom: 2px solid var(--white);
      margin-bottom: 30px;
      padding-bottom: 10px;
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      opacity: 0.8;
    }}
    
    .main-content {{
      display: flex;
      align-items: flex-start;
      gap: 30px;
    }}
    
    .drawing {{
      flex-shrink: 0;
      width: 120px;
      height: 120px;
      border: 2px dashed var(--white);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    
    .drawing svg {{
      width: 60px;
      height: 60px;
      fill: none;
      stroke: var(--white);
      stroke-width: 2;
    }}

    .info {{
      flex-grow: 1;
    }}

    h1 {{
      font-size: 3rem;
      margin: 0 0 10px 0;
      font-weight: normal;
      letter-spacing: 2px;
    }}

    h2 {{
      font-size: 1.2rem;
      margin: 0 0 15px 0;
      text-transform: uppercase;
      border-left: 4px solid var(--white);
      padding-left: 15px;
    }}

    p {{
      font-size: 1rem;
      line-height: 1.6;
      opacity: 0.9;
      margin-bottom: 30px;
    }}

    .specs {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      font-size: 0.8rem;
      border-top: 1px dotted var(--white);
      padding-top: 15px;
      margin-bottom: 20px;
    }}
    
    .btn {{
      display: inline-block;
      border: 2px solid var(--white);
      color: var(--white);
      text-decoration: none;
      padding: 10px 20px;
      text-transform: uppercase;
      font-weight: bold;
      transition: background 0.3s;
    }}
    .btn:hover {{
      background: rgba(255,255,255,0.2);
    }}

    @media (max-width: 500px) {{
      .main-content {{ flex-direction: column; align-items: center; text-align: center; }}
      .drawing {{ margin-bottom: 20px; }}
      .tech-header {{ flex-direction: column; gap: 5px; }}
    }}
    .hidden-data {{ display: none; }}
  </style>
</head>
<body>
  <div class="blueprint-container">
    <div class="tech-header">
      <span>PROJECT: WEB_SERVER</span>
      <span>DWG NO: {code}-REV-A</span>
      <span>STATUS: FAILED</span>
    </div>
    
    <div class="main-content">
      <div class="drawing">
        {icon_svg}
      </div>
      <div class="info">
        <h1>{code}</h1>
        <h2>{title}</h2>
        <p>{desc}</p>
        
        <div class="specs">
          <div>MODULE: HTTP_RESPONSE</div>
          <div>PRIORITY: HIGH</div>
          <div>TIMESTAMP: AUTO</div>
          <div>REF: ERROR_LOG</div>
        </div>

        <a href="./index.html" class="btn">RESET SYSTEM</a>
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

# Blueprint Index
INDEX_TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>System Schematics</title>
  <style>
    :root {
      --blue: #0f52ba;
      --white: #ffffff;
      --line: rgba(255, 255, 255, 0.3);
    }
    body {
      margin: 0;
      min-height: 100vh;
      background-color: var(--blue);
      color: var(--white);
      font-family: 'Courier New', monospace;
      background-image: 
        linear-gradient(var(--line) 1px, transparent 1px),
        linear-gradient(90deg, var(--line) 1px, transparent 1px);
      background-size: 40px 40px;
      padding: 40px;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
      border: 4px solid var(--white);
      padding: 40px;
      background: rgba(15, 82, 186, 0.9);
      position: relative;
    }
    header {
      border-bottom: 4px double var(--white);
      padding-bottom: 20px;
      margin-bottom: 40px;
      text-align: center;
    }
    h1 {
      margin: 0;
      text-transform: uppercase;
      letter-spacing: 4px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 20px;
    }
    .card {
      border: 2px solid var(--white);
      padding: 15px;
      text-decoration: none;
      color: var(--white);
      display: block;
      transition: all 0.3s;
    }
    .card:hover {
      background: rgba(255,255,255,0.1);
      box-shadow: 5px 5px 0 rgba(0,0,0,0.2);
    }
    .code {
      font-size: 2rem;
      font-weight: bold;
      display: block;
      border-bottom: 1px dashed var(--white);
      padding-bottom: 5px;
      margin-bottom: 10px;
    }
    .title {
      font-size: 1rem;
      text-transform: uppercase;
      display: block;
      margin-bottom: 5px;
    }
    .desc {
      font-size: 0.8rem;
      opacity: 0.8;
    }
    .footer {
      margin-top: 40px;
      border-top: 1px solid var(--white);
      padding-top: 10px;
      text-align: right;
      font-size: 0.8rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>System Schematics Overview</h1>
      <p>ENGINEERING DEPT. // ERROR PROTOCOLS</p>
    </header>
    <div class="grid" id="grid">
      <!-- GRID_CONTENT -->
    </div>
    <div class="footer">
      APPROVED BY: ADMIN | DATE: AUTO
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
    print("已更新 index.html (蓝图风格)")

def main():
    for filename in FILES:
        filepath = os.path.join(DIR, filename)
        data = get_content(filepath, filename)
        if data:
            new_html = TEMPLATE.format(**data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"已更新 {filename} (蓝图风格)")
        else:
            print(f"跳过 {filename} (未找到)")
    update_index()

if __name__ == '__main__':
    main()
