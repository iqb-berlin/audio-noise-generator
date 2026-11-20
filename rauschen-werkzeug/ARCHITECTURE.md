# Aufbau des Rauschen-Werkzeugs

Diese Datei erklärt, wie das Werkzeug technisch aufgebaut ist: wie es gestartet wird, was im Browser passiert und wo im Code was steht. Für die Bedienung siehe `README.md` und `HELP.md`.

## Auf einen Blick

Das Werkzeug ist eine einzelne Webseite ohne Backend. Es gibt keinen Server, der rechnet, keine Datenbank und keine Anmeldung. Die gesamte Bearbeitung läuft im Browser der Person, die die Seite öffnet:

- **FFmpeg als WebAssembly** (ffmpeg.wasm) liest die Datei, mischt das Rauschen hinein, encodiert neu und prüft das Ergebnis.
- **Die Seite selbst** (`index.html`) enthält Oberfläche, Styles und die gesamte Ablaufsteuerung.
- **`engine.js`** startet FFmpeg in einem Hintergrundprozess (`engine-worker.js`) und reicht Befehle und Dateien hin und her.
- **`zip.js`** packt auf Wunsch alle Ergebnisse in eine ZIP-Datei.

Dateien verlassen dabei nie den Rechner. Die Seite ruft auch keine externen Dienste auf, Schriften und Bibliotheken liegen alle in diesem Ordner.

```
 lokaler Webserver (nur statische Dateien) oder Offline-Datei
 └── rauschen-werkzeug/
       │  einmal laden, danach aus dem Browser-Cache
       ▼
 Browser
 ├── Hauptseite (index.html, engine.js, zip.js)
 │     Oberfläche · Einstellungen · Warteschlange · Player · Speichern
 │        │  Datei als Bytes hinein, Ergebnis als Bytes zurück
 │        ▼
 └── Hintergrundprozess (Web Worker, engine-worker.js)
          └── FFmpeg-Kern (lib/core/ffmpeg-core.wasm, ca. 32 MB)
                virtuelles Dateisystem im Arbeitsspeicher
```

## Starten

Das Werkzeug läuft nur lokal, auf dem Rechner der Person, die es benutzt. Es gibt zwei Fassungen:

- **Offline-Fassung:** eine einzige HTML-Datei, per Doppelklick. Das ist der Normalfall, siehe „Offline-Fassung“ unten.
- **Dieser Ordner:** braucht einen lokalen Webserver, z. B. `python3 -m http.server 8000`. Die Seite lädt ihre Programmteile als JavaScript-Module und startet einen Hintergrundprozess (Web Worker). Beides blockieren Browser bei Dateien, die direkt per `file://` geöffnet werden. Per Doppelklick geöffnet würde die Seite zwar normal aussehen, aber auf nichts reagieren. Für diesen Fall gibt es ein kleines eigenes Skript vor dem Hauptskript, das auch unter `file://` läuft und einen deutlichen Hinweis anzeigt. Der Kern ist die einfädige Variante und braucht keine besonderen Header (kein `SharedArrayBuffer`, kein COOP/COEP).

### Laden und Cache

Beim ersten Bearbeiten lädt der Browser `ffmpeg-core.wasm` (ca. 32 MB). Danach kommt der Kern aus dem Browser-Cache. Ein Neustart des Programms dauert dann nur Sekundenbruchteile, was das Werkzeug ausnutzt (siehe „Ein frisches FFmpeg pro Datei“).

## Dateien im Ordner

