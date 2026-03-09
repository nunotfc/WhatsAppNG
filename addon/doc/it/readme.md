# WhatsApp NG

Componente aggiuntivo per NVDA che fornisce migliorie di accessibilità per WhatsApp desktop basato sul web

## Caratteristiche

- **Alt+1**: Vai alla lista conversazioni di Whatsapp
- **Alt+2**: Vai alla lista dei messaggi di Whatsapp
- **Alt+D**: Sposta il focus al campo di scrittura dei messaggi
- **Enter**: Riproduci i messaggi vocali (funziona nelle chat individuali e di gruppo)
- **Shift+Enter**: Apri il menu contestuale del messaggio
- **Control+C**: Copia il messaggio attuale negli appunti
- **Control+R**: Leggi il messaggio completo (clicca il pulsante "Leggi di più" se necessario)
- **Control+Shift+Enter**: Reagire al messaggio

### Scripts da attivare o disattivare (nessun tasto predefinito, configurare in "Gesti e tasti di immissione")

- Attiva / disattiva il filtraggio del numero di telefono nella lista conversazioni
- Attiva/disattiva il filtraggio dei messaggi nella lista dei messaggi
- Attiva / disattiva la modalità focus automatica (seleziona modalità navigazione se necessario)

## Scorciatoie da tastiera native di WhatsApp Desktop

