# WhatsApp NG

NVDA-lisäosa, joka tarjoaa saavutettavuusparannuksia verkkopohjaiselle WhatsApp Desktopille.

## Ominaisuudet

* Alt+1: Siirry WhatsAppin keskustelulistaan
* Alt+2: Siirry WhatsAppin viestilistaan
* Alt+D: Siirrä kohdistus viestin syöttökenttään
* Enter: Toista ääniviesti (toimii yksityiskeskusteluissa ja ryhmissä)
* Vaihto+Enter: Avaa viestin pikavalikko
* Ctrl+C: Kopioi nykyinen viesti leikepöydälle
* Ctrl+R: Lue koko viesti (napsauttaa tarvittaessa "lue lisää" -painiketta)
* Ctrl+Vaihto+Enter: Lisää reaktio viestiin

### Tilanvaihtoskriptit (ei oletusarvoisia pikakomentoja – määritä Näppäinkomennot-valintaikkunassa)

* Puhelinnumerosuodatuksen käyttöönotto tai käytöstä poisto keskustelulistassa
* Puhelinnumerosuodatuksen käyttöönotto tai käytöstä poisto viestilistassa
* Automaattisen lomaketilan käyttöönotto tai käytöstä poisto (sallii tarvittaessa selaustilan)

## WhatsApp Desktopin alkuperäiset pikanäppäimet