| Datei | Größe | Aufgabe |
|---|---|---|
| `index.html` | ca. 50 KB | Styles, Markup und Ablaufsteuerung |
| `engine.js` | ca. 3 KB | Klasse `FFmpeg`: übersetzt den Kern einmal, startet pro Datei einen Hintergrundprozess, schickt Befehle und Dateien |
| `engine-worker.js` | ca. 2 KB | der Hintergrundprozess: lädt den Kern und führt die Befehle aus |
| `zip.js` | ca. 3 KB | `zipStore`: schreibt „Alle speichern“ als ZIP-Datei, ohne erneute Kompression |
| `README.md` | | Bedienung, Einrichtung, Lizenzen |
| `HELP.md` | | Hilfe für Nutzer: alle Bedienelemente, Meldungen, häufige Fragen. Quelle der Hilfeseite. |
| `help.html` | ca. 33 KB | Hilfeseite mit mitlaufendem Inhaltsverzeichnis, erzeugt aus `HELP.md` |
| `ARCHITECTURE.md` | | diese Datei |
| `LICENSES.md`, `LICENSE.txt` | | Lizenzübersicht und MIT-Lizenz des eigenen Codes |
| `lib/core/ffmpeg-core.js` | ca. 110 KB | Lader des FFmpeg-Kerns (Emscripten), `@ffmpeg/core` 0.12.10 |
| `lib/core/ffmpeg-core.wasm` | ca. 32 MB | FFmpeg selbst, mit x264 (H.264), LAME (MP3) und AAC |
| `lib/fonts/*.woff2` | je ca. 17 KB | Schrift Atkinson Hyperlegible (normal und fett) |
| `lib/core/LICENSE-*.txt`, `lib/fonts/LICENSE.txt` | | Lizenztexte der Bibliotheken |
| `lib/core/THIRD-PARTY-NOTICES.txt`, `lib/core/SOURCES.txt` | | Hinweise aller Bibliotheken im Kern, genaue Quellen und Prüfsummen. Erzeugt von `maintenance/build_ffmpeg_sources.py` |

## Aufbau von `index.html`

Die Datei besteht aus vier Teilen, in dieser Reihenfolge:

1. **Styles** (`<style>`). Farben und Linien sind als Variablen auf `:root` definiert (`--bg`, `--primary`, `--added`, `--content` usw.) und für den dunklen Modus noch einmal überschrieben. Danach folgen die Bausteine: Einstellungskarte, Ablagefeld, Dateiliste mit aufklappbaren Zeilen, Player und Knöpfe.
2. **Markup** (`<main>`). Kopf, Einstellungskarte (Vorlauf, Rauschpegel, „Auch unter den Ton legen“, Zusatz im Dateinamen, Ausgabeformat mit MP3-Einstellungen), Ablagefeld, Dateiliste mit Kopfzeile und zum Schluss „Was genau passiert“. Die Dateizeilen erzeugt erst das Skript.
3. **`file://`-Prüfung** (ein einfaches `<script>`). Zeigt den Hinweis an und sperrt das Auswahlfeld, wenn die Seite nicht über einen Webserver geöffnet wurde.
4. **Hauptskript** (`<script type="module">`), gegliedert in Abschnitte mit Trennkommentaren:

| Abschnitt | Wichtige Funktionen | Aufgabe |
|---|---|---|
| ffmpeg | `freshEngine`, `stopEngine`, `run` | FFmpeg starten, abbrechen, Befehle ausführen und deren Log mitschneiden |
| Analyse | `probeInfo`, `target`, `audioArgs`, `audioGraph`, `calibrate`, `verify` | Datei untersuchen, Ausgabeformat bestimmen, Encoder-Einstellungen wählen, Filter bauen, Pegel abstimmen, Ergebnis prüfen |
| Bearbeitung | `processEntry` | Der Ablauf für eine einzelne Datei |
| Anzeige | `makeRow`, `drawWave` | Dateizeile mit Status, Wellenform, Player und Knöpfen |
| Ablauf | `settings`, `outSettings`, `forEntry`, `updateCodecPanel`, `enqueue`, `addFiles`, `updateBatch`, `updateRedo`, `savedName`, `saveFile` | Einstellungen lesen, Warteschlange, Fortschritt, Wiederholen, Speichern |

## Ablauf einer Datei

