# Hilfe zum Rauschen-Werkzeug

> **Kurz gesagt:** Dateien in das Feld ziehen, warten, bis bei jeder Datei ein Häkchen steht, und dann „Alle speichern“ klicken. Die Voreinstellungen passen für fast alle Fälle.

Das Rauschen-Werkzeug ergänzt Audios und Videos am Anfang um eine kurze, unhörbar leise Rauschspur, den **[Vorlauf](#glossar)**. USB-C-Adapter mit eigenem Audio-Chip brauchen nach einer Pause einen Moment zum Aufwachen und verschlucken sonst den Anfang. Das Rauschen weckt sie, bevor der eigentliche Ton beginnt.

Diese Seite erklärt jedes Bedienelement der Reihe nach, so wie es auf dem Bildschirm erscheint.

---

## Inhalt

1. [Erste Schritte](#erste-schritte)
2. [Einstellungen](#einstellungen)
   - [Vorlauf](#vorlauf)
   - [Rauschpegel](#rauschpegel)
   - [Rauschen unter dem Ton](#rauschen-unter-dem-ton)
   - [Ohne Rauschen](#ohne-rauschen)
   - [Zusatz im Dateinamen](#zusatz-im-dateinamen)
   - [Ausgabeformat](#ausgabeformat)
3. [Ablagefeld](#ablagefeld)
4. [Dateiliste](#dateiliste)
   - [Kopfzeile der Liste](#kopfzeile-der-liste)
   - [Mit neuen Einstellungen wiederholen](#mit-neuen-einstellungen-wiederholen)
   - [Liste leeren](#liste-leeren)
   - [Alle speichern](#alle-speichern)
5. [Eine Datei in der Liste](#eine-datei-in-der-liste)
   - [Zeilenkopf und Statusmeldungen](#zeilenkopf-und-statusmeldungen)
   - [Wellenform](#wellenform)
   - [Hinweise aus der Prüfung](#hinweise-aus-der-prüfung)
   - [Player](#player)
   - [Diese Datei speichern](#diese-datei-speichern)
   - [Als data-URI kopieren](#als-data-uri-kopieren)
6. [Aufklappbereiche am Seitenende](#aufklappbereiche-am-seitenende)
7. [Bedienung mit der Tastatur](#bedienung-mit-der-tastatur)
8. [Meldungen unter dem Ablagefeld](#meldungen-unter-dem-ablagefeld)
9. [Häufige Fragen](#häufige-fragen)
10. [Glossar](#glossar)
11. [Siehe auch](#siehe-auch)

---

## Erste Schritte

1. Die Seite in Edge, Chrome oder Firefox öffnen.
2. Dateien in das [Ablagefeld](#ablagefeld) ziehen oder dort auf **auswählen** klicken.
3. Warten. Oben in der Liste steht, wie viele Dateien schon fertig sind. Beim ersten Mal lädt der Browser zusätzlich das Bearbeitungsprogramm (ca. 32 MB).
4. Bei jeder Datei steht danach rechts **✓ Vorlauf 1 s**.
5. [Alle speichern](#alle-speichern) klicken, oder einzelne Dateien über [Diese Datei speichern](#diese-datei-speichern).

Die Dateien werden **nur in diesem Browser** bearbeitet. Es wird nichts hochgeladen.

[↑ Nach oben](#inhalt)

---

## Einstellungen

Die Karte oben auf der Seite. Rechts darüber führt der Knopf **Hilfe** zu dieser Seite. „Zurück zum Werkzeug“ führt wieder zurück, die Dateiliste bleibt dabei erhalten.

Die Einstellungen gelten für alle Dateien, die **danach** hineingezogen werden. Wer sie für bereits bearbeitete Dateien ändert, nutzt [Mit neuen Einstellungen wiederholen](#mit-neuen-einstellungen-wiederholen).

### Vorlauf

Wie lange das Rauschen vor dem ersten Ton dauert, in Sekunden.

| | |
|---|---|
| Voreinstellung | 1 s |
| Bereich | 0 bis 5 s |
| Schritte mit −/+ | 0,25 s |

- **Eintippen:** Komma und Punkt funktionieren beide (`1,5` und `1.5`).
- **−** und **+** neben dem Feld oder die Pfeiltasten ↑/↓ ändern den Wert schrittweise.
- Werte außerhalb des Bereichs werden auf die Grenze gesetzt. `10` wird also zu 5 s.
- Steht etwas im Feld, das keine Zahl ist, wird der Rahmen **rot**. Gerechnet wird dann mit der Voreinstellung.
- Ist [Ohne Rauschen](#ohne-rauschen) angekreuzt, heißt der Hinweis darunter „Stille vor dem ersten Ton“.
- **0 s** setzt keinen Vorlauf, der Ton beginnt sofort. Mit [Rauschen unter dem Ton](#rauschen-unter-dem-ton) liegt das Rauschen dann nur unter dem Ton, sonst bekommt die Datei nur den kurzen Nachlauf von 0,1 s und die Markierung. Die Zeile zeigt danach **✓ Ohne Vorlauf**.

**Empfehlung:** 1 s reicht für die meisten Adapter. Wird der Anfang trotzdem verschluckt, auf 1,5 oder 2 s erhöhen.

[↑ Nach oben](#inhalt)

### Rauschpegel

Wie laut das Rauschen ist, in [dBFS](#glossar). Je niedriger die Zahl, desto leiser.

| | |
|---|---|
| Voreinstellung | −70 dBFS |
| Bereich | −90 bis −40 dBFS |
| Schritte mit −/+ | 5 dB |

- Der Wert ist der **Spitzenpegel**. In der Datei kommt im Mittel etwa 5 dB weniger an, deshalb steht im [Player](#player) bei −70 die Angabe „Rauschen im Ergebnis −75 dB“.
- Das Werkzeug gleicht aus, wenn MP3 oder AAC beim Komprimieren Rauschen „verschluckt“. Der Pegel im Ergebnis ist bei allen Formaten gleich.
- Bei [Ohne Rauschen](#ohne-rauschen) ist das Feld ausgegraut.

**Empfehlung:** −70 nicht ändern. Erst wenn bei einer Datei [Vorlauf zu leise](#hinweise-aus-der-prüfung) steht oder ein Adapter trotzdem nicht aufwacht, auf −65 oder −60 erhöhen. Ab etwa −40 ist das Rauschen hörbar.

[↑ Nach oben](#inhalt)

### Rauschen unter dem Ton

Kästchen **„Auch unter den Ton legen“**. Voreinstellung: angekreuzt.

- **Angekreuzt:** Das Rauschen läuft nach dem Vorlauf leise unter dem ganzen Ton weiter. So schlafen Adapter auch in Sprechpausen nicht ein.
- **Nicht angekreuzt:** Rauschen nur im Vorlauf und in einem kurzen Nachlauf von 0,1 s am Ende.
- Bei [Ohne Rauschen](#ohne-rauschen) ist das Kästchen ausgegraut.

[↑ Nach oben](#inhalt)

### Ohne Rauschen

Kästchen **„Kein Rauschen, nur Stille“**. Voreinstellung: nicht angekreuzt.

- Der Vorlauf besteht dann aus **reiner Stille** statt aus Rauschen. Die Datei wird nur am Anfang länger.
- [Rauschpegel](#rauschpegel) und [Rauschen unter dem Ton](#rauschen-unter-dem-ton) sind dann ohne Wirkung und ausgegraut.
- Die Zeile zeigt danach **✓ Vorlauf 1 s, Stille**.

> **Achtung:** Stille hilft **nicht** gegen Adapter, die den Anfang verschlucken. Genau dafür ist das Rauschen da. Diese Option nur nutzen, wenn ausdrücklich eine stille Pause vor dem Ton gewünscht ist.

[↑ Nach oben](#inhalt)

### Zusatz im Dateinamen

Ein Text, der beim Speichern an **alle** Dateinamen angehängt wird, vor der Endung.

| Zusatz | Original | gespeichert als |
|---|---|---|
| *(leer)* | `Aufgabe_01.mp3` | `Aufgabe_01.mp3` |
| `_vorlauf` | `Aufgabe_01.mp3` | `Aufgabe_01_vorlauf.mp3` |
| `-neu` | `Einleitung.final.wav` | `Einleitung.final-neu.wav` |

- Unter dem Feld steht sofort, wie die erste Datei der Liste heißen wird.
- **Leer lassen**, wenn die bearbeiteten Dateien die Originale ersetzen sollen.
- Gilt für [Diese Datei speichern](#diese-datei-speichern), für die Dateien **in** der ZIP von [Alle speichern](#alle-speichern) und für die Ersatz-Textdatei bei [Als data-URI kopieren](#als-data-uri-kopieren).
- Zeichen, die Windows oder macOS in Dateinamen nicht erlauben (`\ / : * ? " < > |`), werden weggelassen.
- Der Zusatz betrifft nur den Namen. Wer ihn nach der Bearbeitung ändert, muss nichts neu bearbeiten.
- Der Browser **merkt sich** den Zusatz für den nächsten Besuch. Wer das Feld leert, löscht ihn.
- Mit dem [Ausgabeformat](#ausgabeformat) **MP3** ändert sich zusätzlich die Endung, z. B. `Aufgabe_01.wav` → `Aufgabe_01_vorlauf.mp3`.

[↑ Nach oben](#inhalt)

### Ausgabeformat

Umschalter **„Wie Original“ | „MP3“**. Voreinstellung: Wie Original.

- **Wie Original:** Jede Datei behält ihr Format, ihre Abtastrate und ihre Bitrate (siehe [Häufige Fragen](#ändert-sich-die-qualität)).
- **MP3:** Alle **Audiodateien** (MP3, WAV, M4A) werden als MP3 gespeichert. Die Endung wird zu `.mp3`, in der Zeile steht neben der Größe z. B. „517 KB → MP3, 33 KB“.
- **Videos behalten immer ihr Format.** Für sie hat der Umschalter keine Wirkung.

Bei **MP3** erscheinen darunter die MP3-Einstellungen:

| Einstellung | Auswahl | Hinweise |
|---|---|---|
| **Kanäle** | Wie Original, Mono, Stereo | Mono mischt beide Kanäle zusammen. Mehrkanalton wird bei „Wie Original“ zu Stereo. |
| **Abtastrate** | Wie Original, 48 000 bis 8 000 Hz | MP3 kann höchstens 48 000 Hz. Bei „Wie Original“ werden höhere Raten (z. B. 96 000 Hz) auf 48 000 Hz gesenkt, krumme Raten auf die nächstniedrigere MP3-Rate. |
| **Bitratenmodus** | Konstant (CBR), Variabel (VBR) | CBR: jede Sekunde gleich groß, gut für alte Player. VBR: die Bitrate passt sich dem Inhalt an, bei gleicher Qualität meist kleiner. |
| **Bitrate** (nur CBR) | Wie Original, 320 bis 32 kb/s | Bei „Wie Original“ die Bitrate der Quelle, mindestens 64 kb/s, höchstens 320 kb/s. Unter 32 000 Hz erlaubt MP3 höchstens 160 kb/s, höhere Werte werden darauf gesenkt. |
| **Qualität** (nur VBR) | V0 bis V9 | V0 ist die beste Qualität (ca. 245 kb/s), V9 die kleinste Datei (ca. 65 kb/s). Voreinstellung V2 (ca. 190 kb/s). Die Angaben gelten für 44 100 Hz Stereo. |

- Wer Format oder MP3-Einstellungen nach der Bearbeitung ändert, kann die Dateien über [Mit neuen Einstellungen wiederholen](#mit-neuen-einstellungen-wiederholen) neu erzeugen.
- Die MP3-Einstellungen werden nicht gespeichert. Nach dem Neuladen der Seite steht das Ausgabeformat wieder auf „Wie Original“.

[↑ Nach oben](#inhalt)

---

## Ablagefeld

Das große Feld mit dem Pfeilsymbol: **„Dateien hierher ziehen oder auswählen“**.

- **Hineinziehen:** Dateien aus dem Explorer bzw. Finder auf das Feld ziehen. Der Rahmen färbt sich, solange man darüber ist.
- **Auswählen:** auf das Feld klicken, dann öffnet sich die Dateiauswahl.
- Mehrere Dateien auf einmal sind möglich. Sie werden **nacheinander** bearbeitet.
- **Unterstützte Formate:** MP3, WAV, M4A sowie Videos als MP4, M4V und MOV.
- Andere Dateien erscheinen trotzdem in der Liste, aber mit der Meldung „Format wird nicht unterstützt“.
- Neue Dateien kommen jeweils unten an die Liste. Was schon drin ist, bleibt erhalten.

Unter dem Feld erscheinen bei Bedarf [Meldungen zum Bearbeitungsprogramm](#meldungen-unter-dem-ablagefeld).

[↑ Nach oben](#inhalt)

---

## Dateiliste

Erscheint, sobald die erste Datei hineingezogen wurde.

### Kopfzeile der Liste

| Element | Bedeutung |
|---|---|
| **„3 Dateien“** | Anzahl der Dateien in der Liste, auch die nicht unterstützten |
| **◌ „1 von 3 fertig“** | Fortschritt, solange noch Dateien warten oder bearbeitet werden. Verschwindet, wenn alles durch ist. |
| **Ocker** ▬ ergänzter Vorlauf | Farbe des neuen Vorlaufs in der [Wellenform](#wellenform) |
| **Petrol** ▬ ursprünglicher Ton | Farbe des ursprünglichen Tons in der [Wellenform](#wellenform) |
| **„ZIP wird erstellt …“** | erscheint kurz beim [Speichern als ZIP](#alle-speichern) |
| **ZIP konnte nicht erstellt werden: …** | meist ist die ZIP größer als 4 GB. Die Dateien einzeln speichern. |

Rechts stehen die drei Knöpfe, die folgen.

[↑ Nach oben](#inhalt)

### Mit neuen Einstellungen wiederholen

Erscheint **nur**, wenn [Vorlauf](#vorlauf), [Rauschpegel](#rauschpegel), [Rauschen unter dem Ton](#rauschen-unter-dem-ton), [Ohne Rauschen](#ohne-rauschen) oder das [Ausgabeformat](#ausgabeformat) nicht mehr zu den Einstellungen passen, mit denen die Dateien bearbeitet wurden.

- Ein Klick bearbeitet alle betroffenen Dateien neu, mit den aktuellen Einstellungen. Man muss sie nicht noch einmal auswählen.
- Wer die alten Werte wieder einstellt, lässt den Knopf verschwinden.
- Eine Datei, die gerade bearbeitet wird, läuft erst zu Ende und kommt dann noch einmal dran.
- Der [Zusatz im Dateinamen](#zusatz-im-dateinamen) löst diesen Knopf nicht aus, weil er nur den Namen betrifft.

[↑ Nach oben](#inhalt)

### Liste leeren

Entfernt alle Dateien aus der Liste und bricht eine laufende Bearbeitung sofort ab.

> **Achtung:** Noch nicht gespeicherte Ergebnisse gehen dabei verloren. Die Originaldateien auf dem Rechner bleiben immer unverändert.

[↑ Nach oben](#inhalt)

### Alle speichern

Speichert alle **fertigen** Dateien zusammen als **`rauschen-werkzeug.zip`** im Download-Ordner.

- Ist ausgegraut, solange noch keine Datei fertig ist.
- Dateien mit Fehlermeldung oder „Bereits bearbeitet“ sind nicht in der ZIP, weil es von ihnen kein neues Ergebnis gibt.
- Die Dateien in der ZIP tragen ihren Originalnamen, gegebenenfalls mit [Zusatz](#zusatz-im-dateinamen).
- Haben zwei Dateien denselben Namen, etwa aus zwei Ordnern, bekommt die zweite einen Zusatz wie `Aufgabe (2).mp3`. So überschreiben sie sich beim Entpacken nicht.

[↑ Nach oben](#inhalt)

---

## Eine Datei in der Liste

Jede Datei hat eine eigene Zeile. Die erste bearbeitbare Datei ist aufgeklappt, die anderen lassen sich über den Zeilenkopf öffnen.

### Zeilenkopf und Statusmeldungen

Der Zeilenkopf zeigt links einen **Pfeil** (› zu, ⌄ offen), dann **Dateiname** und **Größe** und rechts den **Status**. Ein Klick auf die Zeile klappt sie auf oder zu. Das geht erst, wenn die Datei fertig ist.

Während der Bearbeitung läuft unter dem Zeilenkopf ein dünner **Fortschrittsbalken**.

| Status | Bedeutung | Was tun |
|---|---|---|
| In der Warteschlange | wartet, bis die Dateien davor fertig sind | nichts |
| Wartet auf das Bearbeitungsprogramm … | das Programm startet, beim ersten Mal wird es geladen | nichts |
| Pegel wird abgestimmt … | misst, wie viel Rauschen das Format schluckt | nichts |
| Wird bearbeitet … | Rauschen wird hinzugefügt, Datei neu erzeugt | nichts |
| Video wird bearbeitet, das kann etwas dauern … | wie oben, das Bild wird zusätzlich neu kodiert | Geduld, etwa so lange wie das Video |
| Ergebnis wird geprüft … | das Ergebnis wird nachgemessen | nichts |
| **✓ Vorlauf 1 s** | fertig und geprüft | speichern |
| **✓ Vorlauf 1 s, Stille** | fertig, Vorlauf als Stille ([Ohne Rauschen](#ohne-rauschen)) | speichern |
| **✓ Ohne Vorlauf** | fertig, [Vorlauf](#vorlauf) auf 0 s gestellt | speichern |
| ⚠ **Vorlauf zu leise** | fertig, aber das Rauschen kommt zu leise an | [Rauschpegel](#rauschpegel) erhöhen und [wiederholen](#mit-neuen-einstellungen-wiederholen) |
| Bereits bearbeitet, Markierung gefunden | die Datei hat schon einen Vorlauf von diesem Werkzeug oder vom Skript | nichts, das Original ist schon fertig |
| ⚠ Keine Tonspur gefunden, Datei bleibt unverändert | die Datei enthält keinen Ton | Datei prüfen |
| ⚠ Kein Bild gefunden, bitte als Audiodatei speichern | eine `.mp4` oder `.mov` ohne Bild | als `.m4a` speichern und erneut hineinziehen |
| ⚠ Format wird nicht unterstützt (MP3, WAV, M4A, MP4, M4V, MOV) | die Dateiendung ist keines dieser Formate | Datei in eines dieser Formate umwandeln |
| ⚠ Fehler beim Bearbeiten: … | das Bearbeitungsprogramm ist an der Datei gescheitert, dahinter steht seine letzte Meldung | Datei in einem anderen Programm öffnen und neu speichern; siehe [Häufige Fragen](#häufige-fragen) |
| ⚠ Fehler: … | unerwarteter Fehler, z. B. zu wenig Arbeitsspeicher | Seite neu laden, Datei einzeln versuchen |

[↑ Nach oben](#inhalt)

### Wellenform

Das Balkenbild in der aufgeklappten Zeile zeigt die **fertige** Datei:

- **Ocker:** der ergänzte Vorlauf
- **Petrol:** der ursprüngliche Ton

Die Höhe ist logarithmisch dargestellt. Deshalb ist auch das sehr leise Rauschen als Balken zu sehen, obwohl es nicht zu hören ist. Bei [Ohne Rauschen](#ohne-rauschen) ist der ockerfarbene Teil ganz flach.

Bei **Videos** steht über der Wellenform zusätzlich das Bild. Ein Klick darauf startet oder pausiert die Wiedergabe.

[↑ Nach oben](#inhalt)

### Hinweise aus der Prüfung

Rote Hinweise in der aufgeklappten Zeile. Zeilen mit Hinweisen klappen automatisch auf.

| Hinweis | Bedeutung | Was tun |
|---|---|---|
| Rauschen im Vorlauf zu leise, bitte Pegel erhöhen | das Rauschen kommt nach dem Komprimieren mehr als 8 dB unter dem eingestellten Wert an | [Rauschpegel](#rauschpegel) um 5 dB erhöhen und [wiederholen](#mit-neuen-einstellungen-wiederholen) |
| Stille Stelle von 1,2 s ohne Rauschen | irgendwo im Ton gibt es eine Stelle ohne Rauschen, länger als 0,2 s | meist harmlos; ist [Rauschen unter dem Ton](#rauschen-unter-dem-ton) aus, einschalten und wiederholen |

[↑ Nach oben](#inhalt)

### Player

Die Zeile mit dem runden Knopf zum Anhören des **Ergebnisses**.

| Element | Funktion |
|---|---|
| ▶ / ⏸ | abspielen bzw. pausieren. Es läuft immer nur eine Datei, eine andere zu starten pausiert die vorige. |
| `0:01 / 0:04` | aktuelle Position und Gesamtlänge, inklusive Vorlauf |
| Regler | an eine Stelle springen |
| „Rauschen im Ergebnis −75 dB“ | gemessener mittlerer Rauschpegel im Vorlauf. Fehlt bei [Ohne Rauschen](#ohne-rauschen). |

Steht statt der Zeit **„Vorschau in diesem Browser nicht abspielbar, die Datei ist trotzdem fertig“**, kann der Browser dieses Format nicht abspielen, etwa manche MOV-Videos in Firefox. Die Datei lässt sich trotzdem speichern.

[↑ Nach oben](#inhalt)

### Diese Datei speichern

Speichert nur diese eine Datei in den Download-Ordner, mit Originalnamen und gegebenenfalls [Zusatz](#zusatz-im-dateinamen).

[↑ Nach oben](#inhalt)

### Als data-URI kopieren

Kopiert die fertige Datei als **[data-URI](#glossar)** in die Zwischenablage, also als langen Text, der mit `data:audio/mpeg;base64,…` beginnt. Das braucht man, um die Datei direkt in eine Aufgaben- oder Unit-Definition einzufügen.

- Danach steht daneben z. B. **„Kopiert: data:audio/mpeg;base64, 92 KB Text“**.
- Steht dort **„Kopieren nicht möglich, die data-URI wird stattdessen als Textdatei gespeichert.“**, hat der Browser den Zugriff auf die Zwischenablage verweigert. Der Text liegt dann als `.txt`-Datei im Download-Ordner.

[↑ Nach oben](#inhalt)

---

## Aufklappbereiche am Seitenende

| Bereich | Inhalt |
|---|---|
| **Was genau passiert** | kurze technische Erklärung: wie das Rauschen eingefügt wird, was mit Videos passiert, die Markierung |
| **Datenschutz und Lizenzen** | was gespeichert wird (nur der [Zusatz](#zusatz-im-dateinamen)), dass nichts hochgeladen wird, und die Lizenzen aller verwendeten Bibliotheken |

[↑ Nach oben](#inhalt)

---

## Bedienung mit der Tastatur

| Taste | Wirkung |
|---|---|
| **Tab** / **Umschalt+Tab** | zum nächsten bzw. vorigen Bedienelement |
| **↑** / **↓** in [Vorlauf](#vorlauf) oder [Rauschpegel](#rauschpegel) | Wert um einen Schritt erhöhen bzw. verringern |
| **Leertaste** oder **Enter** | Knopf auslösen, Zeile auf- oder zuklappen, Dateiauswahl öffnen |
| **Leertaste** auf einem Kästchen | ankreuzen oder Haken entfernen |
| **←** / **→** auf dem Regler im [Player](#player) | spulen |

Das gerade aktive Element ist mit einem blauen Rahmen markiert.

[↑ Nach oben](#inhalt)

---

## Meldungen unter dem Ablagefeld

| Meldung | Bedeutung |
|---|---|
| Das Bearbeitungsprogramm wird geladen, beim ersten Mal ca. 32 MB … | erscheint beim ersten Bearbeiten; danach kommt das Programm aus dem Browser-Speicher |
| **Das Bearbeitungsprogramm konnte nicht geladen werden: …** | Netz unterbrochen oder Seite unvollständig. Seite neu laden. |
| **Dieses Werkzeug muss über einen Webserver geöffnet werden, nicht als Datei.** | `index.html` wurde per Doppelklick geöffnet. Stattdessen die Offline-Fassung `audio-noise-generator-offline.html` verwenden. |

[↑ Nach oben](#inhalt)

---

## Häufige Fragen

### Die Seite sieht normal aus, reagiert aber auf nichts.

Wahrscheinlich wurde `index.html` per Doppelklick geöffnet. Per Doppelklick funktioniert nur die Offline-Fassung `audio-noise-generator-offline.html`, siehe [Meldungen unter dem Ablagefeld](#meldungen-unter-dem-ablagefeld).

### Kann ich die Originaldateien einfach ersetzen?

Ja. Name und Format bleiben gleich, solange der [Zusatz im Dateinamen](#zusatz-im-dateinamen) leer ist und das [Ausgabeformat](#ausgabeformat) auf „Wie Original“ steht. Am besten die Originale vorher sichern.

### Hört man das Rauschen?

Bei −70 dBFS und normaler Lautstärke nein. Es liegt unter dem Grundgeräusch jedes Raums.

### Was passiert, wenn ich eine Datei zweimal hineinziehe?

Beim zweiten Mal steht „Bereits bearbeitet, Markierung gefunden“. Es wird kein zweiter Vorlauf ergänzt.

### Warum dauern Videos so lange?

Damit Bild und Ton synchron bleiben, wird das erste Bild für die Dauer des Vorlaufs festgehalten und das Video neu kodiert. Das dauert etwa so lange wie das Video selbst, bei hoher Auflösung länger.

### Ein großes Video scheitert mit einem Fehler.

Das Bearbeitungsprogramm im Browser hat höchstens 2 GB Arbeitsspeicher. Sehr lange oder hoch aufgelöste Videos passen nicht hinein. Dafür das Skript `rauschen_werkzeug.py` verwenden (siehe [README](README.md)).

### Eine Datei hängt seit Langem bei „Wird bearbeitet …“.

Bei Videos den Fortschrittsbalken beobachten. Bewegt er sich nicht mehr, die Seite neu laden und die Datei einzeln versuchen.

### Ändert sich die Qualität?

Die Dateien werden neu kodiert, mit gleicher Abtastrate und gleicher oder höherer Bitrate. Hörbar ist das nicht. Das Bild von Videos wird mit hoher Qualität neu kodiert (H.264). Ausnahmen: WAV-Dateien mit 24 oder 32 Bit werden als 16 Bit gespeichert, ein eingebettetes Cover-Bild geht verloren. Mit dem [Ausgabeformat](#ausgabeformat) MP3 bestimmen die gewählten MP3-Einstellungen die Qualität.

### Wird irgendetwas hochgeladen?

Nein. Alles passiert im Browser. Gespeichert wird nur der [Zusatz im Dateinamen](#zusatz-im-dateinamen), und auch der nur in diesem Browser.

[↑ Nach oben](#inhalt)

---

## Glossar

| Begriff | Erklärung |
|---|---|
| **Vorlauf** | der Abschnitt, der vor dem ursprünglichen Ton eingefügt wird: leises Rauschen oder, mit [Ohne Rauschen](#ohne-rauschen), Stille |
| **Nachlauf** | 0,1 s Rauschen oder Stille am Dateiende, damit der Ton nicht hart abbricht |
| **Rauschen** | hier: gleichmäßiges „Weißes Rauschen“ in sehr geringer Lautstärke |
| **dBFS** | Dezibel bezogen auf die größtmögliche Lautstärke einer Datei. 0 dBFS ist das Maximum, −70 dBFS ist sehr leise. |
| **Markierung** | ein Eintrag im Kommentarfeld der Datei, z. B. `rauschen-werkzeug 1000ms -70dBFS`. Daran erkennt das Werkzeug bereits bearbeitete Dateien. |
| **Kodieren / Encodieren** | eine Datei in ihr Format (MP3, AAC, H.264 …) umrechnen und komprimieren |
| **data-URI** | eine Datei als Text, der direkt in andere Dateien eingefügt werden kann |
| **ZIP** | eine Datei, die mehrere Dateien gebündelt enthält; unter Windows per Doppelklick zu öffnen |

[↑ Nach oben](#inhalt)

---

## Siehe auch

- [README](README.md): Einrichtung, Bereitstellung und Hinweise zum Skript
- [ARCHITECTURE](ARCHITECTURE.md): technischer Aufbau des Werkzeugs
- [LICENSES](LICENSES.md): Lizenzen der verwendeten Bibliotheken