* Merkitse lukemattomaksi: Ctrl+Vaihto+U
* Mykistä ilmoitukset: Ctrl+Vaihto+M
* Arkistoi keskustelu: Ctrl+Vaihto+A
* Kiinnitä keskustelu: Ctrl+Alt+Vaihto+P
* Haku: Ctrl+Alt+/
* Haku keskustelussa: Ctrl+Vaihto+F
* Uusi keskustelu: Ctrl+Alt+N
* Seuraava keskustelu: Ctrl+]
* Edellinen keskustelu: Ctrl+[
* Lisää tunniste keskusteluun: Ctrl+Vaihto+L
* Sulje keskustelu: Esc
* Uusi ryhmä: Ctrl+Vaihto+N
* Profiili ja Tietoja: Ctrl+Alt+P
* Lisää valitun ääniviestin toistonopeutta: Vaihto+.
* Vähennä valitun ääniviestin toistonopeutta: Vaihto+,
* Asetukset: Alt+S
* Emojipaneeli: Ctrl+Alt+E
* GIF-paneeli: Ctrl+Alt+G
* Tarrapaneeli: Ctrl+Alt+S
* Laajennettu haku: Alt+K
* Lukitse sovellus: Alt+L
* Avaa keskustelun tiedot: Alt+I
* Estä keskustelu: Ctrl+Vaihto+B
* Vastaa: Alt+R
* Vastaa yksityisesti: Ctrl+Alt+R
* Välitä edelleen: Ctrl+Alt+D
* Merkitse viesti tähdellä: Alt+8
* Avaa liitevalikko: Alt+A
* Aloita PTT-tallennus: Ctrl+Alt+Vaihto+R
* Keskeytä PTT-tallennus: Alt+P
* Lähetä PTT: Ctrl+Enter
* Muokkaa viimeisintä viestiä: Ctrl+Nuoli ylös
* Kamera päälle/pois: Ctrl+Alt+V
* Mykistä/poista mykistys: Ctrl+Alt+M
* Reaktiot: Ctrl+Alt+R
* Nosta käsi: Ctrl+Alt+H
* Jaa näyttö: Ctrl+Alt+S
* Lopeta puhelu: Ctrl+Alt+W
* Lähennä: Ctrl++
* Loitonna: Ctrl+-
* Palauta zoomaus: Ctrl+0
* Avaa keskustelu: Ctrl+1–9

## Vaatimukset

* NVDA 2021.1 tai uudempi
* WhatsApp Desktop (verkkopohjainen versio)

## Asennus

1. Lataa tiedosto "whatsAppNG.nvda-addon"
2. Avaa NVDA-valikko → Työkalut → Lisäosakauppa
3. Paina "Asenna ulkoisesta lähteestä" -painiketta ja valitse lataamasi tiedosto
4. Käynnistä NVDA uudelleen

## Asetusten määritys

Puhelinnumerosuodattimet voi ottaa käyttöön tai poistaa käytöstä:

* Keskustelulistassa: määritä pikanäppäin Näppäinkomennot-valintaikkunassa
* Viestilistassa: määritä pikanäppäin Näppäinkomennot-valintaikkunassa

Määritä pikanäppäimet kohdassa NVDA-valikko → Mukautukset → Näppäinkomennot → WhatsApp NG.

## Muutosloki

### Versio 1.6.0 (23.3.2026)

Lisätty:

* Vihjeiden suodatus: piilottaa automaattisesti viesti-ilmoituksista tekstit kuten "Avaa pikavalikko..." ja muut vastaavat työkaluvihjeet

  * Tukee useita kieliä
  * Voidaan ottaa käyttöön tai poistaa käytöstä painamalla NVDA+Vaihto+H

Korjattu:

* Kaksoisilmoitus keskustelulistassa: NVDA ei enää lue jokaista keskusteluriviä kahdesti nuolinäppäimillä liikuttaessa (#11)
* Siirtyminen Alt+1:llä: keskustelulistan paikantaminen on aiempaa luotettavampaa
* Viestien kopiointi: Ctrl+C:n tarkkuutta on parannettu

### Versio 1.5.0 (5.3.2026)

Lisätty:

* Ctrl+Vaihto+Enter: reagoi viestiin (avaa reaktiovalikon)
* Alt+Enter: lue koko viesti selaustilassa
* Lisätty ohjeeseen WhatsApp Desktopin alkuperäiset pikanäppäimet

Muutettu:

* Suorituskykyä on optimoitu merkittävästi: navigointi on nyt sujuvampaa ja reagoivampaa
* Alt+2-pikanäppäin toimii aiempaa luotettavammin ja täsmällisemmin
* Ctrl+C toimii nyt vain viestilistassa

Korjattu:

* Kun pitkät viestit laajennetaan, Ctrl+R lukee nyt niiden koko tekstin oikein

### Versio 1.4.0 (23.2.2026)

Lisätty:

* Täysi kielituki: arabia, saksa, espanja, italia ja venäjä
* Ukrainankielinen käännös päivitetty uusimmilla teksteillä

Korjattu:

* "Text not found" -virhe Ctrl+R-komennossa "lue lisää" -painikkeen painamisen jälkeen
* Ctrl+R toimii nyt vain tekstimuotoisissa viesteissä (ilmoittaa ääni- ja kuvaviesteille "Not a text message")

Muutettu:

* Koodivaraston linkit päivitetty uuteen (nunotfc/WhatsAppNG)
* Ohje: kaikki lokalisoidut README-tiedostot sisältävät nyt täydellisen muutoslokin versioon 1.3.0 asti

### Versio 1.3.0 (7.2.2026)

Lisätty:

* Turkin kielen tuki
* Automaattisen lomaketilan käyttöönotto ja käytöstä poisto (määritä pikanäppäin Näppäinkomennot-valintaikkunassa)

Muutettu:

* Suorituskykyä on parannettu: navigointikomennot ovat nyt nopeampia toistuvassa käytössä
* Esc-näppäin välittyy nyt oikein WhatsAppille

Korjattu:

* Enter toistaa nyt videoviestit (toimi aiemmin vain ääniviesteillä)

### Versio 1.1.1 (31.1.2025)

Lisätty:

* Ctrl+R: lue koko viesti (napsauttaa automaattisesti "lue lisää" -painiketta)
* Ctrl+C: kopioi nykyinen viesti leikepöydälle
* Selaustilan automaattinen käytöstä poisto (pitää lomaketilan käytössä paremman WhatsApp-kokemuksen vuoksi)

Muutettu:

* Virheilmoituksia on parannettu: kaikki skriptit antavat nyt selkeän palautteen epäonnistumisesta
* Navigointikomentojen (Alt+1, Alt+2 ja Alt+D) suorittamisen onnistuessa ei puhuta mitään
* Enter: liukusäätimeen perustuva tunnistus painikkeiden laskemisen sijaan (luotettavampi)

Korjattu:

* Alt+1 ja Alt+2 ilmoittavat nyt virheet oikein, kun kaikki polut epäonnistuvat
* Kohteiden suodatusta on optimoitu syötetyn viiveen vähentämiseksi

### Versio 1.1.0 (30.1.2025)

Lisätty:

* Ctrl+R: lue koko viesti
* Ääniviestien toisto älykkäällä liukusäädintunnistuksella

Muutettu:

* Enter: parannettu logiikka, jossa käytetään liukusäädintunnistusta painikkeiden laskemisen sijaan

Korjattu:

* Alt+2 yrittää nyt oikein kaikkia navigointipolkuja, jos ensimmäinen yritys epäonnistuu

### Versio 1.0.0 (29.1.2025)

Ensimmäinen julkaisu:

* Navigointipikanäppäimet keskustelulistaan, viestilistaan ja viestin kirjoituskenttään siirtymistä varten
* Ääniviestien toisto, tuki yksityiskeskusteluille ja ryhmille
* Viestitoimintojen pikavalikon avaaminen
* Puhelinnumerosuodatuksen käyttöönotto ja käytöstä poisto keskusteluissa ja viesteissä
* Automaattinen lomaketilan käyttöönotto WhatsApp Desktopissa

## Tekijät

Kehittäjä: Nuno Costa. Tavoitteena on tarjota saavutettavuusparannuksia nykyaikaiseen WhatsApp Desktop -kokemukseen.

## Tuki

Ongelmia tai ehdotuksia varten:
https://github.com/nunotfc/whatsAppNG/issues

## Käännösten kokoaminen

Käännösten päivittäminen tai kokoaminen:

scons pot

Tämä edellyttää GNU Gettext -työkalujen asentamista.
