#!/usr/bin/env python3
"""Recolor sakura.yaml to neonwave palette and generate HTML preview."""
import re
import html
from pathlib import Path

SRC = Path.home() / "Downloads" / "sakura.yaml"
OUT_YAML = Path.home() / "Downloads" / "sakura-neonwave.yaml"
OUT_HTML = Path.home() / "Downloads" / "sakura-preview.html"

# ---- gradient helpers ----
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*(int(round(x)) for x in rgb))

def lerp(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))

def gradient(waypoints, n):
    """waypoints: [(pos_0to1, '#hex'), ...]. Returns n hex strings."""
    out = []
    for i in range(n):
        t = i / (n - 1) if n > 1 else 0
        for j in range(len(waypoints) - 1):
            p1, c1 = waypoints[j]
            p2, c2 = waypoints[j + 1]
            if p1 <= t <= p2:
                lt = (t - p1) / (p2 - p1) if p2 > p1 else 0
                out.append(rgb_to_hex(lerp(hex_to_rgb(c1), hex_to_rgb(c2), lt)))
                break
    return out

WAYPOINTS = [
    (0.00, "#FF2975"),  # hot magenta (banner_title)
    (0.20, "#F222FF"),  # electric pink (ui_label)
    (0.40, "#FF6EC7"),  # hot pink
    (0.60, "#FFFFFF"),  # white (midpoint)
    (0.80, "#65A1D3"),  # sky blue (from banner_logo)
    (1.00, "#00FFFF"),  # cyan (banner_accent)
]

# ---- 1. read source ----
src = SRC.read_text()

# ---- 2. replace welcome/goodbye 38-stop gradient ----
HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}")

def recolor_line(line):
    n = len(HEX_RE.findall(line))
    new_hexes = gradient(WAYPOINTS, n)
    # Replace in order, each occurrence exactly once. Walk the string.
    result = []
    pos = 0
    idx = 0
    for m in HEX_RE.finditer(line):
        result.append(line[pos:m.start()])
        result.append(new_hexes[idx])
        pos = m.end()
        idx += 1
    result.append(line[pos:])
    return "".join(result)

lines = src.split("\n")
for i, line in enumerate(lines):
    if line.startswith("  welcome:") or line.startswith("  goodbye:"):
        lines[i] = recolor_line(line)

result = "\n".join(lines)

# ---- 3. replace banner_hero atmospheric colors (global — verified safe) ----
result = result.replace("#FFD1DC", "#FF6EC7")  # ground/petals
result = result.replace("#FFB7C5", "#00FFFF")  # HANAMI accents
result = result.replace("#CC5B8F", "#6B1FB1")  # HANAMI text

OUT_YAML.write_text(result)
print(f"wrote {OUT_YAML}")

# ---- 4. build HTML preview ----
import yaml
cfg = yaml.safe_load(result)
colors = cfg["colors"]

# Rich markup → HTML translator
RICH_RE = re.compile(r"\[(bold\s+)?(#[0-9A-Fa-f]{6})\](.*?)\[/\]")
def rich_to_html(text):
    def repl(m):
        bold = m.group(1)
        color = m.group(2)
        body = html.escape(m.group(3))
        style = f"color:{color}"
        if bold:
            style += ";font-weight:bold"
        return f'<span style="{style}">{body}</span>'
    # process inside-out so nested cases work
    prev = None
    while prev != text:
        prev = text
        text = RICH_RE.sub(repl, text)
    return text

def render_multiline(s):
    """Convert Rich-markup multi-line banner text to HTML, preserving whitespace."""
    rendered = rich_to_html(s)
    return rendered

palette_labels = [
    ("banner_border", "Banner outer frame"),
    ("banner_title", "Title text"),
    ("banner_accent", "Flourishes"),
    ("banner_dim", "Banner dim"),
    ("banner_text", "Banner body"),
    ("ui_accent", "UI highlight"),
    ("ui_label", "Field label"),
    ("ui_ok", "Success"),
    ("ui_error", "Error"),
    ("ui_warn", "Warning"),
    ("prompt", "Prompt glyph"),
    ("input_rule", "Input underline"),
    ("response_border", "Response frame"),
    ("session_label", "Session label"),
    ("session_border", "Session frame"),
]

palette_html = ""
for key, desc in palette_labels:
    c = colors.get(key, "#000000")
    palette_html += f'''
    <div class="swatch">
      <div class="chip" style="background:{c}"></div>
      <div>
        <div style="font-weight:bold; color:{c}">{key}</div>
        <div style="font-size:10px; color:#B0A4B8">{c} &nbsp;·&nbsp; {desc}</div>
      </div>
    </div>'''