```
Datei ausgewählt oder hineingezogen
  │
  ▼
addFiles ── Endung nicht unterstützt? ──► Zeile mit Fehlermeldung, fertig
  │
  ▼
enqueue ── reiht die Datei mit den aktuellen Einstellungen in die Warteschlange
  │         (die Dateien laufen nacheinander, nie gleichzeitig)
  ▼
processEntry
  1. freshEngine        neues FFmpeg starten
  2. writeFile          Datei ins virtuelle Dateisystem des FFmpeg kopieren
  3. probeInfo          Dauer, Tonspur (Codec, Abtastrate, Kanäle, Bitrate), Bild, Kommentar
       ├─ keine Tonspur             ──► Fehlermeldung
       ├─ Markierung im Kommentar   ──► „Bereits bearbeitet“, Datei bleibt unverändert
       └─ Video ohne Bild           ──► Fehlermeldung
     target             Ausgabeformat: wie das Original oder MP3 mit den gewählten Einstellungen
  4. calibrate          Pegelausgleich für den Encoder bestimmen
  5. Hauptbefehl        Rauschen hineinmischen, neu encodieren, Markierung setzen
  6. verify             Ergebnis nachmessen
  7. readFile           Ergebnis als Blob übernehmen
  │
  ▼
ui.done ── Status, Wellenform, Player, Speichern-Knöpfe
```

### Schritt 4: Pegel abstimmen (`calibrate`)

MP3- und AAC-Encoder werfen sehr leise Anteile teilweise weg. Deshalb wird vorab eine 2 Sekunden lange Rauschprobe mit genau den Encoder-Einstellungen der Datei kodiert und ihr Pegel gemessen. Fehlt etwas, wird die Amplitude um bis zu 8 dB angehoben. Bei WAV entfällt der Schritt. Das Ergebnis hängt nur von Format, Abtastrate, Kanalzahl, Bitrate und Pegel ab und wird deshalb je Kombination nur einmal gemessen (`calibrated`).

### Schritt 5: der Filtergraph (`audioGraph`)

Für die Tonspur baut das Werkzeug diesen FFmpeg-Filtergraphen:

```
[Original] ─ auf Abtastrate und Kanallayout bringen ─────────────────► [src]
anoisesrc (weißes Rauschen, Länge = Vorlauf) ─ mono → Layout ────────► [pre]
anoisesrc (weißes Rauschen, 0,1 s)           ─ mono → Layout ────────► [tail]
anoisesrc (endlos) ─► amix mit [src]   (nur mit „Auch unter den Ton legen“)  ► [body]

[pre] + [body] + [tail]  ── concat ──►  [aout]
```

- Das Rauschen ist weißes Rauschen mit gleichverteilten Abtastwerten. Es wird einkanalig erzeugt und bei Stereo auf beide Kanäle kopiert.
- Der eingestellte Pegel ist der Spitzenpegel. Der mittlere Pegel (RMS) liegt rechnerisch 4,8 dB darunter, bei −70 dBFS also bei etwa −75 dB.
- Mit „Kein Rauschen, nur Stille“ sind Vor- und Nachlauf digitale Stille (`anullsrc`), und es wird kein Rauschen unterlegt. Pegelabstimmung und Prüfung entfallen dann, die Markierung lautet `rauschen-werkzeug 1000ms stille`.
- Bei einem Vorlauf von 0 s fällt `[pre]` weg, und `concat` verbindet nur `[body]` und `[tail]`. `anoisesrc` mit der Länge 0 würde endlos laufen.
- Bei Videos wird zusätzlich das erste Bild für die Dauer des Vorlaufs festgehalten (`tpad=…:start_mode=clone`), damit Bild und Ton synchron bleiben. Das Bild wird dafür als H.264 neu encodiert (`-crf 20`, `-preset veryfast`). Bei einem Vorlauf von 0 s wird kein Bild festgehalten (`null`), neu encodiert wird trotzdem.

