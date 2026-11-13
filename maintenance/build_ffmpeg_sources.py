#!/usr/bin/env python3
"""Collects the complete source code of the bundled FFmpeg core and the license notices of every library in it.

Why: lib/core/ffmpeg-core.wasm is GPL-2.0-or-later. Whoever passes it on (repository download, release asset)
has to offer the corresponding source code from the same place (GPL-2.0, section 3). The BSD, MIT and ISC
libraries inside the core also require their copyright notices to accompany the binary.

What it does:
  1. checks that lib/core/ still holds exactly @ffmpeg/core 0.12.10 (SHA-256)
  2. fetches ffmpeg.wasm at the commit the core was released from and checks its Dockerfile against SOURCES
  3. fetches FFmpeg and every library at the version named there
  4. writes, all in maintenance/build/ (not committed):
       ffmpeg-core-0.12.10-source.tar.gz   upload once as a release asset, see maintenance/RELEASING.md
     and into the repository (committed):
       rauschen-werkzeug/lib/core/THIRD-PARTY-NOTICES.txt   license notices, also embedded by build.py
       rauschen-werkzeug/lib/core/SOURCES.txt               exact versions and commits

Only needed again when lib/core/ is replaced by a different version; then update CORE_* and SOURCES first.
Needs git and network access, downloads about 300 MB. Usage: python3 maintenance/build_ffmpeg_sources.py

License: MIT, see ../LICENSE.
"""
import hashlib
import pathlib
import re
import shutil
import subprocess
import tarfile
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORE_DIR = ROOT / 'rauschen-werkzeug' / 'lib' / 'core'
BUILD = ROOT / 'maintenance' / 'build'
CLONES = BUILD / 'clones'

CORE_VERSION = '0.12.10'
CORE_SHA256 = {
    'ffmpeg-core.wasm': '9f57947a5bd530d8f00c5b3f2cb2a3492faa7e5d823315342d6a8656d0a6b7b7',
    'ffmpeg-core.js': '67a48f11645f85439f3fde4f2119042c16b374b910206b7a7a24f342e28dcae3',   # dist/esm
}
# @ffmpeg/core 0.12.10 was released from this commit (tag v12.15); 0.12.9 has byte-identical files
FFMPEG_WASM = dict(url='https://github.com/ffmpegwasm/ffmpeg.wasm.git', ref='v12.15', commit='71aa99d37c',
                   notices=['LICENSE'], license='MIT (Build-Skripte), Kern als Ganzes GPL-2.0-or-later')
EMSCRIPTEN_VERSION = '3.1.40'

# name: Dockerfile variable, repository, ref, license (SPDX), license files to reproduce
SOURCES = {
    'FFmpeg':     ('FFMPEG_VERSION',    'https://github.com/FFmpeg/FFmpeg.git',       'n5.1.4',        'LGPL-2.1-or-later, mit --enable-gpl GPL-2.0-or-later', ['LICENSE.md', 'COPYING.GPLv2', 'COPYING.LGPLv2.1']),
    'x264':       ('X264_BRANCH',       'https://github.com/ffmpegwasm/x264.git',     '4-cores',       'GPL-2.0-or-later',          ['COPYING']),
    'x265':       ('X265_BRANCH',       'https://github.com/ffmpegwasm/x265.git',     '3.4',           'GPL-2.0-or-later',          ['COPYING']),
    'libvpx':     ('LIBVPX_BRANCH',     'https://github.com/ffmpegwasm/libvpx.git',   'v1.13.1',       'BSD-3-Clause',              ['LICENSE', 'PATENTS']),
    'LAME':       ('LAME_BRANCH',       'https://github.com/ffmpegwasm/lame.git',     'master',        'LGPL-2.0-or-later',         ['COPYING']),
    'libogg':     ('OGG_BRANCH',        'https://github.com/ffmpegwasm/Ogg.git',      'v1.3.4',        'BSD-3-Clause',              ['COPYING']),
    'libtheora':  ('THEORA_BRANCH',     'https://github.com/ffmpegwasm/theora.git',   'v1.1.1',        'BSD-3-Clause',              ['COPYING', 'LICENSE']),
    'Opus':       ('OPUS_BRANCH',       'https://github.com/ffmpegwasm/opus.git',     'v1.3.1',        'BSD-3-Clause',              ['COPYING']),
    'libvorbis':  ('VORBIS_BRANCH',     'https://github.com/ffmpegwasm/vorbis.git',   'v1.3.3',        'BSD-3-Clause',              ['COPYING']),
    'zlib':       ('ZLIB_BRANCH',       'https://github.com/ffmpegwasm/zlib.git',     'v1.2.11',       'Zlib',                      ['README']),
    'libwebp':    ('LIBWEBP_BRANCH',    'https://github.com/ffmpegwasm/libwebp.git',  'v1.3.2',        'BSD-3-Clause',              ['COPYING', 'PATENTS']),
    'FreeType':   ('FREETYPE2_BRANCH',  'https://github.com/ffmpegwasm/freetype2.git', 'VER-2-10-4',   'FTL OR GPL-2.0-or-later (hier GPL)', ['docs/LICENSE.TXT', 'docs/GPLv2.TXT', 'docs/FTL.TXT']),
    'FriBidi':    ('FRIBIDI_BRANCH',    'https://github.com/fribidi/fribidi.git',     'v1.0.9',        'LGPL-2.1-or-later',         ['COPYING']),
    'HarfBuzz':   ('HARFBUZZ_BRANCH',   'https://github.com/harfbuzz/harfbuzz.git',   '5.2.0',         'MIT-Modern-Variant',        ['COPYING']),
    'libass':     ('LIBASS_BRANCH',     'https://github.com/libass/libass.git',       '0.15.0',        'ISC',                       ['COPYING']),
    'zimg':       ('ZIMG_BRANCH',       'https://github.com/sekrit-twc/zimg.git',     'release-3.0.5', 'WTFPL',                     ['COPYING']),
}
# Emscripten runtime parts compiled into the core (libc from musl etc.). The compiler itself is not part of
# the corresponding source (GPL-2.0 section 3: major components of the operating system / compiler).
EMSCRIPTEN_NOTICES = {
    'Emscripten': f'https://raw.githubusercontent.com/emscripten-core/emscripten/{EMSCRIPTEN_VERSION}/LICENSE',
    'musl libc (in Emscripten)': f'https://raw.githubusercontent.com/emscripten-core/emscripten/{EMSCRIPTEN_VERSION}/system/lib/libc/musl/COPYRIGHT',
}

