# Veröffentlichen

Das Werkzeug wird über GitHub-Releases verteilt. Die Offline-Datei und das Quellcode-Archiv entstehen in `maintenance/build/`. Sie werden nie committet, sondern nur als Release-Assets hochgeladen.

## Vor der ersten Veröffentlichung

- Repository `audio-noise-generator` in der Organisation `iqb-berlin` anlegen, wie die anderen Werkzeuge des IQB (z. B. `base64-generator`). Urheber ist wie dort das „Institute for Educational Quality Improvement (IQB)“ (`LICENSE`, `rauschen-werkzeug/LICENSE.txt`).
- Bei der Freigabe erwähnen, dass anders als beim base64-generator fremder GPL-Code mitgeliefert wird: der eigene Code steht unter MIT, der FFmpeg-Kern unter GPL-2.0-or-later, sein Quellcode liegt als Release bei.
- Mit der dienstlichen Adresse committen.

## Einmalig: Quellcode des FFmpeg-Kerns

Die GPL verlangt, dass der Quellcode am selben Ort angeboten wird wie der Kern.

1. `python3 maintenance/build_ffmpeg_sources.py` ausführen. Das Skript erzeugt `maintenance/build/ffmpeg-core-0.12.10-source.tar.gz` (ca. 72 MB).
2. Auf GitHub ein Release anlegen: Tag `ffmpeg-core-0.12.10-source`, Titel „Quellcode FFmpeg-Kern 0.12.10“, das Archiv als Asset hochladen, Text siehe unten.
3. Dieses Release nicht löschen, solange irgendein Release des Werkzeugs herunterladbar ist. Beim Aufräumen immer zuerst die Werkzeug-Releases löschen.

## Bei jeder neuen Version

1. Falls `HELP.md` geändert wurde: `python3 maintenance/build_help.py`
2. Offline-Fassung bauen: `python3 maintenance/build_offline.py`
3. Offline-Fassung kurz ausprobieren: per Doppelklick öffnen, eine Datei bearbeiten, unter „Datenschutz und Lizenzen“ die Texte aufklappen.
4. Änderungen committen und einen Tag setzen, z. B. `v1.1`. Der Tag ist der Quellcode der Offline-Fassung, einschließlich `maintenance/build_offline.py`.
5. Auf GitHub ein Release zum Tag anlegen, `maintenance/build/audio-noise-generator-offline.html` als Asset hochladen, Text siehe unten.

## Wenn sich der FFmpeg-Kern ändert

Wird `rauschen-werkzeug/lib/core/` durch eine andere Version ersetzt:

1. In `maintenance/build_ffmpeg_sources.py` `CORE_VERSION`, `CORE_SHA256`, `FFMPEG_WASM` und `SOURCES` anpassen. Das Skript bricht ab, solange etwas nicht zum Dockerfile von ffmpeg.wasm passt.
2. Skript ausführen und ein neues Quellcode-Release anlegen. Das alte bleibt, solange ältere Werkzeug-Releases es brauchen.
3. Versionsangaben in `index.html` (Abschnitt „Datenschutz und Lizenzen“), `LICENSES.md` und `README.md` anpassen.

## Vorlagen für Release-Texte

**Werkzeug-Release:**

> Rauschen-Werkzeug vX.Y
>
> `audio-noise-generator-offline.html` herunterladen und per Doppelklick öffnen. Funktioniert ohne Installation und ohne Internet, die Dateien werden nur im Browser bearbeitet.
>
> Änderungen: …
>
> Lizenz: Der eigene Code steht unter MIT. Die Datei enthält den FFmpeg-Kern (ffmpeg.wasm `@ffmpeg/core` 0.12.10) unter der GPL-2.0-or-later sowie weitere Bibliotheken. Für die Datei als Ganzes gilt bei der Weitergabe deshalb die GPL-2.0. Alle Lizenztexte und Hinweise stehen in der Datei unter „Datenschutz und Lizenzen“. Den vollständigen Quellcode des Kerns gibt es im Release „Quellcode FFmpeg-Kern 0.12.10“, den Quellcode des Werkzeugs unter diesem Tag.

**Quellcode-Release:**

> Quellcode FFmpeg-Kern 0.12.10
>
> Vollständiger Quellcode des FFmpeg-Kerns, der im Rauschen-Werkzeug unter `rauschen-werkzeug/lib/core/` mitgeliefert wird (ffmpeg.wasm `@ffmpeg/core` 0.12.10, FFmpeg 5.1.4 und alle eingebauten Bibliotheken), bereitgestellt nach Abschnitt 3 der GPL-2.0. Inhalt und genaue Versionen: `SOURCES.txt` im Archiv.
