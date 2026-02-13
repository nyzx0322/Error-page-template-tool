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

# Retro / DOS Template
TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{code} - {title}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    
    :root {{
      --bg: #000000;
      --text: #ffb000; /* Amber monochrome */
      --dim: #996600;
      --scanline: rgba(255, 176, 0, 0.1);
    }}

    body {{
      margin: 0;
      height: 100vh;
      background-color: var(--bg);
      color: var(--text);
      font-family: 'VT323', 'Courier New', monospace;
      font-size: 24px;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      text-transform: uppercase;
    }}

    /* CRT Screen Effect */
    body::before {{
      content: " ";
      display: block;
      position: absolute;
      top: 0; left: 0; bottom: 0; right: 0;
      background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
      z-index: 2;
      background-size: 100% 2px, 3px 100%;
      pointer-events: none;
    }}
    
    body::after {{
      content: " ";
      display: block;
      position: absolute;
      top: 0; left: 0; bottom: 0; right: 0;
      background: rgba(18, 16, 16, 0.1);
      opacity: 0;
      z-index: 2;
      pointer-events: none;
      animation: flicker 0.15s infinite;
    }}

    @keyframes flicker {{
      0% {{ opacity: 0.02; }}
      50% {{ opacity: 0.05; }}
      100% {{ opacity: 0.02; }}
    }}

    .terminal {{
      width: 800px;
      max-width: 90%;
      position: relative;
      z-index: 1;
    }}

    .header {{
      border-bottom: 2px solid var(--text);
      margin-bottom: 20px;
      padding-bottom: 10px;
      display: flex;
      justify-content: space-between;
    }}

    .box {{
      border: 2px solid var(--text);
      padding: 20px;
      margin-bottom: 20px;
    }}

    h1 {{
      font-size: 48px;
      margin: 0;
      font-weight: normal;
      text-shadow: 2px 2px var(--dim);
    }}

    .code-display {{
      font-size: 120px;
      line-height: 1;
      margin: 20px 0;
      font-weight: bold;
    }}

    p {{
      line-height: 1.5;
      margin-bottom: 20px;
    }}

    .cursor {{
      display: inline-block;
      width: 12px;
      height: 24px;
      background: var(--text);
      animation: blink 1s step-end infinite;
      vertical-align: bottom;
    }}

    @keyframes blink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0; }}
    }}

    a {{
      color: var(--bg);
      background: var(--text);
      text-decoration: none;
      padding: 5px 15px;
      display: inline-block;
      margin-right: 15px;
    }}

    a:hover {{
      background: var(--dim);
      color: var(--text);
    }}

    .hidden-data {{ display: none; }}
  </style>
</head>
<body>
  <div class="terminal">
    <div class="header">
      <span>SERVER_OS [VERSION 1.0]</span>
      <span>MEM: 640K OK</span>
    </div>
    
    <div class="box">
      <p>A fatal exception {code} has occurred at {title}.</p>
      <p>The current application will be terminated.</p>
      
      <div class="code-display">ERROR {code}</div>
      
      <p>>> {desc}</p>
      <p>>> SYSTEM HALTED.</p>
    </div>

    <div>
      <p>C:\Users\Admin> WHAT TO DO NEXT?</p>
      <p>
        <a href="javascript:location.reload()">[ RETRY ]</a>
        <a href="./index.html">[ ABORT ]</a>
        <span class="cursor"></span>
      </p>
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

# DOS Directory Style Index
INDEX_TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>DIR /W</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    :root {
      --bg: #000000;
      --text: #ffb000;
    }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'VT323', monospace;
      font-size: 20px;
      padding: 40px;
      margin: 0;
      height: 100vh;
      overflow: hidden;
    }
    .container {
      max-width: 1000px;
      margin: 0 auto;
    }
    h1 { font-size: 24px; font-weight: normal; margin-bottom: 20px; }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 10px;
    }
    a {
      display: block;
      color: var(--text);
      text-decoration: none;
      padding: 5px;
    }
    a:hover {
      background: var(--text);
      color: var(--bg);
    }
    .code { display: inline-block; width: 50px; }
    .title { text-transform: uppercase; }
    .footer { margin-top: 30px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>
      Volume in drive C is WEBSERVER<br>
      Directory of C:\ERRORS
    </h1>
    
    <div class="grid" id="grid"></div>
    
    <div class="footer">
      <span id="fileCount">0</span> File(s)<br>
      0 Dir(s)   640,000 bytes free
      <br><br>
      C:\ERRORS>_
    </div>
  </div>
  <script>
    const pages = [
      { code: '400', title: 'Bad Request' },
      { code: '401', title: 'Unauthorized' },
      { code: '403', title: 'Forbidden' },
      { code: '404', title: 'Not Found' },
      { code: '405', title: 'Method Not Allowed' },
      { code: '408', title: 'Request Timeout' },
      { code: '413', title: 'Payload Too Large' },
      { code: '414', title: 'URI Too Long' },
      { code: '429', title: 'Too Many Requests' },
      { code: '499', title: 'Client Closed Request' },
      { code: '500', title: 'Internal Server Error' },
      { code: '501', title: 'Not Implemented' },
      { code: '502', title: 'Bad Gateway' },
      { code: '503', title: 'Service Unavailable' },
      { code: '504', title: 'Gateway Timeout' },
      { code: '505', title: 'HTTP Version Not Supported' },
      { code: '506', title: 'Variant Also Negotiates' },
      { code: '507', title: 'Insufficient Storage' },
      { code: '509', title: 'Bandwidth Limit Exceeded' },
      { code: '510', title: 'Not Extended' }
    ];
    const grid = document.getElementById('grid');
    document.getElementById('fileCount').innerText = pages.length;
    
    pages.forEach(p => {
        const link = document.createElement('a');
        link.href = `${p.code}.html`;
        // Pad title to align somewhat like a DOS directory
        let title = p.title.length > 15 ? p.title.substring(0, 12) + '...' : p.title;
        link.innerHTML = `<span class="code">${p.code}</span> <span class="ext">HTML</span> <span class="title">${title}</span>`;
        grid.appendChild(link);
    });
  </script>
</body>
</html>"""

def get_content(filepath, filename):
    if not os.path.exists(filepath): return None
    with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
    
    code_match = re.search(r'(?:<div class="code-pill">HTTP\s*|<span class="error-code">|<div class="big-code">|<span class="code">ERROR CODE: |<div class="code">|<div class="code-display">ERROR |<div class="glitch" data-text=")(\d+)', content)
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
    print("已更新 index.html (复古风格)")

def main():
    for filename in FILES:
        filepath = os.path.join(DIR, filename)
        data = get_content(filepath, filename)
        if data:
            new_html = TEMPLATE.format(**data)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"已更新 {filename} (复古风格)")
        else:
            print(f"跳过 {filename} (未找到)")
    update_index()

if __name__ == '__main__':
    main()