TRANSLATIONS = {
    0: """# Tiedostojärjestelmä ja syöte/tuloste (IO) {#sec-filesystem}

Tässä luvussa käsittelemme, miten voit suorittaa tiedostojärjestelmäoperaatioita
ja käsitellä syötettä ja tulostetta (IO) Zig Standard Libraryn alustariippumattomien structien ja funktioiden avulla.
Useimmat näistä funktioista ja structeista
tulevat `std.Io`-moduulista.

## Syötteen ja tulosteen perusteet {#sec-io-basics}

Jos sinulla on kokemusta korkean tason ohjelmointikielistä, olet varmasti käyttänyt
jossain vaiheessa syöte- tai tulostetoimintoja. Toisin sanoen olet varmasti
ollut tilanteessa, jossa sinun täytyi lähettää tulostetta käyttäjälle tai vastaanottaa syötettä
ohjelmasi käyttäjältä.

Esimerkiksi Pythonissa voimme vastaanottaa käyttäjän syötettä `input()`-sisäänrakennetulla
funktiolla. Voimme myös tulostaa (tai "näyttää") tulostetta käyttäjälle `print()`-
sisäänrakennetulla funktiolla. Jos olet ohjelmoinut Pythonilla aiemmin, olet varmasti
käyttänyt näitä funktioita ainakin kerran.

Mutta tiedätkö, miten nämä funktiot liittyvät käyttöjärjestelmääsi (OS)? Miten ne tarkalleen ottaen
vuorovaikuttavat käyttöjärjestelmäsi resurssien kanssa vastaanottaakseen tai lähettääkseen syötettä/tulostetta?
Pohjimmiltaan korkean tason kielten syöte/tuloste-funktiot ovat vain abstraktioita
käyttöjärjestelmän *standard output*- ja *standard input* -kanavien päällä.

Tämä tarkoittaa, että vastaanotamme syötteen tai lähetämme tulosteen käyttöjärjestelmän kautta.
Käyttöjärjestelmä muodostaa sillan käyttäjän ja ohjelmasi välille. Ohjelmallasi
ei ole suoraa pääsyä käyttäjään. Käyttöjärjestelmä välittää kaikki
ohjelmasi ja käyttäjän väliset viestit.

Käyttöjärjestelmän *standard output*- ja *standard input* -kanavia kutsutaan yleisesti
`stdout`- ja `stdin`-kanaviksi. Joissakin yhteyksissä niitä kutsutaan myös
*standard output device*- ja *standard input device* -laitteiksi. Kuten nimestä voi päätellä,
*standard output* on kanava, josta tuloste virtaa, kun taas *standard input*
on kanava, johon syöte virtaa.

Lisäksi käyttöjärjestelmät luovat yleensä erillisen kanavan virheviestien vaihtoon, jota kutsutaan
*standard error* -kanavaksi eli `stderr`-kanavaksi. Tähän kanavaan virhe- ja varoitusviestit
yleensä lähetetään. Nämä viestit näytetään usein terminaalissa punertavissa tai oranssin sävyisissä väreissä.

Yleensä jokainen käyttöjärjestelmä (esim. Windows, macOS, Linux jne.) luo erillisen ja oman joukon
*standard output*-, *standard error*- ja *standard input* -kanavia jokaiselle tietokoneellasi käynnissä olevalle ohjelmalle (tai prosessille).
Tämä tarkoittaa, että jokaisella kirjoittamallasi ohjelmalla on oma `stdin`, `stderr` ja `stdout`, jotka ovat erillään
muiden käynnissä olevien ohjelmien ja prosessien `stdin`-, `stderr`- ja `stdout`-kanavista.

Tämä on käyttöjärjestelmäsi käyttäytymistä. Se ei tule käyttämästäsi ohjelmointikielestä.
Kuten sanoin aiemmin, ohjelmointikielten syöte ja tuloste, erityisesti
korkean tason kielissä, ovat yksinkertainen abstraktio nykyisen käyttöjärjestelmäsi `stdin`-, `stderr`- ja `stdout`-kanavien päällä.
Eli käyttöjärjestelmäsi on välittäjä jokaisessa ohjelmasi syöte/tuloste-operaatiossa
riippumatta käyttämästäsi ohjelmointikielestä.




## Writer- ja reader-malli {#sec-writer-reader}

Zigissä syötteen ja tulosteen (IO) ympärillä on tietty malli. En (kirjan kirjoittaja) tiedä, onko tälle mallille
virallista nimeä. Mutta tässä kirjassa kutsun sitä "writer- ja reader-malliksi".
Pohjimmiltaan jokainen IO-operaatio Zigissä tehdään joko `Reader`- tai `Writer`-olion kautta[^gen-zig].

Nämä kaksi datatyyppiä ovat itse asiassa rajapintoja, ja ne tulevat Zig Standard Libraryn `std.Io`-moduulista. Kuten nimistä voi päätellä,
`Reader` on olio, joka tarjoaa työkaluja datan lukemiseen "jostakin" (tai "jostakin paikasta"), kun taas `Writer`
tarjoaa työkaluja datan kirjoittamiseen tähän "johonkin". Tämä "jokin" voi olla eri asioita: esimerkiksi
tiedostojärjestelmässä oleva tiedosto; tai verkkopistoke järjestelmässäsi[^sock]; tai
jatkuva datavirta, kuten järjestelmän standard input -laite, joka saattaa jatkuvasti
vastaanottaa uutta dataa käyttäjiltä, tai toisena esimerkkinä pelin live-chat, joka jatkuvasti
vastaanottaa ja näyttää uusia viestejä pelaajilta.

[^gen-zig]: Aiemmin näitä olioita kutsuttiin `GenericReader`- ja `GenericWriter`-olioiksi. Molemmat tyypit poistettiin käytöstä versiossa 0.15.
[^sock]: @sec-create-socket-osiossa luodut pistokeoliot ovat esimerkkejä verkkopistokkeista.

Jos haluat **lukea** dataa jostakin tai jostakin paikasta, sinun täytyy käyttää `Reader`-oliota.
Mutta jos haluat sen sijaan **kirjoittaa** dataa tähän "johonkin", sinun täytyy käyttää `Writer`-oliota.
Molemmat näistä olioista luodaan yleensä file descriptor -oliosta. Tarkemmin sanottuna `writer()`- ja `reader()`-
metodien kautta tästä file descriptor -oliosta. Jos et tunne file descriptoreita, siirry seuraavaan osioon.

Jokaisella `Writer`-oliolla on metodeja kuten `print()`, jolla voit kirjoittaa/lähettää muotoillun merkkijonon
(eli tämä muotoiltu merkkijono on kuin Pythonin `f`-merkkijono tai C:n `printf()`-funktio)
käyttämääsi "johonkin" (tiedosto, pistoke, virta jne.). Sillä on myös `writeAll()`-metodi, jolla voit
kirjoittaa merkkijonon tai tavutaulukon "johonkin".

Vastaavasti jokaisella `Reader`-oliolla on metodeja kuten `readSliceAll()`, jolla voit lukea
dataa "jostakin" (tiedosto, pistoke, virta jne.), kunnes se täyttää tietyn taulukko- (eli "puskuri")-olion.
Toisin sanoen, jos annat `readSliceAll()`-metodille 300 `u8`-arvon taulukon, metodi yrittää lukea 300 tavua
dataa "jostakin" ja tallentaa ne antamaasi taulukkoon.

Toinen hyödyllinen metodi on `takeDelimiterExclusive()`. Tässä metodissa määrittelet "erotinmerkin".
Ideana on, että funktio yrittää lukea mahdollisimman monta tavua dataa "jostakin",
kunnes se löytää määrittämäsi erotinmerkin, ja palauttaa datan sisältävän viipaleen sinulle.


Tämä on vain nopea kuvaus näiden oliotyyppien metodeista. Suosittelen kuitenkin lukemaan virallisen dokumentaation sekä
[`Writer`](https://ziglang.org/documentation/master/std/#std.Io.Writer)[^gen-write]- että
[`Reader`](https://ziglang.org/documentation/master/std/#std.Io.Reader)[^gen-read]-tyypeistä.
On myös hyvä idea lukea Zig Standard Libraryn moduulien lähdekoodi,
jotka määrittelevät näiden olioiden metodit, eli
[`Reader.zig`](https://codeberg.org/ziglang/zig/src/branch/master/lib/std/Io/Reader.zig)[^mod-read]
ja [`Writer.zig`](https://codeberg.org/ziglang/zig/src/branch/master/lib/std/Io/Writer.zig)[^mod-write].

[^gen-read]: <https://ziglang.org/documentation/master/std/#std.Io.Reader>.
[^gen-write]: <https://ziglang.org/documentation/master/std/#std.Io.Writer>.
[^mod-read]: <https://codeberg.org/ziglang/zig/src/branch/master/lib/std/Io/Reader.zig>.
[^mod-write]: <https://codeberg.org/ziglang/zig/src/branch/master/lib/std/Io/Writer.zig>.



## Uusi `io`-argumentti {#sec-new-io-backend}

Zig 0.15:stä lähtien Zigin kehitystiimi aloitti liikkeen, jolla muutettiin kokonaan tapa, jolla IO-operaatiot tehdään Zigissä.
Tämän suuren muutoksen myötä kieleen tuotiin täysin uusi IO-rajapinta, eli @sec-writer-reader-osiossa kuvatut `Reader`- ja `Writer`-
rajapinnat. Sen lisäksi Zig 0.16:sta lähtien uuteen IO-rajapintaan tehtiin uusi suuri askel
uuden `io`-argumentin käyttöönotolla, josta voit valita käytettävän "IO-backend-toteutuksen",
kuten `std.Io.Evented`, `std.Io.Threaded` ja muita.

Tehdään nopea vertailu. Olet todennäköisesti huomannut @sec-memory-chap-osiossa, että allokaattorit ovat olennainen olion tyyppi Zigissä.
Ne esiintyvät kaikkialla, ja ne ovat välttämättömiä kaikissa tehtävissä, jotka tarvitsevat muistin varaamista
valmistuakseen. Uuden IO-rajapinnan myötä "IO-backend-toteutuksen" valinnasta tuli myös olennainen
tehtävä Zig-koodissa, aivan kuten allokaattorin valinta.

Nyt aloitat Zig-koodisi yleensä valitsemalla sekä allokaattorin että käytettävän "IO-backend-toteutuksen".
Alla olevassa esimerkissä valitsen IO-toteutuksen, joka perustuu säietiloihin. Voisin myös (jos haluaisin) käyttää
`std.Io.Evented`-toteutusta, joka perustuu jonorengaisiin.

Alla olevan koodinpätkän keskeiset oliot ovat `allocator` ja `io`.""",
    1: """\n\n\nZig 0.16:sta lähtien löydät Zig Standard Librarystä eri funktioita, jotka suorittavat IO-operaatioita ja
ottavat argumentin nimeltä `io`, jonka tyyppi on `std.Io`. Hyvä esimerkki on `std.Io.File`-tyypin `reader()`-metodi. Tämä metodi on vastuussa
`Reader`-olion luomisesta, jonka kautta voit lukea dataa `std.Io.File`-olion edustamasta tiedostosta.
Ja tällä metodilla on nyt `io`-argumentti, johon sinun pitäisi antaa "IO-backend-toteutus", jota
haluat käyttää tiedostoa lukiessasi.

Alla olevassa esimerkissä demonstroin tämän `io`-argumentin käyttöä avaamalla tiedoston tietokoneellani ja lukemalla sen. Huomaa, että annan
"IO-backend-toteutuksen" (eli `io`-olion) `reader()`-metodille. Tämä on vain yksi
esimerkki. Löydät tämän "IO-backend-toteutuksen antamisen" mallin monista muistakin tehtävistä.
Verkkoihin liittyvät funktiot ovat toinen tapaus, jossa näet usein tämän `io`-argumentin.
""",
    2: """\n\n\n## Oletusarvoisen IO-toteutuksen käyttö\n\nJoskus on vaivalloista kirjoittaa kaikki tarvittava koodi IO-toteutuksen
asianmukaiseen luomiseen. Ja joskus et oikeastaan välitä siitä, miten IO-operaatiot tehdään konepellon alla,
vaan haluat vain käyttää IO-backendiä oletusasetuksilla. Jos näin on,
on tällä hetkellä kolme helppoa tapaa saada nopeasti IO-backend oletusasetuksilla:

- käytä kohdekonfiguraation oletusarvoista IO-toteutusta.
- käytä yksisäikeistä IO-toteutusta oletuskonfiguraatiolla.
- käytä `std.testing`-moduulin IO-toteutusta.


### `std.testing`-moduulin IO-toteutuksen käyttö

Kuten nimestä voi päätellä, `std.testing`-moduulin IO-toteutusta pitäisi
käyttää vain "yksikkötestien kontekstissa". Jos yrität käyttää sitä missä tahansa muussa kontekstissa,
päädyt yleensä käännösvirheeseen.
""",
    3: """\n\n\n### Yksisäikeisen IO-toteutuksen käyttö\n\nYksisäikeisen IO-toteutuksen saaminen on helppoa ja nopeaa.
Sinun tarvitsee vain luoda `std.Io.Threaded`-olio arvolla
`.init_single_threaded` ja kutsua sitten syntyneen
olion `io()`-metodia, kuten alla oleva koodiesimerkki osoittaa:
""",
    4: """\n\n### Kohteesi oletusarvoisen IO-toteutuksen käyttö\n\nUudemmissa Zig-versioissa main-funktiolle otettiin käyttöön uusi "oletusargumentti",
joka on `init`-argumentti. Yhteenvetona voit kirjoittaa main-funktion, joka vastaanottaa
`std.process.Init`-tyyppisen olion syötteenä.

`std.process.Init`-olio on pohjimmiltaan olio, joka sisältää joukon valmiiksi alustettuja
API-rajapintoja, joita ohjelmasi voi hyödyntää. Voit käyttää tätä argumenttia saadaksesi helposti ennalta määritellyn
ja valmiiksi alustetun IO-toteutuksen IO-operaatioillesi. Tämä toteutus on käytettävissä
tämän `init`-argumentin `io`-attribuutissa.
""",
    5: """


## File descriptorien esittely {#sec-file-descriptor}

"File descriptor" -olio on keskeinen osa jokaista IO-operaatiota, joka tehdään missä tahansa käyttöjärjestelmässä (OS).
Tällainen olio on tunniste tietylle käyttöjärjestelmäsi syöte/tuloste (IO) -resurssille [@wiki_file_descriptor].
Se kuvaa ja tunnistaa tämän resurssin. IO-resurssi voi olla:

- olemassa oleva tiedosto tiedostojärjestelmässäsi.
- olemassa oleva verkkopistoke.
- muita virtakanavatyyppejä.
- putki (pipe) terminaalissasi[^pipes].

[^pipes]: Putki on mekanismi prosessien väliseen kommunikaatioon tai prosessien väliseen IO:hon. Voit tulkita putken myös "joukkona prosesseja, jotka on ketjutettu yhteen järjestelmän standard input/output -laitteiden kautta". Linuxissa esimerkiksi putki luodaan terminaalissa yhdistämällä kaksi tai useampia terminaalikomentoa "pipe"-merkillä (`|`).

Yllä olevista luettelomerkeistä näemme, että vaikka termissä on sana "file",
"file descriptor" voi kuvata muutakin kuin pelkkää tiedostoa.
Tämä "file descriptor" -käsite tulee Portable Operating System Interface (POSIX) -API:sta,
joka on joukko standardeja, jotka ohjaavat, miten käyttöjärjestelmät ympäri maailmaa tulisi toteuttaa
yhteensopivuuden säilyttämiseksi.

File descriptor ei vain tunnista IO-resurssia, jota käytät datan vastaanottamiseen tai lähettämiseen,
vaan se kuvaa myös, missä tämä resurssi sijaitsee ja mitä IO-tilaa resurssi käyttää tällä hetkellä.
Esimerkiksi tämä IO-resurssi saattaa käyttää vain "read"-IO-tilaa, mikä tarkoittaa, että resurssi
on avoinna "lukuoperaatioille", kun taas "kirjoitusoperaatiot" eivät ole sallittuja.
Nämä IO-tilat ovat pohjimmiltaan samoja tiloja, jotka annat `mode`-argumentille
C:n `fopen()`-funktiossa ja Pythonin `open()`-sisäänrakennetussa funktiossa.

C:ssä "file descriptor" on `FILE`-osoitin, mutta Zigissä file descriptor on `File`-olio.
Tämä datatyyppi (`File`) on kuvattu Zig Standard Libraryn `std.fs`-moduulissa.
Emme yleensä luo `File`-oliota suoraan Zig-koodissamme. Sen sijaan saamme tällaisen olion tuloksena, kun
avaamme IO-resurssin. Toisin sanoen pyydämme yleensä käyttöjärjestelmää avaamaan tietyn IO-resurssin meille,
ja jos käyttöjärjestelmä avaa resurssin onnistuneesti, se palauttaa meille
file descriptorin tähän resurssiin.

Saat siis yleensä `File`-olion käyttämällä Zig Standard Libraryn funktioita ja metodeja,
jotka pyytävät käyttöjärjestelmää avaamaan jonkin IO-resurssin, kuten `openFile()`-metodia, joka avaa tiedoston
tiedostojärjestelmässä. @sec-create-socket-osiossa luotu `std.Io.net.Stream`-olio on myös eräänlainen
file descriptor -olio.


### *Standard output* {#sec-standard-output}

Olet jo nähnyt tässä kirjassa, miten voimme käyttää erityisesti `stdout`-kanavaa Zigissä
lähettääksemme tulostetta käyttäjälle.
Tätä varten käytämme `std.Io`-moduulin `File.stdout()`-funktiota. Tämä funktio palauttaa
file descriptorin, joka kuvaa nykyisen käyttöjärjestelmäsi `stdout`-kanavaa. Tämän file descriptor -olion kautta
voimme lukea tai kirjoittaa ohjelmamme `stdout`-kanavaan.

Vaikka voimme lukea `stdout`-kanavaan tallennettua dataa, kirjoitamme yleensä vain
(tai "tulostamme") dataa tähän kanavaan. Syy on hyvin samanlainen kuin @sec-read-http-message-osiossa,
jossa käsittelimme, mitä "lukeminen" vs. "kirjoittaminen" pienen HTTP-palvelinprojektimme yhteysolioon tarkoittaisi.

Kun kirjoitamme dataa kanavaan, lähetämme käytännössä dataa kanavan toiseen päähän.
Vastoin tätä, kun luemme dataa kanavasta, luemme kanavan kautta lähetettyä dataa. Koska `stdout` on kanava tulosteen lähettämiseen käyttäjälle, keskeinen verbi tässä
on **lähettää**. Haluamme lähettää jotain jollekulle, ja seurauksena haluamme **kirjoittaa** jotain
johonkin kanavaan.

Siksi kun käytämme `File.stdout()`-funktiota, käytämme useimmiten myös `stdout` file descriptorin `writer()`-metodia
saadaksemme writer-olion, jolla voimme kirjoittaa dataa tähän `stdout`-kanavaan.
Kuten kuvasimme @sec-writer-reader-osiossa, tämä `writer()`-metodi palauttaa `Writer`-olion, ja yksi
tämän `Writer`-olion päämetodeista on `print()`-metodi, jota olemme käyttäneet laajasti tässä kirjassa
kirjoittaaksemme (tai "tulostaaksemme") muotoillun merkkijonon `stdout`-kanavaan.

Huomaa myös alla olevassa esimerkissä, että `Writer`-olion luomiseksi
meidän täytyy antaa viite puskuriolioon syötteenä `writer()`-metodille. Alla olevassa esimerkissä
tämä puskuriolio on `stdout_buffer`. Kun annamme tällaisen puskurin, muutamme `Writer`-olion suorittamat IO-operaatiot "puskuroiduiksi IO-operaatioiksi". Puhumme "puskuroidusta IO:sta" lisää @sec-buffered-io-osiossa,
joten älä huoli siitä liikaa toistaiseksi.

""",
    6: """




Tämä `Writer`-olio on kuin mikä tahansa muu writer-olio, jonka yleensä saat file descriptor -oliosta.
Samoja writer-olion metodeja, joita käyttäisit esimerkiksi tiedostojärjestelmään kirjoittaessasi, voit käyttää
myös tässä `stdout` file descriptor -oliosta, ja päinvastoin.


### *Standard input*

Voit käyttää *standard input* -kanavaa (eli `stdin`) Zigissä `std.Io`-moduulin `File.stdin()`-funktiolla.
Kuten sen "veli" (`File.stdout()`), tämä funktio palauttaa myös file descriptor -olion, joka kuvaa käyttöjärjestelmäsi `stdin`-kanavaa.

Koska haluamme vastaanottaa syötettä käyttäjältä, keskeinen verbi tässä on **vastaanottaa**, ja seurauksena
haluamme yleensä **lukea** dataa `stdin`-kanavasta kirjoittamisen sijaan. Käytämme siis yleensä
`File.stdin()`-funktion palauttaman file descriptor -olion `reader()`-metodia saadaksemme `Reader`-
olion, jolla voimme lukea dataa `stdin`-kanavasta.

Alla olevassa esimerkissä yritämme lukea dataa `stdin`-kanavasta `takeDelimiterExclusive()`-metodilla
(joka lukee kaiken datan `stdin`-kanavasta, kunnes se kohtaa rivinvaihtomerkin - `'
'` - virrassa),
ja tallennamme tämän datan `name`-olioon.

Huomaa myös, että kuten `writer()`-metodin kanssa, meidän täytyy antaa viite puskuriolioon
syötteenä `reader()`-metodille, kun luomme `Reader`-oliomme. Syyt ovat täsmälleen samat.
Tämä syötepuskuri muuttaa `Reader`-olion suorittamat IO-operaatiot "puskuroiduiksi IO-operaatioiksi".

Jos suoritat tämän ohjelman, huomaat, että se pysäyttää suorituksen ja alkaa odottaa rajattomasti
käyttäjän syötettä. Toisin sanoen sinun täytyy kirjoittaa nimesi terminaaliin ja painaa Enter
lähettääksesi nimesi `stdin`-kanavaan. Kun olet lähettänyt nimesi `stdin`-kanavaan, ohjelma lukee syötteen ja jatkaa suoritusta
tulostamalla annetun nimen `stdout`-kanavaan. Alla olevassa esimerkissä kirjoitin nimeni (Pedro) terminaaliin ja painoin Enter.


""",
    7: """


### *Standard error*

*Standard error* (eli `stderr`) toimii täsmälleen samalla tavalla kuin `stdout` ja `stdin`.
Kutsut vain `std.Io`-moduulin `File.stderr()`-funktiota, ja saat file descriptorin `stderr`-kanavaan.
Ihannetilanteessa kirjoitat `stderr`-kanavaan vain virhe- tai varoitusviestejä, koska tämä on
tämän kanavan tarkoitus.





## Puskuroitu IO {#sec-buffered-io}

Kuten kuvasimme @sec-io-basics-osiossa, käyttöjärjestelmä suorittaa syöte/tuloste (IO) -operaatiot suoraan.
Käyttöjärjestelmä hallinnoi IO-resurssia, jota haluat käyttää IO-operaatioihisi.
Tämän seurauksena IO-operaatiot perustuvat vahvasti järjestelmäkutsuihin (eli käyttöjärjestelmän suoraan kutsumiseen).

Selvyyden vuoksi: järjestelmäkutsuissa ei ole mitään erityisen vikaa. Käytämme niitä koko ajan
missä tahansa vakavassa matalan tason kielen koodipohjassa. Järjestelmäkutsut ovat kuitenkin
aina monta kertalukua hitaampia kuin monet muut operaatiotyyppiset operaatiot.

On siis täysin ok käyttää järjestelmäkutsua silloin tällöin. Mutta kun järjestelmäkutsuja käytetään usein,
huomaat useimmiten selvästi suorituskyvyn heikkenemisen sovelluksessasi. Hyvä nyrkkisääntö
on käyttää järjestelmäkutsua vain tarvittaessa ja vain harvoin, jotta
järjestelmäkutsujen määrä pysyy minimissä.


### Puskuroidun IO:n toiminnan ymmärtäminen

Puskuroitu IO on strategia paremman suorituskyvyn saavuttamiseksi. Sitä käytetään vähentämään IO-operaatioiden tekemiä järjestelmäkutsuja ja
saavuttamaan siten paljon parempi suorituskyky. @fig-unbuffered-io- ja @fig-buffered-io-kaavioissa näet kaksi eri kaaviota,
jotka esittävät eron lukemistoimintojen välillä puskuroimattomassa IO-ympäristössä vs. puskuroitussa IO-ympäristössä.

Antaaksemme paremman kontekstin näille kaavioille, oletetaan, että tiedostojärjestelmässämme on tekstitiedosto, joka sisältää kuuluisan Lorem ipsum -tekstin[^lorem].
Oletetaan myös, että @fig-unbuffered-io- ja @fig-buffered-io-kaaviot
näyttävät lukemistoimintoja, joita suoritamme lukeaksemme Lorem ipsum -tekstin tästä tekstitiedostosta.
Ensimmäinen asia, jonka huomaat näistä kaavioista, on se, että puskuroimattomassa ympäristössä
lukemistoiminnot johtavat moniin järjestelmäkutsuihin.
Tarkemmin sanottuna @fig-unbuffered-io-kaaviossa saamme yhden järjestelmäkutsun jokaista tiedostosta lukemaamme tavua kohden.
Toisaalta @fig-buffered-io-kaaviossa meillä on vain yksi järjestelmäkutsu aivan alussa.

Kun käytämme puskuroitua IO-järjestelmää, ensimmäisessä lukemistoiminnossa käyttöjärjestelmä lähettää ensin tavujen palan tiedostosta puskuriolioon (eli taulukkoon)
sen sijaan, että lähettäisi yhden tavun suoraan ohjelmaamme.
Tämä tavujoukko välimuistitetaan/tallennetaan tähän puskuriolioon.

Tästä eteenpäin jokaisessa uudessa lukemistoiminnossa lukemistoiminto ohjataan puskuriolioon sen sijaan,
että tehtäisiin uusi järjestelmäkutsu seuraavan tavun pyytämiseksi käyttöjärjestelmältä. Puskurissa on
seuraava tavu jo välimuistissa valmiina.


[^lorem]: <https://www.lipsum.com/>.


![Puskuroimaton IO](./../Figures/unbuffered-io.png){#fig-unbuffered-io width=60%}

![Puskuroitu IO](./../Figures/buffered-io.png){#fig-buffered-io}



Tämä on puskuroitujen IO-järjestelmien peruslogiikka. Puskuriolion koko riippuu useista tekijöistä. Se on yleensä
yhtä suuri kuin täysi muistisivu (4096 tavua). Jos noudatamme tätä logiikkaa, käyttöjärjestelmä lukee tiedoston ensimmäiset 4096 tavua
ja välimuistittaa ne puskuriolioon. Niin kauan kuin ohjelmasi ei kuluta kaikkia näitä 4096 tavua puskurista,
et luo uusia järjestelmäkutsuja.

Kun kuitenkin kulutat kaikki nämä 4096 tavua puskurista, puskurissa ei ole enää tavuja jäljellä.
Tässä tilanteessa tehdään uusi järjestelmäkutsu pyytääksemme käyttöjärjestelmältä seuraavat 4096 tavua tiedostosta, ja jälleen
nämä tavut välimuistitetaan puskuriolioon, ja sykli alkaa alusta.


::: {.callout-tip}
Yleisesti ottaen sinun pitäisi aina käyttää puskuroitua IO-reader- tai puskuroitua IO-writer-oliota koodissasi.
Ne tarjoavat paremman suorituskyvyn IO-operaatioillesi.
:::




### Puskuroidun IO:n käyttö Zigissä

Aiemmin IO-operaatiot Zigissä eivät olleet oletuksena puskuroituja. Uuden IO-rajapinnan myötä, joka otettiin käyttöön Zig 0.15:ssä,
`Reader`- ja `Writer`-rajapinnat ottavat puskuriolion syötteenä luotaessa, kuten demonstroimme @sec-standard-output-osiossa.
Toisin sanoen puskuriolio täytyy antaa `Reader`- tai `Writer`-olion luomiseksi koodissasi. Sen ansiosta
meillä on puskuroituja IO-operaatioita oletuksena Zigin uusimmissa versioissa.

Jos vertaat sitä muihin kieliin, huomaat, että Zig ottaa hieman erilaisen lähestymistavan "puskuroituun IO-strategiaansa". Jos otamme esimerkiksi C:n, C:n `FILE`-osoittimen kautta tehdyt IO-operaatiot ovat oletuksena puskuroituja. C:ssä sinun ei kuitenkaan tarvitse antaa puskurioliota eksplisiittisesti `FILE`-osoitetta luotaessa,
koska puskuriolio luodaan taustalla puolestasi ja on siten ohjelmoijalle näkymätön. Zigissä sinun täytyy
luoda tämä puskuriolio itse manuaalisesti.

Zig ei siis vain valinnut puskuroitua IO:ta, vaan se antoi myös ohjelmoijalle täyden hallinnan näissä operaatioissa käytettävästä puskurista.
Sinä (ohjelmoijana) voit hallita suoraan puskurin kokoa ja myös sitä, miten tämä tietty puskuriolio
varataan koodissasi (eli voit varata sen joko pinolle tai käyttää `Allocator`-oliota keon varaamiseen),
mikä sopii erittäin hyvin Zigin "ei piilotettuja allokaatioita" -mantraan.

Jos haluat käyttää puskuroitua IO:ta Zigissä, varmista vain, että annat viitteen puskuriolioon syötteenä joko `writer()`- tai `reader()`-
metodille luodaksesi `Writer`- tai `Reader`-olion, joka suorittaa puskuroituja IO-operaatioita oletuksena.


### Älä unohda flushata!

Kun käytät puskuroituja IO-operaatioita koodissasi, on tärkeää olla unohtamatta puskurien tyhjentämistä (flush), erityisesti kirjoitusoperaatioissa.
Pohjimmiltaan puskuroitua IO-skenaariossa, kun yritämme kirjoittaa dataa "johonkin", data kirjoitetaan ensin IO-puskuriin, jonka annoimme
`Writer`-oliolle syötteenä, ja tämä IO-puskurin data kirjoitetaan "johonkin" vasta, kun "commitoimme" sen.
"Commitoimme" IO-puskuriin kirjoitetut tavut kohdetulosteeseen "tyhjentämällä IO-puskurimme".

Kun tyhjennämme IO-puskurimme, commitoimme käytännössä IO-puskurissa olevan datapalasen
kirjoitettavaksi file descriptor -oliomme kuvaamaan IO-resurssiin. Jos emme tyhjennä IO-puskuria,
data ei koskaan poistu IO-puskurista (eli se ei koskaan pääse IO-resurssiin). Siksi kun unohdat tyhjentää IO-
resurssisi, useimmiten tapahtuu se, ettei IO-resurssissa näy mitään tulostetta.

Esimerkiksi jos kirjoitat dataa `stdout`-kanavaan ja unohdat tyhjentää sen, yleensä
terminaaliin ei kirjoitu mitään tulostetta. Ohjelma näyttää suorittuvan onnistuneesti, mutta et saa mitään
visuaalista vahvistusta terminaalissa, ja hämmentyt.

Jos kirjoitat dataa Zigissä, älä unohda tyhjentää IO-puskureitasi kutsumalla `Writer`-oliosi `flush()`-metodia.
Tämä varmistaa, että kirjoittamasi tavut/data kirjoitetaan todella file descriptor -oliosi kuvaamaan IO-resurssiin.

::: {.callout-important}
Jos kirjoitat dataa, älä unohda tyhjentää IO-puskuriasi kutsumalla `Writer`-oliosi `flush()`-metodia.
:::



## Tiedostojärjestelmän perusteet

Nyt kun olemme käsitelleet syöte/tuloste-operaatioiden perusteet Zigissä, meidän täytyy
puhua tiedostojärjestelmien perusteista, jotka ovat toinen keskeinen osa mitä tahansa käyttöjärjestelmää.
Tiedostojärjestelmät liittyvät myös syötteeseen ja tulosteeseen, koska tietokoneeseemme tallentamiamme ja luomiamme tiedostoja
pidetään IO-resursseina, kuten kuvasimme @sec-file-descriptor-osiossa.


### Nykyisen työhakemiston (CWD) käsite

Nykyinen työhakemisto (current working directory) on kansio tietokoneellasi, johon olet tällä hetkellä "juurtunut".
Toisin sanoen se on kansio, jota ohjelmasi tällä hetkellä katsoo.
Aina kun suoritat ohjelman, ohjelma työskentelee aina
tietyn kansion kanssa tietokoneellasi. Ohjelma etsii aluksi aina tästä kansiosta
pyytämiäsi tiedostoja, ja se tallentaa aluksi myös kaikki tiedostot, jotka pyydät sitä tallentamaan.

Työhakemisto määräytyy kansiosta, josta käynnistät ohjelmasi
terminaalissa. Toisin sanoen, jos olet käyttöjärjestelmäsi terminaalissa ja
suoritat binääritiedoston (eli ohjelman) tästä terminaalista, kansio, johon terminaalisi
osoittaa, on suoritettavan ohjelmasi nykyinen työhakemisto.

@fig-cwd:ssä on esimerkki ohjelman suorittamisesta terminaalista. Suoritamme
`zig`-kääntäjän kääntämää ohjelmaa kääntämällä `hello.zig`-nimisen Zig-moduulin.
CWD tässä tapauksessa on `zig-book`-kansio. Toisin sanoen, kun `hello.zig`-ohjelma
suoritetaan, se katsoo `zig-book`-kansiota, ja kaikki tässä ohjelmassa suorittamamme tiedosto-operaatiot
käyttävät tätä `zig-book`-kansiota "lähtökohtana" tai "keskipisteenä".

![Ohjelman suorittaminen terminaalista](./../Figures/cwd.png){#fig-cwd}

Vaikka olemme juurtuneet tiettyyn kansioon (@fig-cwd:n tapauksessa `zig-book`-kansioon) tietokoneellamme,
se ei tarkoita, etteikö voisimme käyttää tai kirjoittaa resursseja muissa sijainneissa.
Nykyisen työhakemiston (CWD) mekanismi määrittää vain, mistä ohjelmasi etsii ensin
pyytämiäsi tiedostoja. Tämä ei estä sinua käyttämästä tiedostoja, jotka sijaitsevat
muualla tietokoneellasi. Jos haluat käyttää tiedostoa kansiossa, joka ei ole nykyinen
työhakemistosi, sinun täytyy antaa polku kyseiseen tiedostoon tai kansioon.


### Polkujen käsite

Polku on pohjimmiltaan sijainti. Se osoittaa sijainnin tiedostojärjestelmässäsi. Käytämme
polkuja kuvaamaan tiedostojen ja kansioiden sijainteja tietokoneellamme.
Tärkeä piirre poluissa on, että ne kirjoitetaan aina merkkijonojen sisään,
eli ne annetaan aina tekstiarvoina.

Voit antaa mille tahansa ohjelmalle missä tahansa käyttöjärjestelmässä kahdenlaisia polkuja: suhteellisen polun tai absoluuttisen polun.
Absoluuttiset polut alkavat tiedostojärjestelmän juuresta ja kulkevat aina tiedostonimeen tai tiettyyn kansioon,
johon viittaat. Tätä polkutyyppiä kutsutaan absoluuttiseksi, koska se osoittaa ainutlaatuisen ja absoluuttisen sijainnin tietokoneellasi.
Eli tietokoneellasi ei ole toista sijaintia, joka vastaisi tätä polkua. Se on ainutlaatuinen tunniste.

Windowsissa absoluuttiinen polku alkaa kiintolevyn tunnisteella (esim. `C:/Users/pedro`).
Linuxissa ja macOS:ssa absoluuttiset polut alkavat kauttaviivamerkillä (esim. `/usr/local/bin`).
Huomaa, että polku koostuu "segmenteistä". Jokainen segmentti yhdistetään toisiinsa kauttaviiva-merkillä (`\` tai `/`).
Windowsissa taaksepäin kauttaviivaa (`\`) käytetään yleensä polkusegmenttien yhdistämiseen. Linuxissa ja macOS:ssa eteenpäin
kauttaviivaa (`/`) käytetään polkusegmenttien yhdistämiseen.

Suhteellinen polku alkaa CWD:stä. Toisin sanoen suhteellinen polku on
"suhteessa CWD:hen". Polku, jolla @fig-cwd:n `hello.zig`-tiedostoon pääsee, on esimerkki suhteellisesta polusta. Tämä polku
on alla. Polku alkaa CWD:stä, joka @fig-cwd:n kontekstissa on `zig-book`-kansio,
sitten se menee `ZigExamples`-kansioon, sitten `zig-basics`-kansioon ja lopuksi `hello.zig`-tiedostoon.

""",
    8: """


### Polkujen jokerimerkit

Kun annat polkuja, erityisesti suhteellisia polkuja, voit käyttää *jokerimerkkiä*.
Poluissa käytetään yleisesti kahta *jokerimerkkiä*: "yksi piste" (.) ja "kaksi pistettä" (..).
Toisin sanoen näillä kahdella merkillä on erityisiä merkityksiä poluissa,
ja niitä voi käyttää missä tahansa käyttöjärjestelmässä (Mac, Windows, Linux jne.). Ne ovat
"alustariippumattomia".

"Yksi piste" edustaa aliasta nykyiselle hakemistolle.
Tämä tarkoittaa, että suhteelliset polut `"./Course/Data/covid.csv"` ja `"Course/Data/covid.csv"` ovat vastaavia.
Toisaalta "kaksi pistettä" viittaa edelliseen hakemistoon.
Esimerkiksi polku `"Course/.."` on vastaava polulle `"."`, eli nykyiselle työhakemistolle.

Siksi polku `"Course/.."` viittaa kansioon ennen `Course`-kansiota.
Toisena esimerkkinä polku `"src/writexml/../xml.cpp"` viittaa tiedostoon `xml.cpp`,
joka on kansiossa ennen `writexml`-kansiota; tässä esimerkissä se on `src`-kansio.
Siksi tämä polku on vastaava polulle `"src/xml.cpp"`.




## CWD-käsittelijä

Zigissä tiedostojärjestelmäoperaatiot tehdään yleensä hakemistokäsittelijäolion kautta.
Hakemistokäsittelijä Zigissä on `std.Io.Dir`-tyyppinen olio, joka kuvaa
tiettyä kansiota tietokoneemme tiedostojärjestelmässä.
Luot yleensä `Dir`-olion kutsumalla `std.Io.Dir.cwd()`-funktiota.
Tämä funktio palauttaa `Dir`-olion, joka osoittaa (tai kuvaa)
nykyistä työhakemistoa (CWD).

Tämän `Dir`-olion kautta voit luoda uusia tiedostoja tai muokata tai lukea olemassa olevia tiedostoja,
jotka ovat CWD:si sisällä. Toisin sanoen `Dir`-olio on Zigissä pääsisäänkäynti useiden
tiedostojärjestelmäoperaatioiden suorittamiseen.
Alla olevassa esimerkissä luomme tämän `Dir`-olion ja tallennamme sen
`cwd`-oliossa. Vaikka emme käytä tätä oliota tässä koodiesimerkissä,
käytämme sitä paljon seuraavissa esimerkeissä.

""",
    9: """








## Tiedosto-operaatiot

### Tiedostojen luominen {#sec-creating-files}

Luomme uusia tiedostoja `Dir`-olion `createFile()`-metodilla.
Anna vain luotavan tiedoston nimi, ja funktio tekee
tarvittavat vaiheet tiedoston luomiseksi. Voit myös antaa suhteellisen polun tälle funktiolle,
ja se luo tiedoston seuraamalla tätä polkua, joka on suhteessa CWD:hen.

Tämä funktio voi palauttaa virheen, joten sinun pitäisi käyttää `try`-, `catch`- tai jotain @sec-error-handling-osiossa esiteltyjä
muita menetelmiä virheen käsittelyyn. Jos kaikki menee hyvin,
`createFile()`-metodi palauttaa file descriptor -olion (eli `File`-olion) tuloksena,
jonka kautta voit lisätä sisältöä tiedostoon aiemmin esittelemilläni IO-operaatioilla.

Katso alla olevaa koodiesimerkkiä. Tässä esimerkissä luomme uuden tekstitiedoston
nimeltä `foo.txt`. Jos `createFile()`-funktio onnistuu, `file`-niminen olio sisältää file descriptor -olion,
jota voimme käyttää kirjoittamaan (tai lisäämään) uutta sisältöä tiedostoon, kuten teemme tässä esimerkissä käyttämällä
puskuroitua writer-oliota kirjoittaaksemme uuden tekstirivin tiedostoon.

Nopea huomautus: kun luomme file descriptor -olion C:ssä C-funktiolla kuten `fopen()`, meidän täytyy aina sulkea tiedosto
ohjelmamme lopussa tai heti, kun olemme suorittaneet kaikki haluamamme operaatiot
tiedostolla. Zigissä tilanne on sama. Joka kerta kun luomme uuden tiedoston, tiedosto pysyy
"avoinna" odottaen jonkin operaation suorittamista. Heti kun olemme valmiita, meidän täytyy aina
sulkea tiedosto vapauttaaksemme siihen liittyvät resurssit.
Zigissä teemme tämän kutsumalla `close()`-metodia file descriptor -oliosta.


""",
    10: """


Tässä esimerkissä emme vain luoneet tiedostoa tiedostojärjestelmään,
vaan kirjoitimme myös dataa tähän tiedostoon käyttämällä `createFile()`-funktion palauttamaa file descriptor -oliota.
Jos tiedosto, jota yrität luoda,
on jo olemassa tiedostojärjestelmässäsi, tämä `createFile()`-kutsu
ylikirjoittaa tiedoston sisällön eli poistaa
kaiken olemassa olevan tiedoston sisällön.

Jos et halua tämän tapahtuvan, eli et halua ylikirjoittaa
olemassa olevan tiedoston sisältöä, mutta haluat silti kirjoittaa dataa tiedostoon
(eli haluat liittää dataa tiedostoon), sinun pitäisi käyttää `Dir`-olion `openFile()`-
metodia.

Toinen tärkeä piirre `createFile()`-metodissa on, että se luo tiedoston,
joka ei ole oletuksena avoinna lukuoperaatioille. Et voi lukea tätä tiedostoa.
Se ei ole sallittua.
Esimerkiksi saatat haluta kirjoittaa jotain tiedostoon ohjelmasi suorituksen alussa.
Myöhemmin ohjelmassasi saatat tarvita lukea, mitä kirjoitit tiedostoon. Jos yrität lukea dataa tästä tiedostosta, saat todennäköisesti
`NotOpenForReading`-virheen tuloksena.


Miten voit ylittää tämän esteen? Miten voit luoda tiedoston, joka on avoinna
lukuoperaatioille? Sinun tarvitsee vain asettaa `read`-lippu arvoon true
`createFile()`-metodin kolmannessa argumentissa. Kun asetat tämän lipun arvoon true,
tiedosto luodaan "lukuoikeuksilla", ja seurauksena
alla olevan kaltainen ohjelma on kelvollinen:


""",
    11: """


### Tiedostojen avaaminen ja datan liittäminen

Tiedostojen avaaminen on helppoa. Käytä vain `openFile()`-metodia `createFile()`-metodin sijaan.
`openFile()`-metodin ensimmäisessä argumentissa annat IO-toteutuksen, toisessa argumentissa
polun tiedostoon, jonka haluat avata, ja kolmannessa argumentissa liput (tai asetukset),
jotka määräävät, miten tiedosto avataan.

Näet `openFile()`-metodin täydellisen asetusluettelon lukemalla dokumentaation tyypille
[`OpenFlags`](https://ziglang.org/documentation/master/std/#std.Io.File.OpenFlags)[^oflags].
Mutta pääasiallinen lippu, jota käytät varmasti, on `mode`-lippu.
Tämä lippu määrittää IO-tilan, jota tiedosto käyttää avautuessaan.
On kolme IO-tilaa eli kolme arvoa, joita voit antaa tälle lipulle:

- `read_only`, sallii vain lukuoperaatiot tiedostossa. Kaikki kirjoitusoperaatiot estetään.
- `write_only`, sallii vain kirjoitusoperaatiot tiedostossa. Kaikki lukuoperaatiot estetään.
- `read_write`, sallii sekä kirjoitus- että lukuoperaatiot tiedostossa.

[^oflags]: <https://ziglang.org/documentation/master/std/#std.Io.File.OpenFlags>

Nämä tilat ovat samanlaisia kuin tilat, jotka annat `mode`-argumentille
Pythonin `open()`-sisäänrakennetussa funktiossa[^py-open] tai C:n
`fopen()`-funktiossa[^c-open]. Jos avaat tiedoston tilalla, joka ei salli haluamaasi operaatiota
tiedostossa, saat yleensä käyttöjärjestelmältä `AccessDenied`-virheen tuloksena.

Windows-käyttäjille on syytä huomata, että useimmiten, kun yrität kirjoittaa/liittää dataa tiedostoon,
käytät todennäköisesti `read_write`-tilaa `write_only`-tilan sijaan. Tämä johtuu siitä, että Windows-käyttöjärjestelmä
tarvitsee myös lukuoikeuden tiedostoon voidakseen kirjoittaa siihen dataa. Ole varovainen tämän kanssa. Linux-tyyppisissä järjestelmissä tämä ei yleensä tapahdu,
ja `write_only`-tila riittää yleensä, jos haluat vain kirjoittaa dataa tiedostoon eikä mitään muuta.

Alla olevassa koodiesimerkissä avaamme `foo.txt`-tekstitiedoston `read_write`-tilassa[^windows-write]
ja liitämme uuden tekstirivin tiedoston loppuun. Tätä varten käytämme file descriptor -olion `writePositionalAll()`-
metodia. Tämä metodi antaa sinun kirjoittaa tavu-/datalohkon
tiettyyn kohtaan tiedostossa.

[^windows-write]: Tämä tekee koodiesimerkistä yhteensopivan sekä Linuxin että Windowsin kanssa edellisessä kappaleessa selittämistäni syistä. Jos olet vain Linux-käyttäjä, voisit käyttää `write_only`-tilaa `read_write`-tilan sijaan, ja koodi toimisi silti.

Koska haluamme liittää dataa tiedoston loppuun, käytän file descriptor -olion `length()`-metodia
laskemaan tiedoston pituuden (eli kuinka monta tavua tiedosto sisältää) ja annan tuloksen
`writePositionalAll()`-metodin kolmantena argumenttina, mikä kertoo metodille kirjoittaa syötedata
tiedoston loppuun.

[^py-open]: <https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files>
[^c-open]: <https://www.tutorialspoint.com/c_standard_library/c_function_fopen.htm>



""",
    12: """


### Tiedostojen poistaminen

Joskus meidän täytyy vain poistaa tiedostoja.
Tätä varten käytämme `deleteFile()`-metodia. Anna IO-toteutus
ensimmäisessä argumentissa ja poistettavan tiedoston polku
toisessa argumentissa, ja metodi yrittää poistaa kyseisessä polussa olevan tiedoston.

""",
    13: """

### Tiedostojen kopiointi

Olemassa olevien tiedostojen kopioimiseen käytämme `copyFile()`-metodia. Metodin ensimmäinen argumentti
on polku tiedostoon, jonka haluat kopioida. Toinen argumentti on `Dir`-olio, eli hakemistokäsittelijä,
tarkemmin sanottuna `Dir`-olio, joka osoittaa kansioon, johon haluat
kopioida tiedoston. Kolmas argumentti on tiedoston uusi polku eli uusi sijainti.
Neljäs argumentti on käytettävä IO-toteutus. Viides argumentti ovat
kopiointioperaatiossa käytettävät asetukset (tai liput).

Metodille antamaasi `Dir`-oliota käytetään tiedoston kopioimiseen
uuteen sijaintiin. Voit luoda tämän `Dir`-olion ennen `copyFile()`-metodin kutsumista.
Ehkä aiot kopioida tiedoston täysin eri sijaintiin tietokoneellasi,
joten voi olla hyödyllistä luoda hakemistokäsittelijä kyseiseen sijaintiin. Mutta jos kopioit
tiedoston CWD:n alikansioon, voit yksinkertaisesti antaa CWD-käsittelijän tälle argumentille.

""",
    14: """


### Lue dokumentaatio!

`Dir`-olioissa on muitakin hyödyllisiä tiedosto-operaatiometodeja,
kuten `writeFile()`-metodi, mutta suosittelen lukemaan dokumentaation tyypille
[`Dir`](https://ziglang.org/documentation/master/std/#std.fs.Dir)[^zig-dir]
tutustuaksesi muihin saatavilla oleviin metodeihin, koska olen jo puhunut niistä liikaa.


[^zig-dir]: <https://ziglang.org/documentation/master/std/#std.fs.Dir>





## Hakemisto-operaatiot

### Tiedostojen läpikäynti hakemistossa

Yksi klassisimmista tiedostojärjestelmään liittyvistä tehtävistä on pystyä
käymään läpi hakemistossa olevat tiedostot. Hakemiston tiedostojen läpikäyntiin tarvitsemme iteraattoriolion.

Tällaisen iteraattoriolion voi tuottaa joko `iterate()`- tai `walk()`-metodilla
`Dir`-oliosta. Molemmat metodit palauttavat iteraattoriolion tuloksena, jota voit edetä `next()`-metodilla.
Näiden metodien ero on, että `iterate()` palauttaa ei-rekursiivisen iteraattorin,
kun taas `walk()` tekee. Tämä tarkoittaa, että `walk()`-metodin palauttama iteraattori käy läpi
paitsi nykyisen hakemiston tiedostot myös kaikkien alihakemistojen tiedostot,
jotka löytyvät nykyisestä hakemistosta.

Alla olevassa esimerkissä näytämme hakemistossa `ZigExamples/file-io` tallennettujen tiedostojen nimet.
Huomaa, että meidän täytyi avata tämä hakemisto `openDir()`-funktiolla. Huomaa myös, että annoimme lipun `iterate`
`openDir()`-funktion toisessa argumentissa. Tämä lippu on tärkeä, koska ilman sitä
emme saisi käydä läpi tämän hakemiston tiedostoja.

""",
    15: """


### Uusien hakemistojen luominen

Hakemistojen luomisessa on kaksi tärkeää metodia: `createDir()` ja `createDirPath()`.
Näiden kahden metodin ero on, että `createDir()` voi
luoda vain yhden hakemiston nykyiseen hakemistoon kutsua kohden,
kun taas `createDirPath()` pystyy luomaan alihakemistoja rekursiivisesti samassa kutsussa.


Siksi tämän metodin nimi on "make path". Se luo niin monta
alihakemistoa kuin on tarpeen luodakseen antamasi polun.
Jos annat polun `"sub1/sub2/sub3"` syötteenä tälle metodille,
se luo kolme eri alihakemistoa: `sub1`, `sub2` ja `sub3`,
saman funktiokutsun aikana. Sitä vastoin, jos antaisit tällaisen polun
syötteenä `createDir()`-metodille, saisit todennäköisesti virheen tuloksena, koska
tämä metodi voi luoda vain yhden alihakemiston.

""",
    16: """

### Hakemistojen poistaminen

Poistaaksesi hakemiston, anna poistettavan hakemiston polku
syötteenä `Dir`-olion `deleteDir()`-metodille. Alla olevassa esimerkissä
poistamme `src`-hakemiston, jonka juuri loimme edellisessä esimerkissä.

""",
    17: """


## Yhteenveto

Tässä luvussa olen kuvannut, miten Zigissä suoritetaan yleisimmät tiedostojärjestelmä- ja IO-operaatiot.
Saatat kuitenkin kaivata tästä luvusta joitakin harvinaisempia operaatioita, kuten: miten tiedostoja nimetään uudelleen,
miten hakemisto avataan, miten symbolisia linkkejä luodaan tai miten `access()`-funktiota käytetään testaamaan, onko tietty
polku olemassa tietokoneellasi. Kaikkiin näihin harvinaisempiin tehtäviin suosittelen lukemaan
[`Dir`-tyypin](https://ziglang.org/documentation/master/std/#std.fs.Dir)[^zig-dir]
dokumentaation, josta löydät hyvän kuvauksen näistä tapauksista.
""",
}