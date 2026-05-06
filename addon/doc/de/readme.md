# WhatsApp NG

NVDA-Add-on, das Barrierefreiheitsverbesserungen für die webbasierte WhatsApp-Desktop-Version bietet.

## Funktionen

- **Alt+1**: Zur WhatsApp-Konversationsliste wechseln
- **Alt+2**: Zur WhatsApp-Nachrichtenliste wechseln
- **Alt+D**: Zum Nachrichteneingabefeld wechseln
- **Enter**: Sprachnachricht abspielen (funktioniert in einzelnen Chats und Gruppen)
- **Umschalt+Enter**: Kontextmenü für Nachrichten öffnen
- **Strg+C**: Aktuelle Nachricht in die Zwischenablage kopieren
- **Strg+R**: Vollständige Nachricht vorlesen (klickt bei Bedarf auf "Mehr lesen"-Schaltfläche)
- **Strg+Umschalt+Enter**: Auf Nachricht reagieren

### Umschalt-Skripte (keine Standard-Tastenkürzel - in Eingabegesten konfigurieren)

- Telefonnummernfilter in der Konversationsliste umschalten
- Telefonnummernfilter in der Nachrichtenliste umschalten
- Automatischen Fokusmodus umschalten (ermöglicht den Browse-Modus bei Bedarf)

## Native Tastaturkürzel von WhatsApp Desktop