ARCHIVE_NAME = f'ffmpeg-core-{CORE_VERSION}-source'


def fail(msg):
    raise SystemExit(f'Abgebrochen: {msg}')


def git(*args, cwd=None):
    return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_core():
    for name, expected in CORE_SHA256.items():
        if sha256(CORE_DIR / name) != expected:
            fail(f'{name} ist nicht @ffmpeg/core {CORE_VERSION}. Bei einer neuen Version CORE_* und SOURCES anpassen.')


def clone(name, url, ref):
    """Shallow clone with submodules, cached in maintenance/build/clones; returns (path, commit)."""
    dest = CLONES / name
    if not dest.exists():
        print(f'  hole {name} ({ref}) …', flush=True)
        git('clone', '--quiet', '--depth', '1', '--branch', ref, '--recurse-submodules', '--shallow-submodules', url, str(dest))
    return dest, git('rev-parse', 'HEAD', cwd=dest)


def check_dockerfile(wasm_dir):
    """The table above has to match the build recipe the core was made with."""
    env = dict(re.findall(r'^ENV (\w+)=(\S+)$', (wasm_dir / 'Dockerfile').read_text(), flags=re.M))
    for name, (var, _, ref, _, _) in SOURCES.items():
        if env.get(var) != ref:
            fail(f'{name}: Dockerfile nennt {var}={env.get(var)}, SOURCES nennt {ref}.')
    if not re.search(rf'FROM emscripten/emsdk:{re.escape(EMSCRIPTEN_VERSION)}\b', (wasm_dir / 'Dockerfile').read_text()):
        fail(f'Dockerfile nutzt nicht Emscripten {EMSCRIPTEN_VERSION}.')


def notice_section(title, license_name, files, seen):
    """files: list of (label, text). Texts already written (tracked in seen: hash -> label) are only referenced."""
    out = [f'{"=" * 78}\n{title}\nLizenz: {license_name}\n{"=" * 78}\n']
    for label, text in files:
        digest = hashlib.sha256(' '.join(text.split()).encode()).hexdigest()   # ignores line breaks and indentation
        if digest in seen:
            out.append(f'--- {label}: wortgleich mit {seen[digest]}, siehe oben\n')
        else:
            seen[digest] = f'{title}, {label}'
            out.append(f'--- {label}\n\n{text.strip()}\n')
    return '\n'.join(out) + '\n\n'


def read_notices(src_dir, name, files):
    result = []
    for rel in files:
        path = src_dir / rel
        if not path.is_file():
            fail(f'{name}: Lizenzdatei {rel} fehlt.')
        result.append((rel, path.read_text(encoding='utf-8', errors='replace')))
    return result


def strip_git(path):
    for p in sorted(path.rglob('.git'), key=lambda p: len(p.parts), reverse=True):
        shutil.rmtree(p) if p.is_dir() else p.unlink()


def tar_filter(info):
    info.uid = info.gid = 0
    info.uname = info.gname = ''
    info.mtime = 0
    return info