### Schritt 6: Prüfung (`verify`)

Zwei Messungen an der fertigen Datei:

1. Der mittlere Pegel im Vorlauf, gemessen ab 0,1 s. Liegt er mehr als 8 dB unter dem eingestellten Wert, steht in der Zeile „Vorlauf zu leise“. Bei einem Vorlauf unter 0,2 s gibt es nichts zu messen, die Messung entfällt.
2. Stille Stellen ohne Rauschen, die länger als 0,2 s sind (`silencedetect`). Gibt es welche, erscheint ein Hinweis, und die Zeile klappt automatisch auf.

### Markierung

Jede bearbeitete Datei bekommt im Kommentarfeld der Metadaten einen Eintrag wie `rauschen-werkzeug 1000ms -70dBFS`. Findet das Werkzeug diese Markierung in einer Datei, überspringt es sie. Geprüft wird nur der Anfang (`MARKER`), deshalb zählt auch die stille Variante. Das Skript `rauschen_werkzeug.py` schreibt dieselbe Markierung und erkennt sie ebenfalls. Deshalb überspringen Werkzeug und Skript gegenseitig ihre Dateien. Das Python-Skript ist ein eigenständiges Werkzeug und nicht Teil dieses Repositorys.

## Warteschlange und Zustände

Jede Datei ist intern ein Eintrag in `entries` mit diesen Feldern:

| Feld | Bedeutung |
|---|---|
| `file`, `ext` | die ausgewählte Datei und ihre Endung |
| `s` | die Einstellungen, mit denen sie bearbeitet wird oder wurde |
| `pending` | wartet in der Warteschlange |
| `running` | wird gerade bearbeitet |
| `result` | das fertige Ergebnis als Blob, sonst `null` |
| `ui` | Zugriff auf die Zeile: `status`, `progress`, `reset`, `done`, `openWhenDone` |

Die Warteschlange ist eine einfache Promise-Kette (`queue`). Daraus ergibt sich:

- **Gesamtfortschritt:** `updateBatch` zählt, wie viele Einträge noch `pending` oder `running` sind, und zeigt oben „x von y fertig“ mit Spinner.
- **Wiederholen:** `updateRedo` vergleicht bei jeder Änderung die aktuellen Einstellungen mit `s` jedes Eintrags. Weicht einer ab, erscheint „Mit neuen Einstellungen wiederholen“. Wartende Dateien übernehmen die neuen Werte einfach, fertige werden zurückgesetzt und neu eingereiht. Eine Datei, die gerade läuft, wird zu Ende bearbeitet und kommt danach noch einmal dran.
- **Liste leeren:** bricht eine laufende Bearbeitung mit `stopEngine` sofort ab. Wartende Einträge erkennt die Warteschlange als entfernt und überspringt sie.

## Ein frisches FFmpeg pro Datei

ffmpeg.wasm gibt nach jedem Befehl nicht allen Speicher wieder frei. Nach rund 150 bis 260 Befehlen stürzt es mit „memory access out of bounds“ ab, bei aufwendigen Befehlen früher. Pro Datei laufen 4 bis 6 Befehle, ein Stapel von 30 Dateien hat das zuverlässig ausgelöst.

Deshalb startet `freshEngine` für jede Datei ein neues FFmpeg und beendet das alte. Weil der Kern im Browser-Cache liegt, kostet das nur etwa 0,1 Sekunden. Nebeneffekt: Stürzt FFmpeg bei einer einzelnen Datei doch einmal ab, etwa bei einem sehr großen Video, betrifft das nur diese Datei.

## Einstellungen und Eingaben

