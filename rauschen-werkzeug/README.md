# Rauschen-Werkzeug

Ein Werkzeug für Autorinnen und Autoren: MP3-, WAV- und M4A-Dateien sowie Videos (MP4, MOV) hineinziehen, und jede Datei bekommt am Anfang 1 Sekunde unhörbar leises Rauschen (−70 dBFS). Auf Wunsch liegt dasselbe Rauschen auch unter dem restlichen Ton. So verschlucken USB-C-Adapter mit eigenem Audio-Chip (z. B. „AB13X USB Audio“) den Anfang nicht mehr.

Die Bearbeitung läuft vollständig im Browser. Es werden keine Dateien hochgeladen und keine externen Dienste aufgerufen, auch Schriften und Bibliotheken liegen in diesem Ordner.

## Starten

**Am einfachsten:** die Offline-Fassung `audio-noise-generator-offline.html` aus den Releases des Repositorys herunterladen und per Doppelklick öffnen.

**Aus diesem Ordner:** Per Doppelklick auf `index.html` funktioniert es nicht, weil Browser die nötigen Hintergrundprozesse bei lokal geöffneten Dateien blockieren. Stattdessen im Ordner einen lokalen Webserver starten und im Browser `http://localhost:8000` öffnen:

```
python3 -m http.server 8000
```

## Bedienung

Eine ausführliche Erklärung aller Bedienelemente, Statusmeldungen und häufigen Fragen steht in [HELP.md](HELP.md). Dieselbe Hilfe gibt es als eigene Seite `help.html`, erreichbar über den Knopf „Hilfe“ rechts über den Einstellungen. Sie öffnet sich im selben Tab, „Zurück zum Werkzeug“ führt zurück. Die Dateiliste bleibt dabei erhalten, weil der Browser die Seite aus seinem Zwischenspeicher wiederherstellt.

1. Seite öffnen und Dateien in das Feld ziehen oder auswählen. Beim ersten Mal lädt der Browser das Bearbeitungsprogramm (ca. 32 MB), danach kommt es aus dem Cache.
2. Die Dateien werden nacheinander bearbeitet. Videos dauern länger, weil das Bild neu encodiert wird.
3. Zu jeder Datei erscheinen eine Wellenform (Vorlauf farbig abgesetzt), eine Vorschau zum Anhören und das Prüfergebnis.
4. Mit „Kein Rauschen, nur Stille“ besteht der Vorlauf aus reiner Stille statt aus Rauschen. Das verlängert die Datei nur am Anfang. Gegen Adapter, die den Anfang verschlucken, hilft es nicht.
5. Werden danach Vorlauf, Rauschpegel, „Rauschen auch unter den Ton legen“ oder „Kein Rauschen“ geändert, erscheint „Mit neuen Einstellungen wiederholen“. Damit werden alle Dateien der Liste mit den neuen Werten neu erzeugt, ohne sie erneut auszuwählen.
6. Einzeln speichern oder „Alle speichern“ (als ZIP). Die Dateien behalten Namen und Format und können die Originale direkt ersetzen. Wer die Originale behalten will, trägt unter „Zusatz im Dateinamen“ etwas wie `_vorlauf` ein. Der Zusatz gilt dann für alle Dateien (`Aufgabe.mp3` wird zu `Aufgabe_vorlauf.mp3`) und bleibt für den nächsten Besuch gespeichert.

Bereits bearbeitete Dateien tragen eine Markierung im Kommentarfeld und werden beim nächsten Mal übersprungen. Das gilt auch für Dateien aus dem Skript `rauschen_werkzeug.py`. Das Python-Skript ist ein eigenständiges Werkzeug und nicht Teil dieses Repositorys.

## Hinweise

- **Browser:** Gedacht für aktuelle Versionen von Chrome, Edge, Firefox und Safari. Getestet wurde bisher nur mit Chromium. Bitte vor dem Einsatz in Firefox und Safari ausprobieren.
- **Große Videos:** Das Video wird im Arbeitsspeicher des Browsers bearbeitet. Sehr lange oder sehr hoch aufgelöste Videos können daran scheitern. Dafür das Skript `rauschen_werkzeug.py` verwenden.
- **Pegel:** Das Werkzeug misst vor jeder Datei, wie viel Rauschen der Encoder schluckt, und gleicht das aus. Der Pegel im Ergebnis liegt dadurch bei allen Formaten und Bitraten gleich.
- **Bildqualität:** Videos werden als H.264 mit hoher Qualität (CRF 20) neu encodiert. Das erste Bild steht für die Dauer des Vorlaufs still.

## Lizenzen

Eigener Code unter MIT (`LICENSE.txt`), die Bibliotheken unter `lib/` unter ihren eigenen Lizenzen, darunter der FFmpeg-Kern unter GPL-2.0-or-later. Details und Quellcode-Nachweis: [LICENSES.md](LICENSES.md). Wer den Ordner weitergibt, gibt ihn vollständig weiter, dann sind alle Lizenztexte dabei.
