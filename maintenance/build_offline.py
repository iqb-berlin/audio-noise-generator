#!/usr/bin/env python3
"""Builds a single HTML file from rauschen-werkzeug/ that works when opened by double-click (file://).

Under file:// browsers block loading modules, web workers and the .wasm file.
Everything is therefore embedded here:
  - fonts as data: URIs
  - the page modules engine.js and zip.js directly in the main script
  - FFmpeg core (JS) + engine-worker.js as text, from which the page starts a classic worker via a blob URL
  - ffmpeg-core.wasm as Base64; the page compiles it once and hands the compiled module to every worker
  - the help page and all license texts

The source (rauschen-werkzeug/) is only read. The result goes to maintenance/build/audio-noise-generator-offline.html,
which is not committed but uploaded as a release asset (see RELEASING.md).
Usage: python3 maintenance/build_offline.py

License: MIT, see ../LICENSE. The embedded libraries keep their own licenses
(see rauschen-werkzeug/LICENSES.md); their license texts are written into the file as well.
"""
import base64
import datetime
import html as html_lib
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'rauschen-werkzeug'
OUT = ROOT / 'maintenance' / 'build' / 'audio-noise-generator-offline.html'


def replace_once(text, old, new, what):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'Build abgebrochen: „{what}“ {count}-mal statt einmal gefunden. Hat sich index.html geändert?')
    return text.replace(old, new)


def b64(path):
    return base64.b64encode(path.read_bytes()).decode('ascii')


html = (SRC / 'index.html').read_text(encoding='utf-8')

# 1. Embed fonts
for weight in ('400', '700'):
    name = f'lib/fonts/atkinson-hyperlegible-latin-{weight}-normal.woff2'
    html = replace_once(html, f'url("{name}")', f'url("data:font/woff2;base64,{b64(SRC / name)}")', name)

# 2. Remove the file:// block: that is exactly where this version is meant to run
html, n = re.subn(r'<script>\n// Separate script: under file:// .*?</script>\n', '', html, flags=re.S)
if n != 1:
    raise SystemExit('Build abgebrochen: file://-Prüfskript nicht gefunden.')
html = replace_once(html, "if (location.protocol === 'file:') {", 'if (false) {', 'file://-Prüfung in addFiles')

# 2b. Embed license texts and notices: links to text files do not work in the single file,
#     but the texts have to be distributed along with it (GPL, MIT, BSD, OFL, ...)
def embed_license(match):
    text = (SRC / match.group(1)).read_text(encoding='utf-8')
    return f'<details class="license-text"><summary>{match.group(2)}</summary><pre>{html_lib.escape(text)}</pre></details>'

html, n = re.subn(r'<a class="license" href="([^"]+)"[^>]*>([^<]+)</a>', embed_license, html)
if n < 5:
    raise SystemExit(f'Build abgebrochen: nur {n} Lizenzlinks gefunden.')
html, n = re.subn(r'<p id="license-overview">.*?</p>', '<p>Diese Datei ist die Offline-Fassung des Werkzeugs. Alle Lizenztexte sind oben eingebettet.</p>', html, flags=re.S)
if n != 1:
    raise SystemExit('Build abgebrochen: Hinweis auf LICENSES.md nicht gefunden.')

# 2c. Embed the help page: there is no second file offline. The help button therefore opens the embedded
#     page from a blob URL as a full-page layer above the tool (see the script below).
#     The help is stored as Base64 because it contains a <script> of its own, which would otherwise end an
#     enclosing <script> early.
help_html = (SRC / 'help.html').read_text(encoding='utf-8')
for weight in ('400', '700'):
    name = f'lib/fonts/atkinson-hyperlegible-latin-{weight}-normal.woff2'
    help_html = replace_once(help_html, f'url("{name}")', f'url("data:font/woff2;base64,{b64(SRC / name)}")', f'{name} in help.html')
HELP_PAYLOAD = (
    f'<script type="application/octet-stream" id="hilfe-b64">{base64.b64encode(help_html.encode("utf-8")).decode("ascii")}</script>\n'
    + r"""<script>
// Offline version: Chromium and Edge do not restore locally opened pages after navigating away,
// so the file list would be lost. The help is therefore a full-page layer above the tool.
// A history entry makes sure the browser's back button closes it as well.
(() => {
  let frame = null, url = null;
  function close() {
    if (!frame) return;
    frame.remove(); frame = null;
    document.documentElement.style.overflow = '';
    document.getElementById('help-link').focus();
  }
  document.getElementById('help-link').addEventListener('click', e => {
    e.preventDefault();
    if (frame) return;
    if (!url) {
      const bytes = Uint8Array.from(atob(document.getElementById('hilfe-b64').textContent), c => c.charCodeAt(0));
      url = URL.createObjectURL(new Blob([bytes], { type: 'text/html;charset=utf-8' }));
    }
    frame = document.createElement('iframe');
    frame.src = url; frame.title = 'Hilfe zum Rauschen-Werkzeug';
    frame.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;border:0;z-index:1000;background:var(--bg)';
    document.documentElement.style.overflow = 'hidden';
    document.body.append(frame);
    frame.addEventListener('load', () => frame && frame.focus(), { once: true });
    history.pushState({ rauschenHilfe: true }, '');
  });
  addEventListener('message', e => { if (e.data === 'rauschen-hilfe-schliessen' && frame) history.back(); });
  addEventListener('popstate', close);
})();
</script>
"""
)