- Als ungelesen markieren: Strg+Umschalt+U
- Benachrichtigungen stummschalten: Strg+Umschalt+M
- Chat archivieren: Strg+Umschalt+A
- Chat anheften: Strg+Alt+Umschalt+P
- Suchen: Strg+Alt+/
- Im Chat suchen: Strg+Umschalt+F
- Neuer Chat: Strg+Alt+N
- Nächster Chat: Strg+]
- Vorheriger Chat: Strg+[
- Label zum Chat hinzufügen: Strg+Cmd+Umschalt+L
- Chat schließen: Escape
- Neue Gruppe: Strg+Umschalt+N
- Profil und Info: Strg+Alt+P
- Geschwindigkeit der Sprachnachricht erhöhen: Umschalt+.
- Geschwindigkeit der Sprachnachricht verringern: Umschalt+,
- Einstellungen: Alt+S
- Emoji-Panel: Strg+Alt+E
- GIF-Panel: Strg+Alt+G
- Sticker-Panel: Strg+Alt+S
- Erweiterte Suche: Alt+K
- App sperren: Alt+L
- Chatdetails öffnen: Alt+I
- Chat sperren: Strg+Umschalt+B
- Antworten: Alt+R
- Privat antworten: Strg+Alt+R
- Weiterleiten: Strg+Alt+D
- Nachricht mit Stern markieren: Alt+8
- Anhang-Dropdown-Menü öffnen: Alt+A
- PTT-Aufnahme starten: Strg+Alt+Umschalt+R
- PTT-Aufnahme pausieren: Alt+P
- PTT senden: Strg+Enter
- Letzte Nachricht bearbeiten: Strg+Pfeiltaste nach oben
- Kamera ein/aus: Strg+Alt+V
- Stumm schalten/reaktivieren: Strg+Alt+M
- Reaktionen: Strg+Alt+R
- Hand heben: Strg+Alt+H
- Bildschirm freigeben: Strg+Alt+S
- Anruf beenden: Strg+Alt+W
- Vergrößern: Strg++
- Verkleinern: Strg+-
- Zoom zurücksetzen: Strg+0
- Chat öffnen: Strg+1..9

## Anforderungen

- NVDA 2021.1 oder neuer
- WhatsApp Desktop (webbasierte Version)

## Installation

1. Laden Sie die Datei `whatsAppNG.nvda-addon` herunter
2. Gehen Sie in NVDA zu **Extras → Add-on-Manager**
3. Klicken Sie auf **Installieren** und wählen Sie die Datei aus
4. Starten Sie NVDA neu

## Konfiguration

Die Telefonnummernfilter können umgeschaltet werden:
- In der Konversationsliste: Tastenkürzel in Eingabegesten konfigurieren
- In der Nachrichtenliste: Tastenkürzel in Eingabegesten konfigurieren

Konfigurieren Sie Tastenkürzel unter:
**NVDA-Menü → Einstellungen → Eingabegesten → WhatsApp NG**

## Änderungsprotokoll

### Version 1.8.1 (2026-05-06)

**Geändert:**
- NVDA 2026 Kompatibilität

**Behoben:**
- Control+R: Funktionierte nicht bei Nachrichten mit "Weiterlesen"-Schaltfläche (findet die Schaltfläche jetzt über die Struktur statt über sprachabhängigen Text)
- Control+R: Funktionierte nicht bei deaktiviertem Hinweis-Filter
- Control+R: Las keine Nachrichten mit Links oder formatiertem Text

### Version 1.8.0 (2026-05-01)

**Hinzugefügt:**
- Spenden-Dialog bei der Add-on-Installation

**Geändert:**
- Navigation (Alt+1, Alt+2, Alt+D) widerstandsfähiger gegen WhatsApp-UI-Änderungen

**Behoben:**
- Enter und Shift+Enter funktionierten nicht bei deaktiviertem Hinweis-Filter
- Enter-Taste funktionierte nicht in Dateidialogen und Konversationsliste
- Telefonnummern-Filter in Konversationsliste wurde nach Umschalten nicht korrekt aktualisiert
- Verbesserte finnische Übersetzung und Dokumentation

### Version 1.7.1 (2026-04-10)

**Behoben:**
- Enter-Tasten-Wiedergabereihenfolge: Problem behoben, bei dem Audionachrichten nicht mehr mit der Enter-Taste abgespielt wurden
  - Die Überprüfung der Schaltfläche erfolgt nun nur außerhalb der Nachrichtenliste
  - Audionachrichten werden korrekt abgespielt, wenn in der Nachrichtenliste navigiert wird

### Version 1.7.0 (2026-04-10)

**Hinzugefügt:**
- Finnische Übersetzung: Vollständige Unterstützung der finnischen Sprache

**Behoben:**
- Enter-Taste auf Schaltflächen: Enter wird jetzt korrekt weitergeleitet, wenn der Fokus auf einer Schaltfläche liegt
  - Früher drückte die Eingabetaste auf beliebigen Schaltflächen in WhatsApp die Audiowiedergabe
  - Jetzt funktionieren Schaltflächen korrekt (z. B. funktioniert die Schaltfläche "Datei speichern" wie erwartet)

### Version 1.6.0 (2026-03-23)

**Hinzugefügt:**
- Filter für Nutzungshinweise: Blendet automatisch Hinweise wie "Für weitere Optionen..." aus Nachrichtenankündigungen aus
  - Unterstützt mehrere Sprachen
  - Kann mit NVDA+Shift+H umgeschaltet werden

**Behoben:**
- Doppelte Ankündigungen in der Konversationsliste: NVDA kündigt jede Zeile nicht mehr zweimal bei der Navigation mit Pfeiltasten an (#11)
- Alt+1-Navigation: Höhere Zuverlässigkeit beim Finden der Konversationsliste
- Nachrichten kopieren: Höhere Genauigkeit beim Kopieren von Nachrichten mit Strg+C

### Version 1.5.0 (2026-03-05)

**Hinzugefügt:**
- Strg+Umschalt+Enter: Auf Nachricht reagieren (öffnet Reaktionsmenü)
- Alt+Enter: Vollständige Nachricht im Browsermodus lesen
- Native WhatsApp-Desktop-Tastaturkürzel zur Dokumentation hinzugefügt

**Geändert:**
- Leistung erheblich optimiert: Navigation ist nun flüssiger und reaktiver
- Alt+2 zuverlässiger und präziser in der Navigation
- Strg+C funktioniert jetzt nur in der Nachrichtenliste

**Behoben:**
- Strg+R liest nun den vollständigen Text korrekt beim Erweitern langer Nachrichten

### Version 1.4.0 (2026-02-23)

**Hinzugefügt:**
- Vollständige Sprachunterstützung für: Arabisch, Deutsch, Spanisch, Italienisch und Russisch
- Ukrainische Übersetzung mit aktuellen Strings aktualisiert

**Behoben:**
- "Text nicht gefunden"-Fehler in Strg+R nach dem Klicken auf "Mehr lesen"-Schaltfläche
- Strg+R funktioniert jetzt nur bei Textnachrichten (zeigt "Keine Textnachricht" für Sprachnachrichten/Bilder an)

**Geändert:**
- Repository-Links zum neuen Repository aktualisiert (nunotfc/WhatsAppNG)
- Dokumentation: Alle lokalisierten READMEs enthalten nun das vollständige Änderungsprotokoll bis Version 1.3.0

### Version 1.3.0 (2026-02-07)

**Hinzugefügt:**
- Türkische Übersetzungsunterstützung
- Option zum Umschalten des automatischen Fokusmodus (Geste in Eingabegesten konfigurieren)

**Geändert:**
- Verbesserte Leistung: Navigationsbefehle sind bei wiederholter Verwendung jetzt schneller
- Die Escape-Taste wird nun korrekt an WhatsApp weitergeleitet

**Behoben:**
- Enter spielt jetzt Videonachrichten ab (funktionierte previously nur für Audio)

### Version 1.1.1 (2025-01-31)

**Hinzugefügt:**
- Strg+R: Vollständige Nachricht vorlesen (klickt automatisch auf "Mehr lesen"-Schaltfläche)
- Strg+C: Aktuelle Nachricht in die Zwischenablage kopieren
- Automatisches Deaktivieren des Browse-Modus (hält den Fokusmodus für eine bessere WhatsApp-Erfahrung aktiv)

**Geändert:**
- Verbesserte Fehlermeldungen: Alle Skripte bieten nun ein klares Feedback bei Fehlern
- Navigationsbefehle (Alt+1, Alt+2, Alt+D) sind bei Erfolg nun still

**Behoben:**
- Alt+1 und Alt+2 melden Fehler korrekt, wenn alle Pfade fehlschlagen
- Objektfilterung optimiert, um Eingabeverzögerungen zu reduzieren
- Enter: Slider-basierte Erkennung statt Button-Zählung (zuverlässiger)

### Version 1.1.0 (2025-01-30)

**Hinzugefügt:**
- Strg+R: Vollständige Nachricht vorlesen
- Intelligente Sprachnachrichten-Wiedergabe mithilfe der Slider-Erkennung

**Geändert:**
- Enter: Verbesserte Logik unter Verwendung der Slider-Erkennung anstatt des Zählens von Buttons

**Behoben:**
- Alt+2 versucht nun korrekt alle Navigationspfade, wenn der erste Versuch fehlschlägt

### Version 1.0.0 (2025-01-29)

**Erste Version:**
- Navigationskurzbefehle für Konversationsliste, Nachrichtenliste und Nachrichten-Composer
- Sprachnachrichten-Wiedergabe mit Unterstützung für einzelne Chats und Gruppen
- Kontextmenüzugriff für Nachrichtenaktionen
- Umschalten der Telefonnummernfilter für Konversationen und Nachrichten
- Automatische Fokusmodus-Aktivierung in WhatsApp Desktop

## Credits

Entwickelt von Nuno Costa, um Barrierefreiheitsverbesserungen für das moderne WhatsApp Desktop Erlebnis zu bieten.

## Support

Für Probleme oder Vorschläge besuchen Sie bitte:
https://github.com/nunotfc/whatsAppNG/issues

## Übersetzungskompilierung

Um Übersetzungen zu aktualisieren oder zu kompilieren:
```bash
scons pot
```

Dies erfordert die Installation der GNU Gettext-Tools.