- Segna come non letto: Ctrl+Shift+U
- Disattiva notifiche: Ctrl+Shift+M
- Archivia chat: Ctrl+Shift+A
- Fissa chat: Ctrl+Alt+Shift+P
- Cerca: Ctrl+Alt+/
- Cerca nella conversazione: Ctrl+Shift+F
- Nuova chat: Ctrl+Alt+N
- Chat successiva: Ctrl+]
- Chat precedente: Ctrl+[
- Aggiungi etichetta alla chat: Ctrl+Cmd+Shift+L
- Chiudi chat: Escape
- Nuovo gruppo: Ctrl+Shift+N
- Profilo e Info: Ctrl+Alt+P
- Aumenta velocità messaggio vocale: Shift+.
- Diminuisci velocità messaggio vocale: Shift+,
- Impostazioni: Alt+S
- Pannello emoji: Ctrl+Alt+E
- Pannello GIF: Ctrl+Alt+G
- Pannello sticker: Ctrl+Alt+S
- Ricerca estesa: Alt+K
- Blocca app: Alt+L
- Apri dettagli chat: Alt+I
- Blocca chat: Ctrl+Shift+B
- Rispondi: Alt+R
- Rispondi in privato: Ctrl+Alt+R
- Inoltra: Ctrl+Alt+D
- Messaggio con stella: Alt+8
- Apri menu allegati: Alt+A
- Avvia registrazione PTT: Ctrl+Alt+Shift+R
- Metti in pausa registrazione PTT: Alt+P
- Invia PTT: Ctrl+Enter
- Modifica ultimo messaggio: Ctrl+Freccia Su
- Attiva/Disattiva fotocamera: Ctrl+Alt+V
- Silenzia/Riattiva: Ctrl+Alt+M
- Reazioni: Ctrl+Alt+R
- Alza la mano: Ctrl+Alt+H
- Condivisione schermo: Ctrl+Alt+S
- Termina chiamata: Ctrl+Alt+W
- Aumenta zoom: Ctrl++
- Diminuisci zoom: Ctrl+-
- Ripristina zoom: Ctrl+0
- Apri chat: Ctrl+1..9

## Requisiti

- NVDA 2021.1 o superiore
- WhatsApp Desktop (versione basata sul web)

## Installazione

1. Scaricare il file `whatsAppNG.nvda-addon` 
2. In NVDA, andare su **Strumenti→ Gestione componenti aggiuntivi**
3. Cliccare su **Installa** e selezionare il file
4. Riavviare NVDA

## Configurazione

Il filtraggio dei numeri di telefono può essere attivato o disattivato:
- Nella lista conversazioni: Configurare il tasto rapido nella finestra "Gesti e tasti di immissione"
- Nella lista dei messaggi: configura il tasto rapido nella finestra "Gesti e tasti di immissione

Configura i tasti rapidi in:
**Menu di NVDA → Preferenze → Gesti e tasti di immissione → WhatsApp NG**

## Cronologia delle modifiche

### Versione 1.5.0 (2026-03-05)

**Aggiunto:**
- Ctrl+Shift+Invio: Reagisci al messaggio (apre menu reazioni)
- Alt+Invio: Leggi messaggio completo in modalità navigazione
- Scorciatoie da tastiera nativi WhatsApp Desktop aggiunti alla documentazione

**Cambiato:**
- Prestazioni significativamente ottimizzate: La navigazione è ora più fluida e reattiva
- Alt+2 più affidabile e preciso nella navigazione
- Ctrl+C ora funziona solo nella lista messaggi

**Corretto:**
- Ctrl+R ora legge il testo correttamente quando espande messaggi lunghi

### Versione 1.4.0 (2026-02-23)

**Aggiunto:**
- Supporto linguistico completo per: Arabo, Tedesco, Spagnolo, Italiano e Russo
- Traduzione ucraina aggiornata con le stringhe più recenti

**Risolto:**
- Errore "Testo non trovato" in Control+R dopo aver cliccato il pulsante "Leggi di più"
- Control+R ora funziona solo sui messaggi di testo (mostra "Non è un messaggio di testo" per voce/immagini)

**Modificato:**
- Link del repository aggiornati al nuovo repository (nunotfc/WhatsAppNG)
- Documentazione: Tutti i README localizzati ora includono la cronologia completa fino alla versione 1.3.0

### Versione 1.3.0 (2026-02-07)

**Aggiunto:**
- Supporto per la traduzione in turco
- Attiva/disattiva la modalità focus automatica (configura il tasto rapido nella finestra Gesti e tasti di immissione)

**Modificato:**
- Prestazioni migliorate: i comandi di navigazione sono ora più veloci nell'uso ripetuto
- Il tasto Escape ora passa a WhatsApp correttamente

**Risolto:**
- L'invio ora riproduce i messaggi video (precedentemente funzionava soltanto con gli audio)

### Versione 1.1.1 (2025-01-31)

**Aggiunto:**
- Control+R: Legge il messaggio completo (clicca il pulsante "Leggi di più" automaticamente)
- Control+C: Copia il messaggio attuale negli appunti
- Disattiva automaticamente la modalità navigazione (mantiene abilitata la modalità focus per una migliore esperienza in WhatsApp)

**Modificato:**
- Messaggi di errore migliorati: ora tutti gli scripts forniscono un chiaro feedback se qualcosa va storto
- I comandi di navigazione(Alt+1, Alt+2, Alt+D) ora rimangono muti se tutto va a buon fine
- Enter: rilevazione basata sullo slider invece che sul conteggio dei pulsanti (più affidabile)

**Risolto:**
- Alt+1 e Alt+2 segnala correttamente gli errori quando tutti i percorsi falliscono
- Ottimizzato il filtraggio oggetti per ridurre la latenza in digitazione

### Versione 1.1.0 (2025-01-30)

**Aggiunto:**
- Control+R: Leggi il messaggio completo
- Riproduzione del messaggio intelligente usando la rilevazione dello slider

**Modificato:**
- Invio: Logica migliorata utilizzando il rilevamento degli slider anziché il conteggio dei pulsanti

**Risolto:**
- Alt+2 ora tenta tutti i percorsi di navigazione se il primo tentativo non riesce

### Versione 1.0.0 (2025-01-29)

**Versione iniziale:**
- Tasti rapidi per la lista conversazioni, la lista dei messaggi, e il campo di scrittura del messaggio
- Riproduzione dei messaggi vocali con supporto alle chat individuali e di gruppo
- Accesso al menu di contesto per le azioni sui messaggi
- Attiva/disattiva il filtraggio dei numeri di telefono per la lista conversazioni e quella dei messaggi
- Attivazione della modalità focus automatica in WhatsApp desktop

## Ringraziamenti

Sviluppato da Nuno Costa per fornire migliorie di accessibilità sul nuovo WhatsApp desktop.

## Supporto

Per problemi o suggerimenti, si prega di visitare:
https://github.com/nunotfc/whatsAppNG/issues

## Compilazione delle traduzioni

Per aggiornare o compilare le traduzioni:
```bash
scons pot
```

Questo richiede l'installazione di GNU Gettext tools.
