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

# 赛博朋克风格模板
TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{code} - {title}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    
    :root {{
      --bg: #0b0b0b;
      --primary: #00f3ff; /* 青色 */
      --secondary: #ff003c; /* 红色 */
      --text: #e0e0e0;
      --scan-line: rgba(0, 243, 255, 0.1);
    }}

    body {{
      margin: 0;
      height: 100vh;
      overflow: hidden;
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Orbitron', sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }}

    /* 背景网格 */
    body::before {{
      content: "";
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: 
        linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%),
        linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
      background-size: 100% 2px, 3px 100%;
      z-index: 1;
      pointer-events: none;
    }}

    /* 扫描线效果 */
    .scan-line {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 5px;
      background: var(--scan-line);
      opacity: 0.4;
      animation: scan 6s linear infinite;
      z-index: 2;
      pointer-events: none;
    }}

    @keyframes scan {{
      0% {{ top: -5%; }}
      100% {{ top: 105%; }}
    }}

    .container {{
      position: relative;
      z-index: 10;
      text-align: center;
      padding: 40px;
      border: 2px solid var(--primary);
      box-shadow: 0 0 20px var(--primary), inset 0 0 20px var(--primary);
      background: rgba(0, 0, 0, 0.8);
      max-width: 600px;
      width: 90%;
      clip-path: polygon(
        0 0, 100% 0, 100% 10%, 95% 10%, 95% 15%, 100% 15%, 100% 85%, 
        95% 85%, 95% 90%, 100% 90%, 100% 100%, 0 100%, 0 90%, 5% 90%, 
        5% 85%, 0 85%, 0 15%, 5% 15%, 5% 10%, 0 10%
      );
    }}

    .glitch {{
      font-size: 8rem;
      font-weight: 900;
      color: var(--text);
      position: relative;
      margin: 0;
      text-shadow: 2px 2px var(--secondary), -2px -2px var(--primary);
      animation: glitch-skew 1s infinite linear alternate-reverse;
    }}

    .glitch::before, .glitch::after {{
      content: attr(data-text);
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }}

    .glitch::before {{
      left: 2px;
      text-shadow: -2px 0 var(--secondary);
      clip: rect(44px, 450px, 56px, 0);
      animation: glitch-anim 5s infinite linear alternate-reverse;
    }}

    .glitch::after {{
      left: -2px;
      text-shadow: -2px 0 var(--primary);
      clip: rect(44px, 450px, 56px, 0);
      animation: glitch-anim2 5s infinite linear alternate-reverse;
    }}

    @keyframes glitch-anim {{
      0% {{ clip: rect(31px, 9999px, 91px, 0); }}
      20% {{ clip: rect(8px, 9999px, 95px, 0); }}
      40% {{ clip: rect(56px, 9999px, 63px, 0); }}
      60% {{ clip: rect(2px, 9999px, 84px, 0); }}
      80% {{ clip: rect(72px, 9999px, 17px, 0); }}
      100% {{ clip: rect(96px, 9999px, 45px, 0); }}
    }}

    @keyframes glitch-anim2 {{
      0% {{ clip: rect(66px, 9999px, 78px, 0); }}
      20% {{ clip: rect(12px, 9999px, 3px, 0); }}
      40% {{ clip: rect(89px, 9999px, 56px, 0); }}
      60% {{ clip: rect(23px, 9999px, 12px, 0); }}
      80% {{ clip: rect(45px, 9999px, 67px, 0); }}
      100% {{ clip: rect(34px, 9999px, 98px, 0); }}
    }}

    h1 {{
      font-size: 1.5rem;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--primary);
      margin: 10px 0 20px;
    }}

    p {{
      font-size: 1rem;
      line-height: 1.6;
      color: #aaa;
      margin-bottom: 30px;
    }}

    .btn {{
      display: inline-block;
      padding: 15px 40px;
      background: transparent;
      color: var(--primary);
      border: 2px solid var(--primary);
      font-weight: 700;
      text-decoration: none;
      text-transform: uppercase;
      letter-spacing: 2px;
      transition: all 0.3s;
      position: relative;
      overflow: hidden;
      margin: 0 10px;
    }}

    .btn::before {{
      content: "";
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: var(--primary);
      transition: all 0.3s;
      z-index: -1;
    }}

    .btn:hover {{
      color: #000;
    }}

    .btn:hover::before {{
      left: 0;
    }}

    .btn.secondary {{
      color: var(--secondary);
      border-color: var(--secondary);
    }}

    .btn.secondary::before {{
      background: var(--secondary);
    }}

    .hidden-data {{ display: none; }}
  </style>