def main():
    check_core()
    CLONES.mkdir(parents=True, exist_ok=True)
    stage = BUILD / ARCHIVE_NAME
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir()

    print('Quellen holen:')
    wasm_dir, wasm_commit = clone('ffmpeg.wasm', FFMPEG_WASM['url'], FFMPEG_WASM['ref'])
    if not wasm_commit.startswith(FFMPEG_WASM['commit']):
        fail(f'ffmpeg.wasm {FFMPEG_WASM["ref"]} zeigt auf {wasm_commit}, erwartet {FFMPEG_WASM["commit"]}.')
    check_dockerfile(wasm_dir)

    seen = {}
    rows = [('ffmpeg.wasm', FFMPEG_WASM['url'], FFMPEG_WASM['ref'], wasm_commit, FFMPEG_WASM['license'])]
    notices = [notice_section(f'ffmpeg.wasm ({FFMPEG_WASM["ref"]})', FFMPEG_WASM['license'],
                              read_notices(wasm_dir, 'ffmpeg.wasm', FFMPEG_WASM['notices']), seen)]
    for name, (_, url, ref, license_name, files) in SOURCES.items():
        src, commit = clone(name, url, ref)
        rows.append((name, url, ref, commit, license_name))
        notices.append(notice_section(f'{name} ({ref})', license_name, read_notices(src, name, files), seen))

    emscripten_dir = stage / f'emscripten-{EMSCRIPTEN_VERSION}-lizenzen'
    emscripten_dir.mkdir()
    for title, url in EMSCRIPTEN_NOTICES.items():
        text = urllib.request.urlopen(url, timeout=30).read().decode('utf-8')
        filename = pathlib.Path(url).name
        (emscripten_dir / filename).write_text(text, encoding='utf-8')
        license_name = 'MIT OR NCSA' if title == 'Emscripten' else 'MIT'
        notices.append(notice_section(f'{title} {EMSCRIPTEN_VERSION}', license_name, [(filename, text)], seen))

    quellen = (
        f'Quellen des FFmpeg-Kerns in rauschen-werkzeug/lib/core/\n\n'
        f'Paket: @ffmpeg/core {CORE_VERSION} (dist/esm), unverändert aus npm übernommen\n'
        + ''.join(f'SHA-256 {name}: {digest}\n' for name, digest in CORE_SHA256.items())
        + f'Gebaut mit: Emscripten {EMSCRIPTEN_VERSION} (Docker-Image emscripten/emsdk:{EMSCRIPTEN_VERSION})\n'
        f'Bauanleitung: Dockerfile in ffmpeg.wasm/, siehe dort README und Makefile\n\n'
        + ''.join(f'{name}\n  Quelle: {url}\n  Version: {ref}\n  Commit: {commit}\n  Lizenz: {lic}\n\n'
                  for name, url, ref, commit, lic in rows)
        + 'x264 und LAME sind im Dockerfile nur als Branch angegeben. Der Commit oben ist der Stand beim Erstellen\n'
          'dieses Archivs; die Branches werden seit Jahren nicht mehr verändert.\n'
    )
    header = (
        f'Lizenzhinweise der Bibliotheken im FFmpeg-Kern (@ffmpeg/core {CORE_VERSION})\n\n'
        'Die Datei lib/core/ffmpeg-core.wasm enthält die unten aufgeführten Bibliotheken. Der Kern als Ganzes steht\n'
        'unter der GPL-2.0-or-later. Für die einzelnen Bibliotheken gelten zusätzlich die folgenden Hinweise.\n'
        'Der vollständige Quellcode liegt als Release-Asset ' f'„{ARCHIVE_NAME}.tar.gz“ im Repository dieses Werkzeugs.\n'
        'Erzeugt mit maintenance/build_ffmpeg_sources.py.\n\n'
    )

    (CORE_DIR / 'SOURCES.txt').write_text(quellen, encoding='utf-8')
    (CORE_DIR / 'THIRD-PARTY-NOTICES.txt').write_text(header + ''.join(notices), encoding='utf-8')

    print('Archiv bauen …', flush=True)
    for name, *_ in rows:
        shutil.copytree(CLONES / name, stage / name, symlinks=True, ignore=shutil.ignore_patterns('.git'))
    strip_git(stage)
    (stage / 'SOURCES.txt').write_text(quellen, encoding='utf-8')
    shutil.copy2(CORE_DIR / 'THIRD-PARTY-NOTICES.txt', stage / 'THIRD-PARTY-NOTICES.txt')
    archive = BUILD / f'{ARCHIVE_NAME}.tar.gz'
    with tarfile.open(archive, 'w:gz') as tar:
        tar.add(stage, arcname=ARCHIVE_NAME, filter=tar_filter)
    shutil.rmtree(stage)
    print(f'{archive.relative_to(ROOT)}: {archive.stat().st_size / 2**20:.0f} MiB')
    print('Aktualisiert: rauschen-werkzeug/lib/core/SOURCES.txt, rauschen-werkzeug/lib/core/THIRD-PARTY-NOTICES.txt')


if __name__ == '__main__':
    main()