- **Vorlauf und Rauschpegel** sind bewusst Textfelder, keine Zahlenfelder (`type="number"`). Firefox und Chrome verwerfen in Zahlenfeldern je nach Sprache das Dezimalkomma. `readNum` akzeptiert Komma und Punkt. Grenzen, Schrittweite und Voreinstellung stehen in `NUM`: Vorlauf 0–5 s in Schritten von 0,25, voreingestellt 1 s. Rauschpegel −90 bis −40 dBFS in Schritten von 5, voreingestellt −70.
- **−/+ und Pfeiltasten** ändern die Werte schrittweise (`stepNum`). Ungültige Eingaben bekommen einen roten Rahmen, gerechnet wird dann mit der Voreinstellung.
- **Zusatz im Dateinamen** betrifft nur das Speichern (`savedName`). Er steht vor der Endung, unzulässige Zeichen fallen weg. Der Browser merkt ihn sich in `localStorage`. Ist der Speicher gesperrt, funktioniert alles weiter, nur ohne Merken.

## Anzeige

- **Dateizeile** (`makeRow`): ein Knopf zum Auf- und Zuklappen mit Name, Größe und Status. Darunter ein dünner Fortschrittsbalken während der Bearbeitung. Aufgeklappt folgen gegebenenfalls das Video, die Wellenform, Hinweise aus der Prüfung, der Player und die Knöpfe.
- **Wellenform** (`drawWave`): Das Ergebnis wird mit der Web Audio API dekodiert und als Balken auf eine Canvas gezeichnet. Die Höhe ist logarithmisch von −90 bis 0 dB, damit auch das leise Rauschen sichtbar ist. Der Vorlauf ist ockerfarben, der ursprüngliche Ton petrol.
- **Player:** eigene Steuerung über ein `<audio>`- bzw. `<video>`-Element. Es läuft immer nur ein Stück gleichzeitig. Kann der Browser eine Vorschau nicht abspielen, steht ein Hinweis da, die Datei selbst ist trotzdem fertig.

## Speichern

- **Diese Datei speichern:** lädt das Ergebnis mit dem Originalnamen herunter, gegebenenfalls mit Zusatz.
- **Alle speichern:** packt alle fertigen Dateien mit `zipStore` (`zip.js`) in `rauschen-werkzeug.zip`. Die Dateien werden nur gespeichert, nicht noch einmal komprimiert, weil Audio und Video schon komprimiert sind. Gleiche Namen bekommen einen Zusatz wie `Aufgabe (2).mp3` (`uniqueNames`), sonst würden sie sich beim Entpacken überschreiben. Grenze: 4 GB für das ganze Archiv.
- **Als data-URI kopieren:** wandelt das Ergebnis in eine `data:`-Adresse um und legt sie in die Zwischenablage. Geht das nicht, wird sie stattdessen als Textdatei gespeichert.

Mit dem Ausgabeformat „Wie Original“ bleiben Endung und Containerformat gleich. Neu kodiert wird trotzdem: MP3 als MP3, WAV immer als 16 Bit, M4A und der Ton in Videos als AAC, Videobild als H.264.

### Ausgabeformat MP3

Mit „MP3“ bestimmt `target` für Audiodateien statt des Originalformats die Endung `mp3` und die Zielwerte (Abtastrate, Kanäle, Bitrate bzw. VBR-Qualität). Videos sind ausgenommen: `forEntry` setzt für sie das Ausgabeformat auf „Wie Original“, damit eine Änderung bei ihnen auch kein Wiederholen auslöst. Werte auf „Wie Original“ stehen in `s.out` als `null` und werden aus der Quelle übernommen: Abtastraten über 48 kHz auf die nächstniedrigere MP3-Rate, Bitrate wie bei MP3-Quellen über `snapKbps`. Eine gewählte Bitrate rundet `fitKbps` auf die nächste erlaubte, unter 32 kHz höchstens 160 kb/s. CBR wird als `-b:a`, VBR als `-q:a 0–9` an LAME übergeben. Die Umrechnung von Abtastrate und Kanälen übernimmt der Filtergraph (`aresample`, `aformat`), Pegelabstimmung und Prüfung laufen mit den Zielwerten. `entry.resultExt` hält die Endung des Ergebnisses, `savedName` tauscht damit beim Speichern die Endung aus.

