# Rauschen-Werkzeug

Setzt vor Audio- und Videodateien (MP3, WAV, M4A, MP4, MOV) eine Sekunde unhörbar leises Rauschen. So verschlucken USB-C-Adapter mit eigenem Audio-Chip den Anfang nicht mehr. Die Bearbeitung läuft vollständig im Browser: Es wird nichts hochgeladen, und es werden keine externen Dienste aufgerufen.

## Benutzen

**Am einfachsten:** Unter [Releases](../../releases) die Datei `audio-noise-generator-offline.html` herunterladen und per Doppelklick öffnen. Sie funktioniert ohne Installation und ohne Internet.

**Alternativ aus dem Repository:** Repository herunterladen, im Ordner `rauschen-werkzeug/` einen lokalen Webserver starten und `http://localhost:8000` öffnen. Per Doppelklick auf `index.html` funktioniert diese Fassung nicht.

```bash
python3 -m http.server 8000 -d rauschen-werkzeug
```

Die Bedienung erklärt [HELP.md](rauschen-werkzeug/HELP.md), im Werkzeug über den Knopf „Hilfe“.

## Aufbau

| Ordner | Inhalt |
|---|---|
| `rauschen-werkzeug/` | das Werkzeug selbst, nur statische Dateien. [README](rauschen-werkzeug/README.md), [Architektur](rauschen-werkzeug/ARCHITECTURE.md), [Lizenzen](rauschen-werkzeug/LICENSES.md) |
| `rauschen-werkzeug/lib/` | mitgelieferte Bibliotheken anderer Projekte, unverändert |
| `maintenance/` | Skripte für Hilfeseite, Offline-Fassung und FFmpeg-Quellcode ([Offline-Fassung](rauschen-werkzeug/ARCHITECTURE.md#offline-fassung)), Anleitung für neue Versionen ([RELEASING](maintenance/RELEASING.md)) |

## Lizenz

Der eigene Code steht unter der **MIT-Lizenz** ([LICENSE](LICENSE)).

**Ausgenommen ist `rauschen-werkzeug/lib/`.** Die dortigen Bibliotheken behalten ihre eigenen Lizenzen:

| Bestandteil | Lizenz |
|---|---|
| FFmpeg-Kern (`lib/core/`, ffmpeg.wasm `@ffmpeg/core` 0.12.10) | **GPL-2.0-or-later**, enthaltene Bibliotheken siehe [THIRD-PARTY-NOTICES.txt](rauschen-werkzeug/lib/core/THIRD-PARTY-NOTICES.txt) |
| Schrift Atkinson Hyperlegible (`lib/fonts/`) | SIL Open Font License 1.1 |

Die Details stehen in [LICENSES.md](rauschen-werkzeug/LICENSES.md).

**Quellcode des FFmpeg-Kerns:** Den vollständigen Quellcode des Kerns und aller darin enthaltenen Bibliotheken gibt es unter [Releases](../../releases) als `ffmpeg-core-0.12.10-source.tar.gz`. Die genauen Versionen und Commits stehen in [SOURCES.txt](rauschen-werkzeug/lib/core/SOURCES.txt).

**Weitergabe:** Die Offline-Fassung und der Ordner `rauschen-werkzeug/` enthalten den GPL-lizenzierten FFmpeg-Kern. Wer sie weitergibt, muss die Bedingungen der GPL-2.0 einhalten, also vor allem die Lizenztexte mitgeben und auf den Quellcode verweisen. Der eigene Code bleibt dabei MIT-lizenziert und kann einzeln unter MIT verwendet werden.