# 3. Worker source for a classic (non-module) worker: the core followed by engine-worker.js without its import.
#    The core is modified slightly; the GPL (section 2a) requires modified files to state the change and its date.
core_version = re.search(r'@ffmpeg/core (\S+)', (SRC / 'lib/core/SOURCES.txt').read_text(encoding='utf-8'))
if not core_version:
    raise SystemExit('Build abgebrochen: Version des Kerns in lib/core/SOURCES.txt nicht gefunden.')
CHANGE_NOTICE = f'''// Geänderte Fassung von ffmpeg-core.js aus @ffmpeg/core {core_version.group(1)} (GPL-2.0-or-later).
// Geändert am {datetime.date.today().isoformat()} durch maintenance/build_offline.py des Rauschen-Werkzeugs:
// "import.meta.url" ersetzt, "export default" entfernt und um die Worker-Logik aus engine-worker.js
// ergänzt, damit der Kern als klassischer Hintergrundprozess aus dieser Datei heraus läuft.
// Unveränderter Quellcode: siehe „Datenschutz und Lizenzen“ auf dieser Seite.
'''
core = (SRC / 'lib/core/ffmpeg-core.js').read_text(encoding='utf-8')
core = core.replace('import.meta.url', '"http://offline.invalid/ffmpeg-core.js"')   # never fetched, the wasm arrives as a compiled module
core = replace_once(core, 'export default createFFmpegCore;', '', 'export im Kern')
worker_logic = replace_once((SRC / 'engine-worker.js').read_text(encoding='utf-8'),
                            "import createFFmpegCore from './lib/core/ffmpeg-core.js';\n", '', 'Import in engine-worker.js')
WORKER = CHANGE_NOTICE + core + '\n' + worker_logic

# 4. Inline the page modules. engine.js gets loaders that take worker and core from the embedded text.
OFFLINE_LOADERS = r'''// Offline version: worker and core are embedded in this file (see maintenance/build_offline.py)
const embedded = id => { const el = document.getElementById(id), text = el.textContent; el.remove(); return text; };
let workerUrl = null;
const loaders = {
  worker() {
    workerUrl ??= URL.createObjectURL(new Blob([embedded('ffmpeg-worker-src')], { type: 'text/javascript' }));
    return new Worker(workerUrl);
  },
  async wasm() {
    const b64 = embedded('ffmpeg-wasm-b64');
    const bytes = typeof Uint8Array.fromBase64 === 'function' ? Uint8Array.fromBase64(b64) : Uint8Array.from(atob(b64), c => c.charCodeAt(0));
    return WebAssembly.compile(bytes);
  },
};
'''


def module_code(name):
    """A page module as plain code: without "export", to be pasted into the main script."""
    return re.sub(r'^export ', '', (SRC / name).read_text(encoding='utf-8'), flags=re.M)


engine, n = re.subn(r'// <loaders>\n.*?// </loaders>\n', lambda _: OFFLINE_LOADERS, module_code('engine.js'), flags=re.S)
if n != 1:
    raise SystemExit('Build abgebrochen: Block <loaders> in engine.js nicht gefunden.')
inlined = engine + '\n' + module_code('zip.js')
if '</script' in inlined.lower():
    raise SystemExit('Build abgebrochen: engine.js oder zip.js enthält </script.')
html = replace_once(html, "import { FFmpeg } from './engine.js';\nimport { zipStore } from './zip.js';", inlined, 'Imports im Hauptskript')

# 5. Data at the end of <body> so the interface is visible before it loads
payload = (
    f'<script type="text/plain" id="ffmpeg-worker-src">{WORKER}</script>\n'
    f'<script type="application/octet-stream" id="ffmpeg-wasm-b64">{b64(SRC / "lib/core/ffmpeg-core.wasm")}</script>\n'
    + HELP_PAYLOAD
)
html = replace_once(html, '</body>', payload + '</body>', '</body>')
if '</script' in WORKER.lower():
    raise SystemExit('Build abgebrochen: Worker-Quelltext enthält </script.')

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding='utf-8')
print(f'{OUT.relative_to(ROOT)}: {OUT.stat().st_size / 2**20:.1f} MiB')