## Wo man was ändert

| Was | Wo |
|---|---|
| Voreinstellungen, Grenzen, Schrittweiten | `NUM` im Abschnitt „Ablauf“ |
| Erlaubte Formate | `AUDIO_EXT`, `VIDEO_EXT` und `MIME` oben im Hauptskript, dazu das `accept`-Attribut am Auswahlfeld |
| Encoder und Bitraten | `audioArgs`, `snapKbps`, `fitKbps`, für MP3-Ausgabe `target` und die Auswahllisten im `#mp3-panel` |
| Art und Länge des Rauschens, Nachlauf | `audioGraph` |
| Videoqualität | Hauptbefehl in `processEntry` (`-crf`, `-preset`) |
| Prüfschwellen | `verify` und der Hinweis zu stillen Stellen in `makeRow` |
| Markierung | `MARKER` |
| Farben, Abstände, dunkler Modus | Variablen auf `:root` am Anfang der Styles |
| Texte der Oberfläche | Markup in `<main>` und die Statustexte in `processEntry` |
| Hilfe | nur in `HELP.md` ändern, dann `python3 maintenance/build_help.py` ausführen. Das Skript erzeugt daraus `help.html` und übernimmt Schriften und Farben aus `index.html`. |
| Offline-Fassung | `maintenance/build_offline.py`. Nach jeder Änderung an `index.html` oder `help.html` neu bauen, siehe „Offline-Fassung“ |

## Offline-Fassung

`maintenance/build_offline.py` erzeugt aus diesem Ordner die Datei `maintenance/build/audio-noise-generator-offline.html`: das komplette Werkzeug in **einer einzigen Datei**, die per Doppelklick funktioniert, ohne Webserver und ohne Internet. Sie wird nicht committet, sondern als Release verteilt (siehe `maintenance/RELEASING.md`) und lässt sich auch per Stick, Netzlaufwerk oder Cloud-Link weitergeben.

```
python3 maintenance/build_offline.py
```

Vorher gegebenenfalls `python3 maintenance/build_help.py` ausführen, falls sich `HELP.md` geändert hat. Ändert sich `index.html` an einer Stelle, auf die das Skript angewiesen ist, bricht es mit einer Meldung ab, statt eine kaputte Datei zu bauen.

### Wie sie unter `file://` funktioniert

Browser blockieren bei lokal geöffneten Dateien das Nachladen von Modulen, Hintergrundprozessen und der `.wasm`-Datei. Die Offline-Fassung lädt deshalb nichts nach. Das Skript bettet alles ein:

- **Schriften** als data-URI und **`engine.js` und `zip.js`** direkt im Hauptskript. In `engine.js` ersetzt das Skript den Block `<loaders>`: Hintergrundprozess und Kern kommen dann aus der Seite statt aus Dateien.
- **Den FFmpeg-Kern** als Base64 (aus 32 MB werden ca. 43 MB). Er wird einmal übersetzt, und jeder neue Hintergrundprozess bekommt dieses fertige WebAssembly-Modul direkt übergeben, ohne Abruf einer Datei.
- **Den Hintergrundprozess** als Text aus `ffmpeg-core.js` und `engine-worker.js`, der per Blob-URL als klassischer Worker ohne Module startet. Dafür wird `ffmpeg-core.js` leicht verändert (`import.meta.url` ersetzt, `export` entfernt). Wie es die GPL verlangt, steht ein Änderungsvermerk mit Datum im eingebetteten Code.
- **Die Hilfeseite.** Der Knopf „Hilfe“ öffnet sie als ganzseitige Ebene über dem Werkzeug. „Zurück zum Werkzeug“ und der Zurück-Knopf des Browsers schließen sie wieder. Anders als online wird nicht die Seite gewechselt, weil Chrome und Edge lokal geöffnete Seiten beim Zurückgehen neu laden und die Dateiliste dann verloren wäre.
- **Alle Lizenztexte und Hinweise**, aufklappbar unter „Datenschutz und Lizenzen“. Die Datei kann deshalb allein weitergegeben werden.