banner_logo_html = render_multiline(cfg["banner_logo"])
banner_hero_html = render_multiline(cfg["banner_hero"])
welcome_html = render_multiline(cfg["branding"]["welcome"])
goodbye_html = render_multiline(cfg["branding"]["goodbye"])

tool_emojis = cfg["tool_emojis"]
tool_grid_html = ""
for name, emoji in tool_emojis.items():
    tool_grid_html += f'<div><div style="color:{colors["ui_accent"]};font-size:22px">{html.escape(emoji)}</div><div class="label">{html.escape(name)}</div></div>'

thinking_verbs = cfg["spinner"]["thinking_verbs"]
thinking_faces = cfg["spinner"]["thinking_faces"]
# Build JS-free CSS animation that cycles verbs via pseudo-element
verbs_css = ""
for i, v in enumerate(thinking_verbs):
    start = i * (100 / len(thinking_verbs))
    end = (i + 1) * (100 / len(thinking_verbs))
    verbs_css += f'{start:.2f}%, {end - 0.01:.2f}% {{ content: "{html.escape(v)}"; }}\n'

resp_label = cfg["branding"]["response_label"]
prompt_symbol = cfg["branding"]["prompt_symbol"]

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>✿ Sakura × Neonwave — Preview</title>
<style>
  :root {{
    --bg: {colors['session_border']};
    --bg-panel: #0a0614;
    --fg: {colors['banner_text']};
    --accent: {colors['banner_title']};
    --border: {colors['banner_border']};
  }}
  * {{ box-sizing: border-box; }}
  body {{
    background: var(--bg);
    color: var(--fg);
    font-family: ui-monospace, 'SF Mono', Menlo, 'Cascadia Code', Consolas, monospace;
    padding: 32px;
    font-size: 13px;
    line-height: 1.5;
    max-width: 1100px;
    margin: 0 auto;
  }}
  h1 {{ color: var(--accent); font-size: 22px; margin-top: 0; }}
  h2 {{
    color: var(--accent);
    font-size: 14px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 4px;
    margin-top: 32px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }}
  .swatch-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin: 16px 0;
  }}
  .swatch {{
    padding: 10px 12px;
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--bg-panel);
  }}
  .swatch .chip {{
    width: 28px;
    height: 28px;
    border: 1px solid var(--bg);
    flex-shrink: 0;
  }}
  .banner {{
    white-space: pre;
    font-size: 12px;
    line-height: 1.0;
    background: #000;
    padding: 16px;
    border: 1px solid var(--border);
    overflow-x: auto;
  }}
  .chatbox {{
    border: 2px solid {colors['response_border']};
    padding: 20px;
    margin: 16px 0;
    background: #000;
    font-size: 14px;
  }}
  .chatbox .label {{
    background: {colors['response_border']};
    color: #000;
    padding: 2px 10px;
    font-weight: bold;
    display: inline-block;
    letter-spacing: 0.05em;
  }}
  .tool-line {{
    color: var(--fg);
    font-size: 13px;
    margin-top: 12px;
  }}
  .prompt-line {{
    background: #000;
    border: 1px solid var(--border);
    padding: 12px 16px;
    font-size: 14px;
    margin: 16px 0;
    display: flex;
    align-items: baseline;
    gap: 8px;
  }}
  .prompt-line .glyph {{ color: {colors['prompt']}; }}
  .prompt-line .rule {{
    display: inline-block;
    min-width: 200px;
    border-bottom: 2px solid {colors['input_rule']};
  }}
  .tool-grid {{
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 8px;
    margin: 16px 0;
  }}
  .tool-grid > div {{
    background: var(--bg-panel);
    padding: 10px 4px;
    border: 1px solid var(--border);
    text-align: center;
  }}
  .tool-grid .label {{ font-size: 10px; color: var(--fg); margin-top: 4px; }}
  @keyframes faces {{
    0%, 19% {{ content: "{html.escape(thinking_faces[0])}"; }}
    20%, 39% {{ content: "{html.escape(thinking_faces[1])}"; }}
    40%, 59% {{ content: "{html.escape(thinking_faces[2])}"; }}
    60%, 79% {{ content: "{html.escape(thinking_faces[3])}"; }}
    80%, 100% {{ content: "{html.escape(thinking_faces[4])}"; }}
  }}
  @keyframes verbs {{
{verbs_css}  }}
  .spinner::before {{
    content: "";
    animation: faces 1.5s steps(1, end) infinite;
    color: {colors['ui_accent']};
    font-weight: bold;
  }}
  .spinner::after {{
    content: "";
    animation: verbs 8s steps(1, end) infinite;
    color: {colors['ui_label']};
  }}
  .spinner {{ font-size: 14px; }}
  .divider {{ color: var(--border); }}
  .meta {{ font-size: 11px; color: var(--fg); opacity: 0.75; }}
