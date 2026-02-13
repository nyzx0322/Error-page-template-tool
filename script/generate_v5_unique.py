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

# Unique Styles Configuration
# Each key defines the CSS variables and specific styles for that error code
STYLES = {
    '400': { # Minimalist Black & White
        'css': """
            :root { --bg: #ffffff; --text: #000000; --accent: #000000; }
            body { font-family: 'Times New Roman', serif; border: 20px solid #000; box-sizing: border-box; }
            h1 { font-size: 15vw; line-height: 0.8; letter-spacing: -0.05em; margin: 0; }
            h2 { font-style: italic; font-weight: 400; border-bottom: 2px solid #000; display: inline-block; }
            .container { text-align: center; }
        """,
        'card_css': "background: #fff; color: #000; border: 4px solid #000; font-family: 'Times New Roman';"
    },
    '401': { # Security / Matrix
        'css': """
            :root { --bg: #000000; --text: #00ff00; --accent: #00ff00; }
            body { font-family: 'Courier New', monospace; background-image: linear-gradient(rgba(0,255,0,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,0,0.03) 1px, transparent 1px); background-size: 20px 20px; }
            h1 { text-shadow: 0 0 10px #00ff00; font-size: 8rem; margin: 0; }
            .container { border: 1px solid #00ff00; padding: 40px; box-shadow: 0 0 20px rgba(0,255,0,0.2); max-width: 600px; }
            .btn { border: 1px solid #00ff00; color: #00ff00; }
            .btn:hover { background: #00ff00; color: #000; }
        """,
        'card_css': "background: #000; color: #00ff00; border: 1px solid #00ff00; font-family: monospace;"
    },
    '403': { # Red Alert
        'css': """
            :root { --bg: #1a0000; --text: #ff0000; --accent: #ff0000; }
            body { font-family: 'Impact', sans-serif; background: repeating-linear-gradient(45deg, #1a0000, #1a0000 10px, #2a0000 10px, #2a0000 20px); }
            h1 { font-size: 10rem; color: #ff0000; text-transform: uppercase; letter-spacing: 10px; margin: 0; text-shadow: 2px 2px 0 #000; }
            .container { background: #000; padding: 50px; border: 4px solid #ff0000; transform: rotate(-2deg); }
            h2 { background: #ff0000; color: #000; padding: 5px 20px; display: inline-block; }
        """,
        'card_css': "background: #1a0000; color: #ff0000; border: 2px solid #ff0000; font-family: 'Impact';"
    },
    '404': { # Space / Void
        'css': """
            :root { --bg: #0b0d17; --text: #d0d6f9; --accent: #ffffff; }
            body { font-family: system-ui; background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%); }
            h1 { font-size: 12rem; background: -webkit-linear-gradient(#eee, #333); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }
            .container { animation: float 6s ease-in-out infinite; }
            @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }
            .btn { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); }
        """,
        'card_css': "background: #0b0d17; color: #d0d6f9; background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);"
    },
    '405': { # Traffic / Warning
        'css': """
            :root { --bg: #f7d716; --text: #000000; --accent: #000000; }
            body { font-family: 'Arial Black', sans-serif; text-transform: uppercase; }
            h1 { font-size: 8rem; border: 10px solid #000; padding: 20px 40px; border-radius: 20px; background: #000; color: #f7d716; margin-bottom: 20px; }
            h2 { font-size: 2rem; border-bottom: 5px solid #000; }
            .btn { background: #000; color: #f7d716; border-radius: 0; font-weight: 900; }
        """,
        'card_css': "background: #f7d716; color: #000; font-family: 'Arial Black'; border: 2px solid #000;"
    },
    '408': { # Time / Blur
        'css': """
            :root { --bg: #e6e2d3; --text: #5c5546; --accent: #8b8066; }
            body { font-family: 'Georgia', serif; }
            h1 { font-size: 10rem; color: rgba(92, 85, 70, 0.2); position: absolute; z-index: -1; filter: blur(2px); }
            h2 { font-size: 2.5rem; letter-spacing: 5px; }
            .container { backdrop-filter: blur(5px); padding: 40px; border: 1px solid rgba(92, 85, 70, 0.2); }
            p { font-style: italic; }
        """,
        'card_css': "background: #e6e2d3; color: #5c5546; font-family: 'Georgia';"
    },
    '413': { # Industrial / Heavy
        'css': """
            :root { --bg: #2d3436; --text: #dfe6e9; --accent: #fab1a0; }
            body { font-family: 'Impact', sans-serif; background: repeating-linear-gradient(45deg, #2d3436, #2d3436 10px, #353b48 10px, #353b48 20px); }
            .container { background: #636e72; padding: 40px; border: 4px solid #2d3436; box-shadow: 10px 10px 0 #000; max-width: 500px; }
            h1 { font-size: 6rem; line-height: 1; margin: 0; color: #fab1a0; }
            h2 { background: #2d3436; color: #fff; padding: 10px; display: inline-block; }
            .btn { background: #fab1a0; color: #2d3436; font-weight: bold; border: none; box-shadow: 4px 4px 0 #000; }
        """,
        'card_css': "background: #636e72; color: #dfe6e9; border: 2px solid #2d3436;"
    },
    '414': { # Receipt / Long
        'css': """
            :root { --bg: #ddd; --text: #333; --accent: #000; }
            body { font-family: 'Courier New', monospace; background: #ccc; }
            .container { background: #fff; padding: 40px; width: 300px; margin: 50px auto; box-shadow: 0 5px 15px rgba(0,0,0,0.1); position: relative; }
            .container::before { content: ''; position: absolute; top: -5px; left: 0; width: 100%; height: 10px; background: radial-gradient(circle, #fff 5px, transparent 6px); background-size: 15px 15px; }
            .container::after { content: ''; position: absolute; bottom: -5px; left: 0; width: 100%; height: 10px; background: radial-gradient(circle, #fff 5px, transparent 6px); background-size: 15px 15px; }
            h1 { border-bottom: 2px dashed #000; padding-bottom: 20px; margin-bottom: 20px; font-size: 3rem; text-align: center; }
            p { text-align: justify; font-size: 0.9rem; }
            .btn { display: block; text-align: center; border: 1px solid #000; margin-top: 30px; color: #000; }
        """,
        'card_css': "background: #fff; color: #333; font-family: 'Courier New'; border-top: 2px dashed #333; border-bottom: 2px dashed #333;"
    },
    '429': { # Busy / Pattern
        'css': """
            :root { --bg: #6c5ce7; --text: #fff; --accent: #a29bfe; }
            body { font-family: sans-serif; background-color: #6c5ce7; background-image: radial-gradient(#a29bfe 2px, transparent 2px); background-size: 20px 20px; }
            h1 { font-size: 8rem; font-weight: 900; letter-spacing: -5px; margin: 0; color: #fff; text-shadow: 4px 4px 0 #000; }
            .container { background: #fff; color: #6c5ce7; padding: 40px; border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.2); max-width: 400px; }
            h2 { font-weight: 900; }
            .btn { background: #6c5ce7; color: #fff; border-radius: 10px; }
        """,
        'card_css': "background: #6c5ce7; color: #fff; background-image: radial-gradient(#a29bfe 2px, transparent 2px); background-size: 10px 10px;"
    },
    '499': { # Disconnected / Static
        'css': """
            :root { --bg: #222; --text: #fff; --accent: #777; }
            body { font-family: 'Consolas', monospace; background: #111; display: flex; align-items: center; justify-content: center; }
            h1 { font-size: 6rem; color: #444; margin: 0; position: relative; }
            h1::after { content: '499'; position: absolute; left: 2px; top: 0; color: #fff; clip-path: polygon(0 0, 100% 0, 100% 45%, 0 45%); transform: translate(-2px, 0); }
            h2 { border-left: 3px solid #fff; padding-left: 15px; color: #aaa; }
            .container { position: relative; z-index: 10; }
            .static-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.05; background: repeating-radial-gradient(#fff 0 0.0001%, #000 0 0.0002%); z-index: 1; pointer-events: none; }
        """,
        'card_css': "background: #222; color: #fff; font-family: 'Consolas';"
    },
    '500': { # BSOD
        'css': """
            :root { --bg: #0000AA; --text: #fff; --accent: #fff; }
            body { font-family: 'Lucida Console', monospace; background: #0000AA; color: #fff; align-items: flex-start; padding: 50px; text-align: left; }
            h1 { background: #fff; color: #0000AA; display: inline-block; padding: 0 10px; font-size: 2rem; margin-bottom: 30px; }
            h2 { font-size: 1.2rem; margin-bottom: 20px; font-weight: normal; }
            p { font-size: 1rem; line-height: 1.5; max-width: 800px; }
            .container { width: 100%; }
            .btn { border: 1px solid #fff; color: #fff; margin-top: 40px; display: inline-block; }
            .btn:hover { background: #fff; color: #0000AA; }
        """,
        'card_css': "background: #0000AA; color: #fff; font-family: 'Lucida Console'; text-align: left;"
    },
    '501': { # Blueprint Sketch
        'css': """
            :root { --bg: #34495e; --text: #ecf0f1; --accent: #f1c40f; }
            body { font-family: 'Segoe UI', sans-serif; background: #34495e; background-image: linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px); background-size: 50px 50px; }
            h1 { font-size: 6rem; font-weight: 300; border: 4px solid #ecf0f1; display: inline-block; padding: 20px 40px; border-radius: 10px; }
            h2 { color: #f1c40f; text-transform: uppercase; letter-spacing: 2px; }
            .container { text-align: center; }
            .icon svg { stroke: #ecf0f1; stroke-width: 2; fill: none; width: 80px; height: 80px; }
            .btn { background: #f1c40f; color: #34495e; font-weight: bold; border-radius: 5px; }
        """,
        'card_css': "background: #34495e; color: #ecf0f1; border: 1px dashed #ecf0f1;"
    },
    '502': { # Broken Link
        'css': """
            :root { --bg: #f8f9fa; --text: #212529; --accent: #dee2e6; }
            body { font-family: 'Verdana', sans-serif; background: #f8f9fa; }
            .container { background: #fff; padding: 60px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border-top: 5px solid #dc3545; }
            h1 { font-size: 4rem; color: #dc3545; margin: 0 0 20px; }
            .icon { background: #f8f9fa; width: 100px; height: 100px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 30px; }
            .icon svg { fill: #dc3545; width: 50px; height: 50px; }
            .btn { background: #343a40; color: #fff; border-radius: 4px; }
        """,
        'card_css': "background: #fff; color: #212529; border-top: 4px solid #dc3545;"
    },
    '503': { # Sleeping / Night
        'css': """
            :root { --bg: #2c2c54; --text: #dcdde1; --accent: #fbc531; }
            body { font-family: 'Quicksand', sans-serif; background: #2c2c54; color: #dcdde1; }
            h1 { font-size: 6rem; color: #fbc531; text-shadow: 0 0 20px rgba(251, 197, 49, 0.5); margin: 0; }
            h2 { font-weight: 300; letter-spacing: 1px; }
            .container { position: relative; }
            .moon { width: 100px; height: 100px; background: #fbc531; border-radius: 50%; box-shadow: 0 0 50px #fbc531; margin: 0 auto 40px; opacity: 0.8; }
            .btn { background: transparent; border: 2px solid #dcdde1; color: #dcdde1; border-radius: 50px; }
            .btn:hover { background: #dcdde1; color: #2c2c54; }
        """,
        'card_css': "background: #2c2c54; color: #dcdde1; border-radius: 10px;"
    },
    '504': { # Ghost / Timeout
        'css': """
            :root { --bg: #f1f2f6; --text: #a4b0be; --accent: #57606f; }
            body { font-family: 'Arial', sans-serif; background: #f1f2f6; }
            h1 { font-size: 8rem; color: transparent; -webkit-text-stroke: 2px #a4b0be; opacity: 0.5; margin: 0; }
            h2 { color: #57606f; font-weight: bold; }
            .container { opacity: 0; animation: fadeIn 2s forwards; }
            @keyframes fadeIn { to { opacity: 1; } }
            .btn { color: #57606f; border-bottom: 2px solid #57606f; padding: 5px 0; border-radius: 0; }
            .btn:hover { color: #2f3542; border-color: #2f3542; background: none; }
        """,
        'card_css': "background: #f1f2f6; color: #57606f; -webkit-text-stroke: 1px #a4b0be;"
    },
    '505': { # Retro Game
        'css': """
            :root { --bg: #0f380f; --text: #9bbc0f; --accent: #8bac0f; }
            @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
            body { font-family: 'Courier New', monospace; background: #0f380f; color: #9bbc0f; }
            h1 { font-size: 3rem; margin-bottom: 20px; line-height: 1.5; }
            .container { border: 4px solid #9bbc0f; padding: 20px; max-width: 600px; background: #0f380f; box-shadow: 10px 10px 0 #306230; }
            .btn { background: #9bbc0f; color: #0f380f; border: none; font-weight: bold; box-shadow: 5px 5px 0 #306230; font-family: inherit; }
            .btn:hover { transform: translate(2px, 2px); box-shadow: 3px 3px 0 #306230; }
        """,
        'card_css': "background: #0f380f; color: #9bbc0f; border: 2px solid #9bbc0f; font-family: monospace;"
    },
    '506': { # Split
        'css': """
            :root { --bg: #fff; --text: #000; --accent: #000; }
            body { display: grid; grid-template-columns: 1fr 1fr; padding: 0; }
            .left { background: #000; color: #fff; display: flex; align-items: center; justify-content: center; height: 100vh; }
            .right { background: #fff; color: #000; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; padding: 40px; box-sizing: border-box; }
            h1 { font-size: 8rem; margin: 0; }
            h2 { font-size: 2rem; margin-bottom: 20px; }
            .btn { border: 2px solid #000; color: #000; }
            .btn:hover { background: #000; color: #fff; }
            .container { width: 100%; display: contents; }
            @media(max-width: 700px) { body { grid-template-columns: 1fr; } .left { height: 200px; } .right { height: auto; padding: 60px 20px; } .container { display: block; } }
        """,
        'card_css': "background: linear-gradient(90deg, #000 50%, #fff 50%); color: #888; border: 1px solid #000;"
    },
    '507': { # Stacked / Full
        'css': """
            :root { --bg: #ff9f43; --text: #fff; --accent: #ee5253; }
            body { font-family: 'Arial Rounded MT Bold', 'Arial', sans-serif; background: #ff9f43; }
            .container { background: #fff; color: #333; padding: 40px; border-radius: 20px; box-shadow: 0 10px 0 #ff6b6b; margin-top: -20px; max-width: 400px; }
            h1 { font-size: 5rem; color: #ee5253; margin: 0; }
            h2 { margin-bottom: 20px; }
            .btn { background: #ee5253; color: #fff; border-radius: 10px; width: 100%; display: block; box-sizing: border-box; text-align: center; }
            .btn:hover { background: #ff6b6b; }
        """,
        'card_css': "background: #ff9f43; color: #fff; border-bottom: 10px solid #ee5253;"
    },
    '509': { # Squeezed
        'css': """
            :root { --bg: #54a0ff; --text: #fff; --accent: #2e86de; }
            body { font-family: 'Oswald', sans-serif; background: #54a0ff; color: #fff; }
            h1 { font-size: 10rem; transform: scaleX(0.5); margin: 0; line-height: 0.8; }
            h2 { font-weight: 300; text-transform: uppercase; letter-spacing: 5px; margin-top: 20px; }
            .container { padding: 0 20px; border-left: 10px solid rgba(255,255,255,0.3); border-right: 10px solid rgba(255,255,255,0.3); height: 80vh; display: flex; flex-direction: column; justify-content: center; }
            .btn { background: #fff; color: #54a0ff; font-weight: bold; }
        """,
        'card_css': "background: #54a0ff; color: #fff; font-family: 'Impact', sans-serif; letter-spacing: -2px;"
    },
    '510': { # Puzzle / Missing
        'css': """
            :root { --bg: #c8d6e5; --text: #576574; --accent: #222f3e; }
            body { font-family: 'Verdana', sans-serif; background: #c8d6e5; color: #576574; }
            .container { border: 4px dashed #576574; padding: 50px; border-radius: 20px; background: rgba(255,255,255,0.5); position: relative; }
            .container::after { content: '?'; position: absolute; top: -30px; right: -30px; background: #576574; color: #fff; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; font-weight: bold; }
            h1 { font-size: 5rem; color: #222f3e; margin: 0; }
            .btn { background: #222f3e; color: #fff; border-radius: 5px; }
        """,
        'card_css': "background: #c8d6e5; color: #576574; border: 2px dashed #576574;"
    }
}