Außerdem entfernt das Skript die Sperre für `file://`. Die Bearbeitung selbst (`index.html`, Abschnitte Analyse bis Ablauf) ist unverändert.

### Getestet

Unter `file://`, jeweils ohne Fenster (headless):

| | Chromium 155 (Linux) | Firefox 158 (Linux) | Chrome (macOS) |
|---|---|---|---|
| Seite öffnen, keine Fehlermeldung | ✓ | ✓ | ✓ |
| WAV, MP3, M4A und MP4 bearbeiten | ✓ | ✓ | nur WAV getestet |
| Abspielen | ✓ | ✓ | nicht getestet |
| Einzeln speichern mit Zusatz im Dateinamen | ✓ | ✓ | nicht getestet |
| „Alle speichern“ als ZIP | ✓ | ✓ | nicht getestet |
| Zusatz nach Neuladen noch da | ✓ | ✓ | nicht getestet |
| 31 Dateien am Stück | ✓, ca. 4 s | nicht getestet | nicht getestet |

Vom Öffnen bis zum ersten Bearbeitungsschritt vergingen etwa 0,3 s.

**Nicht getestet:** Edge (nutzt dieselbe Technik wie Chromium und sollte sich gleich verhalten), Windows allgemein, Öffnen direkt von einem Netzlaufwerk (`\\server\…`) und Safari. Das sollte vor dem Verteilen jemand auf einem echten Windows-Laptop ausprobieren.

### Grenzen gegenüber der Fassung mit Webserver

- **Größe:** Die Datei hat ca. 42 MB. Für die meisten Mail-Anhänge ist das zu groß.
- **Öffnen:** Der Browser muss beim Öffnen jedes Mal die ganze Datei einlesen. Auf schwachen Laptops dauert das etwas länger, die Oberfläche erscheint aber zuerst.
- **Updates:** Jede neue Version muss neu heruntergeladen werden. Wer eine alte Kopie behält, arbeitet mit der alten Version.
- **Gemerkter Zusatz:** Er gilt für alle lokal geöffneten HTML-Dateien gemeinsam, weil Browser bei `file://` nicht zwischen einzelnen Dateien unterscheiden. Das ist unkritisch.

## Grenzen

- **Arbeitsspeicher:** Jede Datei wird komplett in den Speicher des FFmpeg im Browser kopiert, das Ergebnis ebenso. Sehr lange oder hoch aufgelöste Videos können daran scheitern. Dafür ist das Skript `rauschen_werkzeug.py` gedacht.
- **Geschwindigkeit:** Der FFmpeg-Kern läuft einfädig. Audio geht schnell, Videos dauern spürbar länger, weil das Bild neu encodiert wird.
- **Verlustbehaftete Sonderfälle:** 24- und 32-Bit-WAV werden zu 16 Bit, Apple Lossless (ALAC) wird zu AAC, Mehrkanalton wird zu Stereo, MP3 mit variabler Bitrate wird bei „Wie Original“ zu konstanter Bitrate.
- **Browser:** Entwickelt und getestet in Chromium, die Bearbeitung zusätzlich in Firefox. Safari ist noch nicht getestet.

## Bibliotheken und Lizenzen

Der eigene Code steht unter der MIT-Lizenz. Die mitgelieferten Bibliotheken behalten ihre eigenen Lizenzen: FFmpeg-Kern GPL-2.0-or-later, Atkinson Hyperlegible SIL Open Font License. Details, die Bibliotheken im FFmpeg-Kern und der Quellcode-Nachweis stehen in `LICENSES.md`, die Kurzfassung auf der Seite unter „Datenschutz und Lizenzen“. Die Offline-Fassung bettet die Lizenztexte beim Bauen direkt in die Datei ein.