</head>
<body>
  <div class="scan-line"></div>
  <div class="container">
    <div class="glitch" data-text="{code}">{code}</div>
    <h1>SYSTEM ERROR: {title}</h1>
    <p>>> {desc}</p>
    <div>
      <a href="javascript:location.reload()" class="btn">RETRY</a>
      <a href="./index.html" class="btn secondary">ABORT</a>
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

INDEX_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>SYSTEM STATUS</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
    :root {
      --bg: #0b0b0b;
      --primary: #00f3ff;
      --secondary: #ff003c;
      --text: #e0e0e0;
      --scan-line: rgba(0, 243, 255, 0.1);
    }
    body {
      margin: 0;
      min-height: 100vh;
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Orbitron', sans-serif;
      overflow-x: hidden;
      background-image: 
        linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%),
        linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
      background-size: 100% 2px, 3px 100%;
    }
    .scan-line {
      position: fixed; top: 0; left: 0; width: 100%; height: 5px;
      background: var(--scan-line); opacity: 0.4; animation: scan 6s linear infinite; pointer-events: none; z-index: 999;
    }
    @keyframes scan { 0% { top: -5%; } 100% { top: 105%; } }
    .container { max-width: 1200px; margin: 0 auto; padding: 60px 24px; }
    header { text-align: center; margin-bottom: 60px; border-bottom: 2px solid var(--primary); padding-bottom: 40px; }
    h1 {
      font-size: 3rem; color: var(--text); text-transform: uppercase; letter-spacing: 4px;
      text-shadow: 2px 2px var(--secondary), -2px -2px var(--primary);
    }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
    .card {
      display: block; text-decoration: none; color: var(--text);
      border: 1px solid var(--primary); padding: 20px; background: rgba(0, 243, 255, 0.05);
      transition: all 0.3s; position: relative; overflow: hidden;
    }
    .card:hover { background: rgba(0, 243, 255, 0.1); transform: translateY(-5px); box-shadow: 0 0 15px var(--primary); }
    .card::before {
      content: ""; position: absolute; top: 0; left: 0; width: 2px; height: 100%; background: var(--primary);
    }
    .code { font-size: 2rem; font-weight: bold; color: var(--primary); display: block; margin-bottom: 10px; }
    .title { font-size: 1.2rem; font-weight: bold; text-transform: uppercase; display: block; margin-bottom: 5px; }
    .desc { font-size: 0.9rem; color: #888; }
    .tag {
        float: right; font-size: 0.8rem; padding: 2px 8px; border: 1px solid var(--secondary); color: var(--secondary);
    }
  </style>
</head>
<body>
  <div class="scan-line"></div>
  <div class="container">
    <header>
      <h1>SYSTEM DIAGNOSTICS</h1>
      <p>ERROR PROTOCOL LIBRARY</p>
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
            <span class="tag">${p.type.toUpperCase()}</span>
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
    
    code_match = re.search(r'(?:<div class="code-pill">HTTP\s*|<span class="error-code">|<div class="big-code">|<span class="code">ERROR CODE: |<div class="code">|<div class="glitch" data-text=")(\d+)', content)
    file_code = filename.split('.')[0]
    code = code_match.group(1) if code_match else file_code

    title_match = re.search(r'<h1>(?:SYSTEM ERROR: )?\s*(.*?)\s*</h1>', content)
    if not title_match: title_match = re.search(r'\[MSG\] (.*?)</div>', content) 
    
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
    print("已更新 index.html (赛博朋克风格)")

def main():
    for filename in FILES:
        filepath = os.path.join(DIR, filename)
        data = get_content(filepath, filename)
        if data:
            new_html = TEMPLATE.format(**data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"已更新 {filename} (赛博朋克风格)")
        else:
            print(f"跳过 {filename} (未找到)")
    update_index()

if __name__ == '__main__':
    main()
