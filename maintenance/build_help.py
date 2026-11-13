#!/usr/bin/env python3
"""Builds the help page ../rauschen-werkzeug/help.html from ../rauschen-werkzeug/HELP.md.

HELP.md is the single source of the help. Run this script after every change there:
    python3 build_help.py
Then rebuild the offline version if needed (build_offline.py).

The page gets a table of contents that stays next to the text on wide screens and highlights the
section currently in view; on narrow screens it is a collapsible menu.
Fonts and colors (including dark mode) are taken from index.html so that both pages look the same.

Exactly the Markdown that HELP.md uses is supported: headings, paragraphs, lists (also nested),
tables, block quotes, **bold**, *italic*, `code` and links. The table of contents and the
"↑ Nach oben" links from HELP.md are dropped, the menu takes over their job. Links to other .md files
become plain text, because the page also has to work in the offline version.

License: MIT, see ../rauschen-werkzeug/LICENSE.txt
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent / 'rauschen-werkzeug'
SRC, PAGE, OUT = ROOT / 'HELP.md', ROOT / 'index.html', ROOT / 'help.html'
NO_SUBMENU = {'Häufige Fragen'}          # its subheadings are long questions, too much for the menu


def slug(text):
    """Anchor like GitHub: lower case, punctuation removed, spaces become hyphens."""
    return re.sub(r'[^\w\- ]', '', text.strip().lower()).replace(' ', '-')


def plain(text):
    """Heading without Markdown, for the menu."""
    return re.sub(r'[*`]', '', re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text))


def inline(text):
    codes = []
    def keep(m):
        codes.append(f'<code>{html.escape(m.group(1))}</code>')
        return f'\0{len(codes) - 1}\0'
    text = re.sub(r'`([^`]+)`', keep, text)          # protect code first, no Markdown applies inside it
    text = html.escape(text, quote=False)
    def link(m):
        label, target = m.group(1), m.group(2)
        if target.startswith('#'):
            return f'<a href="{target}">{label}</a>'
        if target.endswith('.md'):
            return label
        return f'<a href="{html.escape(target)}" target="_blank" rel="noopener">{label}</a>'
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', text)
    return re.sub(r'\0(\d+)\0', lambda m: codes[int(m.group(1))], text)


def render_list(items):
    """items: (indent, numbered, text) in file order; indentation creates sublists."""
    tag = 'ol' if items[0][1] else 'ul'
    out, i = [f'<{tag}>'], 0
    while i < len(items):
        indent, _, text = items[i]
        j = i + 1
        while j < len(items) and items[j][0] > indent:
            j += 1
        out.append(f'<li>{inline(text)}{render_list(items[i + 1:j]) if j > i + 1 else ""}</li>')
        i = j
    return ''.join(out) + f'</{tag}>'


def render_table(rows):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    head, body = cells[0], cells[2:]                  # row 2 is the separator row |---|
    out = ['<div class="table-box"><table>']
    if any(head):                                     # tables with an empty header row get no <thead>
        out.append('<thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead>')
    out.append('<tbody>' + ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in body) + '</tbody>')
    return ''.join(out) + '</table></div>'


def convert(md):
    """Returns (title, content HTML, menu entries)."""
    md = re.sub(r'^## Inhalt\n.*?(?=^## )', '', md, flags=re.S | re.M)        # the menu replaces the table of contents
    md = re.sub(r'^\[↑ Nach oben\]\(#inhalt\)\n', '', md, flags=re.M)
    lines = md.splitlines()
    title = lines.pop(0)[2:] if lines and lines[0].startswith('# ') else 'Hilfe'
    out, toc, i, section = [], [], 0, None
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.strip() == '---':
            i += 1
        elif m := re.match(r'^(#{2,6}) (.+)$', line):
            level, text = len(m.group(1)), m.group(2)
            out.append(f'<h{level} id="{slug(text)}">{inline(text)}</h{level}>')
            if level == 2:
                section = plain(text); toc.append((slug(text), section, []))
            elif level == 3 and toc and section not in NO_SUBMENU:
                toc[-1][2].append((slug(text), plain(text)))
            i += 1
        elif line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(lines[i]); i += 1
            out.append(render_table(rows))
        elif line.startswith('>'):
            quote = []
            while i < len(lines) and lines[i].startswith('>'):
                quote.append(lines[i].lstrip('>').strip()); i += 1
            out.append(f'<blockquote><p>{inline(" ".join(quote))}</p></blockquote>')
        elif re.match(r'^\s*([-*]|\d+\.) ', line):
            items = []
            while i < len(lines) and (m := re.match(r'^(\s*)([-*]|\d+\.) (.*)$', lines[i])):
                items.append((len(m.group(1)), m.group(2)[0].isdigit(), m.group(3))); i += 1
            out.append(render_list(items))
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r'^(#{2,6} |\||>|\s*([-*]|\d+\.) |---$)', lines[i]):
                para.append(lines[i].strip()); i += 1
            out.append(f'<p>{inline(" ".join(para))}</p>')
    return title, '\n'.join(out), toc


def render_toc(toc):
    items = []
    for sid, text, subs in toc:
        sub = ''.join(f'<li><a href="#{s}">{html.escape(t)}</a></li>' for s, t in subs)
        items.append(f'<li><a href="#{sid}">{html.escape(text)}</a>{f"<ul>{sub}</ul>" if sub else ""}</li>')
    return '<ul>' + ''.join(items) + '</ul>'


# Take fonts and colors from index.html: everything in <style> up to the general base rules
page = PAGE.read_text(encoding='utf-8')
m = re.search(r'<style>\n(.*?)(?=^  \*, \*::before, \*::after)', page, flags=re.S | re.M)
if not m or '--primary' not in m.group(1):
    raise SystemExit('Abgebrochen: Schrift- und Farbdefinitionen in index.html nicht gefunden.')
tokens = m.group(1)

title, body, toc = convert(SRC.read_text(encoding='utf-8'))
ids = set(re.findall(r' id="([^"]+)"', body))
broken = sorted(set(re.findall(r'href="#([^"]+)"', body + render_toc(toc))) - ids)
if broken:
    raise SystemExit(f'Abgebrochen: Links ohne Ziel in HELP.md: {broken}')

OUT.write_text(f'''<!DOCTYPE html>
<!-- Generated from HELP.md by maintenance/build_help.py. Do not edit by hand. -->
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Hilfe – Rauschen-Werkzeug</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎧</text></svg>">
<style>
{tokens}  *, *::before, *::after {{ box-sizing: inherit; }}
  body {{ margin: 0; background: var(--bg); color: var(--ink);
    font-family: "Atkinson Hyperlegible", "Segoe UI", system-ui, -apple-system, sans-serif; font-size: 1rem; line-height: 1.55; }}
  a {{ color: var(--primary); }}
  a:focus-visible, summary:focus-visible {{ outline: 3px solid var(--focus); outline-offset: 2px; border-radius: 2px; }}

  .layout {{ max-width: 1120px; margin: 0 auto; padding: 32px 20px 64px; display: grid; grid-template-columns: 240px minmax(0, 1fr); gap: 48px; }}
  .page-head {{ grid-column: 1 / -1; display: flex; flex-direction: column; align-items: flex-start; gap: 16px; }}
  .page-head h1 {{ margin: 0; font-size: 1.875rem; line-height: 2.375rem; letter-spacing: -0.01em; }}
  .back {{ display: inline-flex; align-items: center; gap: 6px; height: 38px; padding: 0 14px 0 10px; border: 1px solid var(--btn-line);
    border-radius: 6px; background: var(--surface); color: var(--ink); font-size: 0.875rem; font-weight: 700; text-decoration: none; }}
  .back:hover {{ background: var(--hover); }}

  /* Floating table of contents next to the text */
  .toc {{ position: sticky; top: 24px; align-self: start; max-height: calc(100vh - 48px); overflow-y: auto;
    padding: 16px 12px; background: var(--surface); border: 1px solid var(--card-line); border-radius: 12px; font-size: 0.875rem; }}
  .toc summary {{ display: none; }}
  .toc ul {{ list-style: none; margin: 0; padding: 0; }}
  .toc ul ul {{ margin: 2px 0 6px 10px; padding-left: 8px; border-left: 1px solid var(--card-line); }}
  .toc a {{ display: block; padding: 4px 8px; border-radius: 6px; color: var(--ink); text-decoration: none; line-height: 1.3; }}
  .toc ul ul a {{ color: var(--muted); }}
  .toc a:hover {{ background: var(--hover); color: var(--ink); }}
  .toc a.active {{ background: var(--primary-ring); color: var(--primary); font-weight: 700; }}

  .content {{ min-width: 0; max-width: 760px; }}
  .content > :first-child {{ margin-top: 0; }}
  .content h2 {{ margin: 2.5rem 0 0.6rem; padding-bottom: 0.3rem; font-size: 1.375rem; border-bottom: 1px solid var(--card-line); }}
  .content h3 {{ margin: 1.75rem 0 0.4rem; font-size: 1.0625rem; }}
  .content [id] {{ scroll-margin-top: 20px; }}
  .content ol, .content ul {{ padding-left: 1.4rem; }}
  .content li + li {{ margin-top: 0.3rem; }}
  .content code {{ font-size: 0.875em; padding: 0.05em 0.3em; border-radius: 4px; background: var(--surface-2); border: 1px solid var(--card-line); }}
  .content blockquote {{ margin: 1rem 0; padding: 0.7rem 1rem; border-radius: 8px; background: var(--added-wash); }}
  .content blockquote p {{ margin: 0; }}
  .table-box {{ overflow-x: auto; margin: 0.75rem 0; }}
  /* separate instead of collapse, plus border-box: otherwise the borders overhang by 1 px and cause a scrollbar */
  .content table {{ box-sizing: border-box; border-collapse: separate; border-spacing: 0; width: 100%; font-size: 0.9rem;
    border-top: 1px solid var(--card-line); border-left: 1px solid var(--card-line); }}
  .content th, .content td {{ text-align: left; vertical-align: top; padding: 7px 10px;
    border-right: 1px solid var(--card-line); border-bottom: 1px solid var(--card-line); background: var(--surface); }}
  .content th {{ background: var(--surface-2); }}

  /* Narrow screens: table of contents as a collapsible menu above the text */
  @media (max-width: 860px) {{
    .layout {{ grid-template-columns: minmax(0, 1fr); gap: 24px; padding-top: 24px; }}
    .toc {{ position: static; max-height: none; padding: 0; }}
    .toc summary {{ display: block; padding: 12px 16px; font-weight: 700; cursor: pointer; }}
    .toc[open] summary {{ border-bottom: 1px solid var(--card-line); }}
    .toc > ul {{ padding: 8px; }}
  }}
</style>
</head>
<body>
<div class="layout">
  <header class="page-head">
    <a class="back" id="back" href="index.html">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>
      Zurück zum Werkzeug
    </a>
    <h1>{html.escape(title)}</h1>
  </header>
  <nav aria-label="Inhalt der Hilfe">
    <details class="toc" id="toc" open>
      <summary>Inhalt</summary>
      {render_toc(toc)}
    </details>
  </nav>
  <main class="content">
{body}
  </main>
</div>
<script>
// Go back through the history instead of reloading the tool: that way the browser restores the page
// including the file list. If the help was opened directly there is no history, so it is a normal link.
// In the offline version the help is a layer above the tool; then the tool closes it.
document.getElementById('back').addEventListener('click', e => {{
  if (window.parent !== window) {{ e.preventDefault(); parent.postMessage('rauschen-hilfe-schliessen', '*'); }}
  else if (history.length > 1) {{ e.preventDefault(); history.back(); }}
}});

// Narrow: menu collapsed initially and collapsed again after a click. Wide: always open.
const toc = document.getElementById('toc'), narrow = matchMedia('(max-width: 860px)');
const sync = () => {{ toc.open = !narrow.matches; }};
sync(); narrow.addEventListener('change', sync);
toc.addEventListener('click', e => {{ if (narrow.matches && e.target.closest('a')) toc.open = false; }});

// Highlight the menu entry of the section currently at the top of the window
const links = new Map([...toc.querySelectorAll('a')].map(a => [decodeURIComponent(a.hash.slice(1)), a]));
const heads = [...document.querySelectorAll('.content h2[id], .content h3[id]')].filter(h => links.has(h.id));
function highlight() {{
  let current = heads[0];
  for (const h of heads) if (h.getBoundingClientRect().top <= 80) current = h;
  links.forEach(a => {{ a.classList.remove('active'); a.removeAttribute('aria-current'); }});
  const a = current && links.get(current.id);
  if (!a) return;
  a.classList.add('active'); a.setAttribute('aria-current', 'true');
  // Only scroll the menu itself; scrollIntoView would also move the page
  if (!narrow.matches) {{
    if (a.offsetTop < toc.scrollTop) toc.scrollTop = a.offsetTop - 16;
    else if (a.offsetTop + a.offsetHeight > toc.scrollTop + toc.clientHeight) toc.scrollTop = a.offsetTop + a.offsetHeight - toc.clientHeight + 16;
  }}
}}
let raf = 0;
addEventListener('scroll', () => {{ cancelAnimationFrame(raf); raf = requestAnimationFrame(highlight); }}, {{ passive: true }});
highlight();
</script>
</body>
</html>
''', encoding='utf-8')
print(f'{OUT.name}: {len(ids)} Sprungmarken, {len(toc)} Menüabschnitte, alle Links gültig.')
