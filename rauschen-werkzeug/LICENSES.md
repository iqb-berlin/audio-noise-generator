# Lizenzen

Das Werkzeug besteht aus eigenem Code und mitgelieferten Bibliotheken anderer Projekte. Für jeden Teil gilt seine eigene Lizenz. Die vollständigen Lizenztexte liegen in den genannten Dateien.

## Eigener Code: MIT

`index.html`, `engine.js`, `engine-worker.js`, `zip.js`, `help.html`, `HELP.md`, `README.md`, `ARCHITECTURE.md`, `LICENSES.md` und die Skripte in `maintenance/` stehen unter der MIT-Lizenz, siehe `LICENSE.txt`. Die MIT-Lizenz gilt nicht für die Dateien unter `lib/`, für die gelten die Lizenzen unten.

## Mitgelieferte Bibliotheken

| Bestandteil | Dateien | Lizenz | Lizenztext |
|---|---|---|---|
| FFmpeg-Kern (ffmpeg.wasm, `@ffmpeg/core` 0.12.10 mit FFmpeg 5.1.4) | `lib/core/` | GPL-2.0-or-later | `lib/core/LICENSE-GPL-2.0.txt`, Hinweise aller Bibliotheken in `lib/core/THIRD-PARTY-NOTICES.txt` |
| Atkinson Hyperlegible, Copyright 2020 Braille Institute of America, Inc. | `lib/fonts/` | SIL Open Font License 1.1 | `lib/fonts/LICENSE.txt` |

### Was im FFmpeg-Kern steckt

`lib/core/` enthält unverändert `@ffmpeg/core` 0.12.10 aus npm (die ESM-Fassung, identisch mit 0.12.9). FFmpeg wurde mit `--enable-gpl` und den folgenden Bibliotheken gebaut und mit Emscripten 3.1.40 übersetzt. Deshalb steht der Kern als Ganzes unter der GPL-2.0-or-later.

| Bibliothek | Version | Lizenz |
|---|---|---|
| FFmpeg | 5.1.4 | LGPL-2.1-or-later, durch `--enable-gpl` als Ganzes GPL-2.0-or-later |
| x264 (H.264-Encoder) | Branch `4-cores` | GPL-2.0-or-later |
| x265 (H.265-Encoder) | 3.4 | GPL-2.0-or-later |
| LAME (MP3-Encoder) | Branch `master` | LGPL-2.0-or-later |
| FriBidi | 1.0.9 | LGPL-2.1-or-later |
| FreeType | 2.10.4 | FreeType License oder GPL-2.0 (hier: GPL-2.0) |
| libvpx, libogg, libtheora, libvorbis, Opus, libwebp | 1.13.1, 1.3.4, 1.1.1, 1.3.3, 1.3.1, 1.3.2 | BSD-3-Clause |
| HarfBuzz | 5.2.0 | MIT (alte Fassung) |
| libass | 0.15.0 | ISC |
| zlib | 1.2.11 | zlib-Lizenz |
| zimg | 3.0.5 | WTFPL |
| Laufzeitbibliotheken von Emscripten, darunter musl libc | 3.1.40 | MIT bzw. MIT oder NCSA |

- `lib/core/LICENSE-GPL-2.0.txt` und `lib/core/LICENSE-LGPL-2.1.txt`: die Lizenztexte der GPL und LGPL
- `lib/core/THIRD-PARTY-NOTICES.txt`: Urheberhinweise und Lizenztexte jeder einzelnen Bibliothek, wie sie die BSD-, MIT- und ISC-Lizenzen bei der Weitergabe verlangen
- `lib/core/SOURCES.txt`: genaue Quellen, Commits und SHA-256-Prüfsummen

Diese drei Dateien erzeugt `maintenance/build_ffmpeg_sources.py`.

## Quellcode des FFmpeg-Kerns

Nach der GPL-2.0 muss, wer den Kern weitergibt, den vollständigen Quellcode am selben Ort anbieten. Dafür liegt im Repository dieses Werkzeugs dauerhaft ein Release „Quellcode FFmpeg-Kern 0.12.10“ mit dem Archiv `ffmpeg-core-0.12.10-source.tar.gz`. Es enthält:

- ffmpeg.wasm am Commit, aus dem `@ffmpeg/core` 0.12.10 veröffentlicht wurde, mit Dockerfile und Build-Skripten
- den Quellcode von FFmpeg und jeder Bibliothek oben, in genau der verwendeten Version
- `SOURCES.txt` und `THIRD-PARTY-NOTICES.txt`

Das Archiv muss erreichbar bleiben, solange irgendeine Fassung des Werkzeugs zum Herunterladen angeboten wird. Ersatzweise ist der Quellcode auch bei den Projekten selbst zu finden, etwa unter https://github.com/ffmpegwasm/ffmpeg.wasm.

## Offline-Fassung

Die Offline-Fassung (`maintenance/build_offline.py`) bettet den Kern in eine einzige HTML-Datei ein. Dafür wird `ffmpeg-core.js` leicht verändert: `import.meta.url` und der `export` werden ersetzt, damit der Kern als klassischer Hintergrundprozess läuft. Die Datei `ffmpeg-core.wasm` bleibt unverändert. Wie es die GPL verlangt, steht ein Hinweis auf diese Änderung mit Datum direkt im eingebetteten Code. Alle Lizenztexte und Hinweise sind in der Datei unter „Datenschutz und Lizenzen“ enthalten. Der Quellcode der Offline-Fassung ist dieses Repository am Tag des jeweiligen Releases.

## Patente

Die Patente für MP3 sind abgelaufen. Für H.264, H.265 und AAC gibt es Patentpools. Bei kostenloser, nicht kommerzieller Nutzung spielen sie in der Praxis keine Rolle. Das ist kein Rechtsrat.