# Fallback for generic logic if needed, though we cover all 20 files above
DEFAULT_STYLE = {
    'css': ":root { --bg: #fff; --text: #333; --accent: #007bff; } body { font-family: sans-serif; background: #f8f9fa; } h1 { font-size: 5rem; } .container { background: #fff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); } .btn { background: #007bff; color: #fff; border-radius: 4px; }",
    'card_css': "background: #fff; color: #333;"
}

# Universal HTML Template that adapts to CSS
TEMPLATE = r"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{code} - {title}</title>
  <style>
    /* Base Reset */
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      transition: all 0.3s ease;
    }}
    a {{ text-decoration: none; }}
    
    /* Common Elements */
    .icon {{ margin-bottom: 20px; display: inline-block; }}
    .icon svg {{ width: 64px; height: 64px; fill: currentColor; }}
    .btn {{
      padding: 12px 30px;
      margin-top: 30px;
      display: inline-block;
      text-decoration: none;
      transition: transform 0.2s, box-shadow 0.2s;
      cursor: pointer;
    }}
    .btn:active {{ transform: scale(0.98); }}
    .desc {{ max-width: 500px; margin: 20px auto; line-height: 1.6; font-size: 1.1rem; opacity: 0.9; }}
    .hidden-data {{ display: none; }}
    
    /* Specific Injected CSS */
    {css}
    
    /* Responsive */
    @media (max-width: 600px) {{
      h1 {{ font-size: 4rem !important; }}
      .container {{ padding: 20px !important; width: 90% !important; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="icon">{icon_svg}</div>
    
    <!-- Special Split Structure for 506 -->
    {extra_html_start}
    
    <h1>{code}</h1>
    <h2>{title}</h2>
    <p class="desc">{desc}</p>
    <a href="./index.html" class="btn">RETURN HOME</a>
    
    {extra_html_end}
  </div>

  <div class="hidden-data">
    <div class="code-pill">HTTP {code}</div>
    <h1>{title}</h1>
    <p class="desc">{desc}</p>
    <div class="icon">{icon_svg}</div>
  </div>
</body>
</html>"""

def get_content(filepath, filename):
    if not os.path.exists(filepath): return None
    with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
    
    code_match = re.search(r'(?:<div class="code-pill">HTTP\s*|<span class="error-code">|<div class="big-code">|<span class="code">ERROR CODE: |<div class="code">|<div class="code-display">ERROR |<div class="code-box">|<div class="glitch" data-text=")(\d+)', content)
    file_code = filename.split('.')[0]
    code = code_match.group(1) if code_match else file_code
    
    # Use hardcoded data for reliability if code matches
    for p in PAGES_DATA:
        if p['code'] == code:
            # Try to extract SVG from file, otherwise default
            icon_match = re.search(r'<svg[\s\S]*?</svg>', content)
            icon_svg = icon_match.group(0) if icon_match else '<svg viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2z"/></svg>'
            return {
                'code': code,
                'title': p['title'],
                'desc': p['desc'],
                'icon_svg': icon_svg
            }

    # Fallback parsing
    title_match = re.search(r'<h1>\s*(.*?)\s*</h1>', content)
    desc_match = re.search(r'<p class="desc">\s*(.*?)\s*</p>', content)
    icon_match = re.search(r'<svg[\s\S]*?</svg>', content)

    return {
        'code': code,
        'title': title_match.group(1) if title_match else 'Error',
        'desc': desc_match.group(1) if desc_match else 'An unknown error occurred.',
        'icon_svg': icon_match.group(0) if icon_match else '<svg viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2z"/></svg>'
    }

def update_index():
    index_path = os.path.join(DIR, 'index.html')
    
    grid_html = ""
    card_styles = ""
    
    for p in PAGES_DATA:
        code = p['code']
        style = STYLES.get(code, DEFAULT_STYLE)
        
        # Add CSS rule for this specific card
        card_styles += f".card-{code} {{ {style.get('card_css', '')} }}\n"
        
        grid_html += f"""
        <a href="{code}.html" class="card card-{code}">
            <div class="code">{code}</div>
            <div class="title">{p['title']}</div>
            <div class="desc">{p['desc']}</div>
        </a>
        """

    index_content = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Unique Error Pages Gallery</title>
  <style>
    :root {{ --bg: #f0f2f5; --text: #333; }}
    body {{
      margin: 0; min-height: 100vh; background: var(--bg); color: var(--text);
      font-family: system-ui, sans-serif; padding: 40px;
    }}
    .header {{ text-align: center; margin-bottom: 50px; }}
    h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
    .subtitle {{ color: #666; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 30px;
      max-width: 1200px;
      margin: 0 auto;
    }}
    .card {{
      display: flex; flex-direction: column; justify-content: center; align-items: center;
      padding: 30px 20px;
      border-radius: 12px;
      text-decoration: none;
      text-align: center;
      transition: transform 0.3s, box-shadow 0.3s;
      box-shadow: 0 4px 6px rgba(0,0,0,0.05);
      min-height: 180px;
      position: relative;
      overflow: hidden;
    }}
    .card:hover {{
      transform: translateY(-5px) scale(1.02);
      box-shadow: 0 15px 30px rgba(0,0,0,0.1);
      z-index: 10;
    }}
    .code {{ font-size: 2.5rem; font-weight: bold; margin-bottom: 10px; line-height: 1; }}
    .title {{ font-weight: bold; font-size: 1rem; margin-bottom: 8px; text-transform: uppercase; }}
    .desc {{ font-size: 0.8rem; opacity: 0.8; }}
    
    /* Generated Card Styles */
    {card_styles}
  </style>
</head>
<body>
  <div class="header">
    <h1>Unique Style Gallery (V5)</h1>
    <p class="subtitle">20 Distinct Visual Identities</p>
  </div>
  <div class="grid">
    {grid_html}
  </div>
</body>
</html>"""

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print("已更新 index.html (画廊预览模式)")

def main():
    for filename in FILES:
        filepath = os.path.join(DIR, filename)
        data = get_content(filepath, filename)
        if data:
            code = data['code']
            style_config = STYLES.get(code, DEFAULT_STYLE)
            
            # Special handling for 506 split screen structure
            extra_html_start = ""
            extra_html_end = ""
            if code == '506':
                extra_html_start = '<div class="left">'
                extra_html_end = '</div><div class="right"><h2>Identity Crisis</h2><p>Server returned a variant list.</p></div>'

            new_html = TEMPLATE.format(
                css=style_config['css'],
                extra_html_start=extra_html_start,
                extra_html_end=extra_html_end,
                **data
            )
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"已更新 {filename} (独立风格: {code})")
        else:
            print(f"跳过 {filename} (未找到)")
    update_index()

if __name__ == '__main__':
    main()