</style>
</head>
<body>

<h1>✿ Sakura × Neonwave — Preview</h1>
<p class="meta">
  Target file: <code>~/Downloads/sakura-neonwave.yaml</code> &nbsp;·&nbsp;
  Identity preserved (agent_name, labels, emojis, copy, braille art) &nbsp;·&nbsp;
  Every hex recolored to the neonwave palette.
</p>

<h2>Palette (top <code>colors:</code> block)</h2>
<div class="swatch-grid">{palette_html}
</div>

<h2>banner_logo (shown on <code>hermes chat</code> start)</h2>
<div class="banner">{banner_logo_html}</div>

<h2>banner_hero (shown on welcome)</h2>
<div class="banner">{banner_hero_html}</div>

<h2>welcome gradient</h2>
<div class="banner" style="font-size:16px">{welcome_html}</div>

<h2>goodbye gradient</h2>
<div class="banner" style="font-size:16px">{goodbye_html}</div>

<h2>Simulated chat response</h2>
<div class="chatbox">
  <div><span class="label">{html.escape(resp_label.strip())}</span></div>
  <br>
  <div>Dhroov — I'm listening.</div>
  <div class="tool-line"><span class="divider">┊</span> <span style="color:{colors['ui_accent']}">{tool_emojis['memory']}</span> <span style="color:{colors['ui_label']}">memory</span>: recalled 3 relevant notes</div>
  <div class="tool-line"><span class="divider">┊</span> <span style="color:{colors['ui_accent']}">{tool_emojis['terminal']}</span> <span style="color:{colors['ui_label']}">terminal</span>: <span style="color:{colors['ui_ok']}">OK</span></div>
  <br>
  <div class="spinner"></div>
</div>

<div class="prompt-line">
  <span class="glyph">{html.escape(prompt_symbol.strip())}</span>
  <span class="rule"></span>
</div>

<h2>Tool emojis (14 tools)</h2>
<div class="tool-grid">{tool_grid_html}</div>

<h2 style="color:{colors['ui_ok']}">Status</h2>
<div style="background:var(--bg-panel); padding:12px; border-left: 4px solid {colors['ui_ok']};">
  <span style="color:{colors['ui_ok']}">✓ OK — this renders whatever the neonwave-colored sakura.yaml would produce in a real Hermes session.</span>
</div>
<div style="background:var(--bg-panel); padding:12px; border-left: 4px solid {colors['ui_warn']}; margin-top:8px">
  <span style="color:{colors['ui_warn']}">⚠ Warning — example line to show the warn color in context.</span>
</div>
<div style="background:var(--bg-panel); padding:12px; border-left: 4px solid {colors['ui_error']}; margin-top:8px">
  <span style="color:{colors['ui_error']}">✗ Error — example line to show the error color in context.</span>
</div>

<p class="meta" style="margin-top:40px">
  If this looks right: tell Claude to ship it. Rollback is always one command away.
</p>

</body>
</html>
"""

OUT_HTML.write_text(HTML)
print(f"wrote {OUT_HTML}")

# ---- 5. sanity checks ----
parsed = yaml.safe_load(result)
assert parsed["name"] == "sakura"
print(f"YAML parses OK. Keys: {sorted(parsed.keys())}")

remaining_pastels = []
for bad in ("#CC3366", "#FFD1DC", "#FFB7C5", "#CC5B8F"):
    if bad in result:
        remaining_pastels.append(bad)
if remaining_pastels:
    print(f"WARN: still contains legacy pastels: {remaining_pastels}")
else:
    print("All legacy pastels removed.")

# Count changes vs source
changed_hexes = 0
for m_old, m_new in zip(HEX_RE.findall(src), HEX_RE.findall(result)):
    if m_old != m_new:
        changed_hexes += 1
print(f"{changed_hexes} hex values changed (out of {len(HEX_RE.findall(src))} total).")
