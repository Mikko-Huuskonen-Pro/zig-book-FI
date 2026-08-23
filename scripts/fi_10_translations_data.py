TRANSLATIONS = {
    0: """# Projekti 3 – pinorakenteen rakentaminen

Tässä luvussa toteutamme pinorakenteen (stack) seuraavana pienenä projektina
tässä kirjassa. Perustietorakenteiden toteuttaminen millä tahansa kielellä on eräänlainen
"eskaritehtävä" (jos tämä termi edes on olemassa) tietojenkäsittelytieteessä (TKT), koska
niitä opetellaan ja toteutetaan yleensä TKT-opintojen ensimmäisillä lukukausilla.

Mutta tämä on itse asiassa hyvä asia! Koska tehtävän pitäisi olla hyvin helppo, meidän ei tarvitse selittää paljoa
sitä, mikä pino on, vaan voimme keskittyä siihen, mikä tässä on oikeasti tärkeää: oppia,
miten "geneerisyyden" (generics) käsite toteutetaan Zig-kielessä ja miten yksi Zigin keskeisistä
ominaisuuksista, `comptime`, toimii, ja käyttää pinorakennetta näiden käsitteiden havainnollistamiseen käytännössä.

Ennen kuin ryhdymme rakentamaan pinorakennetta, meidän täytyy ensin ymmärtää,
mitä `comptime`-avainsana tekee koodillesi, ja sen jälkeen opetella,
miten geneerisyys toimii Zigissä.


## `comptime`-avainsanan ymmärtäminen Zigissä {#sec-comptime}

Yksi Zigin keskeisistä ominaisuuksista on `comptime`. Tämä avainsana tuo mukanaan kokonaan
uuden käsitteen ja paradigman, joka on tiiviisti yhteydessä käännösprosessiin.
@sec-compile-time-osiossa kuvasimme "käännösaika vs. ajonaika" -erottelun merkityksen ja roolin
Zigissä. Siinä osiossa opimme, että arvoon tai olioon sovellettavat säännöt muuttuvat
paljon sen mukaan, onko arvo tiedossa käännösaikana vai vasta ajonaikana.

`comptime`-avainsana liittyy vahvasti näihin kahteen aikajaksoon (käännösaika ja ajonaika).
Kerrataan nopeasti erot. Käännösaika on ajanjakso, jolloin Zig-lähdekoodiasi käännetään `zig`-kääntäjällä,
kun taas ajonaika on ajanjakso, jolloin Zig-ohjelmaasi suoritetaan, eli kun suoritamme
`zig`-kääntäjän tuottamia binääritiedostoja.

`comptime`-avainsanaa voi käyttää kolmella tavalla:

- soveltaa `comptime` funktion argumenttiin.
- soveltaa `comptime` olioon.
- soveltaa `comptime` lausekejoukkoon.



### Soveltaminen funktion argumenttiin

Kun sovellat `comptime`-avainsanaa funktion argumenttiin, kerrot `zig`-kääntäjälle,
että kyseisen funktion argumenttiin annetun arvon täytyy olla tiedossa käännösaikana.
Selitimme @sec-compile-time-osiossa yksityiskohtaisesti, mitä "käännösaikana tiedossa oleva arvo" tarkoittaa. Jos
sinulla on epäilyksiä tästä ajatuksesta, palaa takaisin kyseiseen osioon.

Mietitään nyt tämän ajatuksen seurauksia. Ensinnäkin asetamme rajoituksen tai vaatimuksen
kyseiselle funktion argumentille. Jos ohjelmoija vahingossa yrittää antaa tälle
funktion argumentille arvon, joka ei ole tiedossa käännösaikana, `zig`-kääntäjä huomaa ongelman ja
nostaa käännösvirheen, jossa kerrotaan, ettei ohjelmaa voi kääntää. Sillä
annat "ajonaikana tiedossa olevan" arvon funktion argumentille, jonka täytyy olla "käännösaikana tiedossa".

Katso alla olevaa hyvin yksinkertaista esimerkkiä, jossa määrittelemme `twice()`-funktion, joka yksinkertaisesti
kaksinkertaistaa syötteen arvon nimeltä `num`. Huomaa, että käytämme `comptime`-avainsanaa ennen
funktion argumentin nimeä. Tämä avainsana merkitsee funktion argumentin `num` "comptime-argumentiksi".

Kyseessä on funktion argumentti, jonka arvon täytyy olla käännösaikana tiedossa. Siksi lauseke
`twice(5678)` on kelvollinen eikä käännösvirheitä synny. Arvo `5678`
on käännösaikana tiedossa, joten tämä on odotettu käyttäytyminen tälle funktiolle.""",
    1: """Entä jos annamme tälle funktiolle luvun, joka ei ole käännösaikana tiedossa?
Esimerkiksi ohjelmasi voi vastaanottaa käyttäjältä syötettä järjestelmän `stdin`-
kanavan kautta. Tämä käyttäjän syöte voi olla monia eri asioita,
eikä sitä voida ennakoida käännösaikana. Nämä olosuhteet tekevät tästä "käyttäjän syötteestä"
vain ajonaikana tiedossa olevan arvon.

Alla olevassa esimerkissä tämä "käyttäjän syöte" vastaanotetaan aluksi merkkijonona,
joka jäsennetään ja muunnetaan kokonaisluvuksi, ja tämän operaation tulos
tallennetaan `n`-olioon.

Koska "käyttäjän syöte" on tiedossa vasta ajonaikana, olion `n` arvo määräytyy vasta ajonaikana.
Seurauksena emme voi antaa tätä oliota syötteeksi `twice()`-funktiolle.
`zig`-kääntäjä ei salli sitä, koska merkitsimme
argumentin `num` "comptime-argumentiksi". Siksi `zig`-kääntäjä nostaa
alla näkyvän käännösaikaisen virheen:""",
    2: """Comptime-argumentteja käytetään usein funktioissa, jotka palauttavat jonkinlaisen
geneerisen rakenteen. Itse asiassa `comptime` on olennainen osa (tai perusta) geneerisyyden toteuttamiseen Zigissä.
Puhumme geneerisyydestä lisää @sec-generics-osiossa.

Toistaiseksi katsotaan tätä koodiesimerkkiä lähteestä @karlseguin_generics. Näet,
että tällä `IntArray()`-funktiolla on yksi argumentti nimeltä `length`.
Tämä argumentti on merkitty comptime-argumentiksi ja vastaanottaa syötteenä `usize`-tyyppisen arvon. Argumentille annetun arvon
täytyy siis olla käännösaikana tiedossa.
Näemme myös, että funktio palauttaa tuloksena `i64`-arvojen taulukon.""",
    3: """Nyt tämän funktion keskeinen osa on `length`-argumentti. Tätä argumenttia
käytetään määrittämään funktion tuottaman taulukon koko. Mietitään
tämän seurauksia. Jos taulukon koko riippuu
`length`-argumentille annetusta arvosta, funktion tulosteen datatyyppi riippuu
tämän `length`-argumentin arvosta.

Anna tämän ajatuksen upota mieleesi hetkeksi. Kuten kuvasin @sec-root-file-osiossa,
Zig on vahvasti tyypitetty kieli, erityisesti funktioiden määrittelyissä.
Joka kerta kun kirjoitamme funktion Zigissä, meidän täytyy merkitä funktion palauttaman arvon datatyyppi.
Mutta miten voimme tehdä sen, jos datatyyppi
riippuu funktion argumentille annetusta arvosta?

Mieti tätä hetki. Jos `length` on esimerkiksi 3, funktion
palautustyyppi on `[3]i64`. Mutta jos `length` on 40,
palautustyypistä tulee `[40]i64`. Tässä vaiheessa `zig`-kääntäjä olisi hämmentynyt
ja nostaisi käännösvirheen, jossa sanottaisiin jotain tällaista:

> Hei! Olet merkinnyt, että tämän funktion pitäisi palauttaa `[3]i64`-arvo, mutta sain `[40]i64`-arvon! Tämä ei vaikuta oikealta!

Miten ratkaiset tämän ongelman? Miten ylitämme tämän esteen? Tähän asti tulee
`type`-avainsana. Tämä `type`-avainsana sanoo käytännössä
`zig`-kääntäjälle, että funktio palauttaa jonkin datatyypin tuloksena, mutta se ei vielä tiedä,
mikä datatyyppi se on. Puhumme tästä lisää @sec-generics-osiossa.



### Soveltaminen lausekkeeseen

Kun sovellat `comptime`-avainsanaa lausekkeeseen, `zig`-kääntäjä suorittaa
kyseisen lausekkeen taatusti käännösaikana. Jos lauseketta ei jostain syystä voida suorittaa käännösaikana
(esimerkiksi jos lauseke riippuu arvosta, joka on tiedossa vasta ajonaikana), `zig`-kääntäjä
nostaa käännösvirheen.

Ota tämä esimerkki Zigin virallisesta dokumentaatiosta [@zigdocs]. Suoritamme
samaa `fibonacci()`-funktiota sekä ajonaikana että käännösaikana.
Funktio suoritetaan oletuksena ajonaikana, mutta koska käytämme `comptime`-
avainsanaa toisessa "try-lausekkeessa", tämä lauseke suoritetaan käännösaikana.

Tämä voi olla joillekin hämmentävää. Kyllä! Kun sanon, että lauseke
suoritetaan käännösaikana, tarkoitan, että lauseke käännetään ja suoritetaan
sillä aikaa, kun `zig`-kääntäjä kääntää Zig-lähdekoodiasi.""",
    4: """Suuri osa Zig-lähdekoodistasi voidaan mahdollisesti suorittaa käännösaikana,
koska `zig`-kääntäjä pystyy päättelemään joidenkin lausekkeiden tuloksen.
Erityisesti jos lausekkeet riippuvat vain käännösaikana tiedossa olevista arvoista.
Olemme puhuneet tästä @sec-compile-time-osiossa.

Mutta kun käytät `comptime`-avainsanaa lausekkeessa, ei ole enää kyse siitä, että lauseke "saattaa suorittua
käännösaikana". `comptime`-avainsanalla määräät `zig`-kääntäjän
suorittamaan lausekkeen käännösaikana. Asetat tämän säännön, ja on taattua,
että kääntäjä suorittaa sen aina käännösaikana. Tai ainakin kääntäjä
yrittää suorittaa sen. Jos kääntäjä ei jostain syystä pysty suorittamaan lauseketta,
se nostaa käännösvirheen.


### Soveltaminen lohkoon

Lohkot kuvattiin @sec-blocks-osiossa. Kun sovellat `comptime`-avainsanaa
lausekejoukkoon, saat käytännössä saman vaikutuksen kuin soveltaessasi avainsanaa
yksittäiseen lausekkeeseen. Eli koko lausekejoukko suoritetaan
käännösaikana `zig`-kääntäjän toimesta.

Alla olevassa esimerkissä merkitsemme `blk`-nimellä merkityn lohkon comptime-lohkoksi,
ja siksi lohkon sisällä olevat lausekkeet suoritetaan käännösaikana.""",
    5: """## Geneerisyyden esittely {#sec-generics}

Ensinnäkin, mikä on geneerinen tyyppi? Geneerisyys on ajatus, jossa tyypin
(`f64`, `u8`, `u32`, `bool` ja myös käyttäjän määrittelemät tyypit, kuten `User`-struct,
jonka määrittelimme @sec-structs-and-oop-osiossa) sallitaan olla parametri metodeille, luokille ja
rajapinnoille [@geeks_generics]. Toisin sanoen "geneerinen" on luokka (tai metodi), joka voi toimia
useiden datatyyppien kanssa.

Esimerkiksi Javassa geneeriset tyypit luodaan `<>`-operaattorilla. Tällä operaattorilla
Java-luokka voi vastaanottaa datatyypin syötteenä ja sovittaa
ominaisuutensa tämän syötedatyypin mukaan.
Toisena esimerkkinä C++:ssa geneerisyyttä tuetaan mallien (templates) käsitteen kautta.
C++:n luokkamallit ovat geneerisiä tyyppejä.

Zigissä geneerisyys toteutetaan `comptime`-avainsanan kautta. `comptime`-avainsana
antaa meidän kerätä datatyypin käännösaikana ja välittää sen
syötteenä koodinpätkälle.


### Geneerinen funktio {#sec-generic-fun}

Ota ensimmäisenä esimerkkinä alla oleva `max()`-funktio.
Tämä funktio on pohjimmiltaan "geneerinen funktio".
Funktiossa on comptime-funktion argumentti nimeltä `T`.
Huomaa, että tämän `T`-argumentin datatyyppi on `type`. Outoa, eikö? Tämä `type`-avainsana on
"kaikkien tyyppien isä" tai "tyyppien tyyppi" Zigissä.

Koska olemme käyttäneet `type`-avainsanaa `T`-argumentissa, kerromme
`zig`-kääntäjälle, että tämä `T`-argumentti vastaanottaa jonkin datatyypin syötteenä.
Huomaa myös `comptime`-avainsanan käyttö tässä argumentissa.
Kuten kuvasin @sec-comptime-osiossa, aina kun käytät tätä avainsanaa funktion argumentissa,
argumentin arvon täytyy olla tiedossa käännösaikana.
Tämä on järkevää, eikö? Koska ei ole olemassa datatyyppiä, joka ei olisi tiedossa käännösaikana.

Mieti tätä. Jokainen datatyyppi, jonka koskaan kirjoitat, on aina
tiedossa käännösaikana. Erityisesti koska datatyypit ovat olennaista
tietoa kääntäjälle, jotta se voi kääntää lähdekoodisi.
Tämän huomioiden on järkevää merkitä argumentti comptime-argumentiksi.""",
    6: """Huomaa myös, että `T`-argumentin arvoa käytetään
määrittämään funktion muiden argumenttien `a` ja `b` datatyypit sekä funktion
palautustyypin merkintä.
Eli näiden argumenttien (`a` ja `b`) datatyypit ja funktion itsensä palautustyyppi
määräytyvät `T`-argumentille annetun syötteen perusteella.

Tuloksena meillä on geneerinen funktio, joka toimii eri datatyyppien kanssa.
Esimerkiksi voin antaa `u8`-arvoja tälle `max()`-funktiolle, ja se toimii odotetusti.
Mutta jos annan `f64`-arvoja, se toimii myös odotetusti.
Ilman geneeristä funktiota minun pitäisi kirjoittaa erillinen `max()`-funktio
jokaiselle datatyypille, jota haluaisin käyttää.
Tämä geneerinen funktio tarjoaa meille hyvin hyödyllisen oikotien.""",
    7: """### Geneerinen tietorakenne {#sec-generic-struct}

Jokainen Zig Standard Libraryn tietorakenne (esim. `ArrayList`, `HashMap` jne.)
on pohjimmiltaan geneerinen tietorakenne.
Nämä tietorakenteet ovat geneerisiä siinä mielessä, että ne toimivat minkä tahansa haluamasi datatyypin kanssa.
Kerrot vain, mikä on niihin tallennettavien arvojen datatyyppi,
ja ne toimivat odotetusti.

Geneerinen tietorakenne Zigissä on tapa toteuttaa Javan geneerinen luokka
tai C++:n luokkamalli. Mutta saatat kysyä itseltäsi: miten rakennamme
geneerisen tietorakenteen Zigissä?

Perusajatus on kirjoittaa geneerinen funktio, joka luo tietorakenteen määrittelyn
haluamallemme tyypille. Toisin sanoen tämä geneerinen funktio toimii "tietorakenteiden tehtaalana".
Geneerinen funktio tuottaa `struct`-määrittelyn, joka kuvaa tätä tietorakennetta
tietylle datatyypille.

Tällaisen funktion luomiseksi lisäämme funktioon comptime-argumentin, joka vastaanottaa datatyypin
syötteenä. Opimme tämän edellisessä osiossa (@sec-generic-fun).
Mielestäni paras tapa havainnollistaa geneerisen tietorakenteen luomista on kirjoittaa sellainen.
Tässä siirrymme kirjan seuraavaan pieneen projektiin. Kyseessä on hyvin pieni projekti:
geneerisen pinorakenteen kirjoittaminen.




## Mikä on pino? {#sec-what-stack}

Pinorakenne (stack) on rakenne, joka noudattaa LIFO-periaatetta (*last in, first out*, viimeinen sisään, ensimmäinen ulos).
Pinorakenteessa tuetaan yleensä vain kahta operaatiota: `push` ja `pop`.
`push`-operaatiolla lisätään uusia arvoja pinoon, kun taas `pop`-operaatiolla poistetaan
arvoja pinosta.

Kun ihmiset yrittävät selittää, miten pinorakenne toimii, yleisin analogia
on lautasstacki. Kuvittele, että sinulla on pino lautasia,
esimerkiksi 10 lautasta pöydälläsi. Jokainen lautanen edustaa arvoa, joka
on tällä hetkellä tallennettuna tähän pinoon.

Aloitamme pinosta, jossa on 10 eri arvoa tai 10 eri lautasta. Kuvittele nyt, että haluat
lisätä uuden lautasen (tai uuden arvon) tähän pinoon, mikä vastaa `push`-operaatiota.
Lisäisit tämän lautasen (tai arvon) asettamalla uuden lautasen
pinon päälle. Sitten pinossa olisi 11 lautasta.

Mutta miten poistaisit lautasia (tai arvoja) tästä pinosta (eli `pop`-operaatio)?
Poistaisimme pinon päällimmäisen lautasen, ja tuloksena
meillä olisi jälleen 10 lautasta pinossa.

Tämä havainnollistaa LIFO-käsitettä, koska pinon ensimmäinen lautanen, eli pinon
alimmainen lautanen, on aina viimeinen, joka poistuu pinosta. Mieti tätä. Jotta
voisimme poistaa tämän tietyn lautasen pinosta, meidän täytyy poistaa kaikki pinon lautaset.
Joten jokainen pinon operaatio, sekä lisäys että poisto, tehdään aina pinon päällä.
@fig-stack havainnollistaa tätä logiikkaa visuaalisesti:

![Pinorakenteen kaavio. Lähde: Wikipedia, vapaa tietosanakirja.](./../Figures/lifo-stack.svg){#fig-stack}



## Pinorakenteen kirjoittaminen

Kirjoitamme pinorakenteen kahdessa vaiheessa. Ensin toteutamme
pinon, joka voi tallentaa vain `u32`-arvoja. Sen jälkeen laajennamme
toteutustamme geneeriseksi, jotta se toimii minkä tahansa haluamamme datatyypin kanssa.

Ensin meidän täytyy päättää, miten arvot tallennetaan pinon sisään. Pinorakenteen taustatallennuksen toteuttamiseen on useita
tapoja. Jotkut käyttävät kaksisuuntaista linkitettyä listaa,
toiset dynaamista taulukkoa jne. Tässä esimerkissä käytämme taulukkoa konepellon alla
pinon arvojen tallentamiseen; se on `items`-jäsen `Stack`-struct-määrittelyssämme.

Huomaa myös `Stack`-structissamme kolme muuta jäsentä: `capacity`, `length` ja `allocator`.
`capacity`-jäsen sisältää pinon arvot tallentavan taustataulukon kapasiteetin.
`length` sisältää pinossa tällä hetkellä tallennettujen arvojen määrän.
`allocator` sisältää allokaattorioleksen, jota pinorakenne käyttää aina, kun sen
täytyy varata lisää tilaa tallennettaville arvoille.

Aloitamme määrittelemällä structin `init()`-metodin, joka on vastuussa
`Stack`-olion luomisesta. Huomaa, että tämän
`init()`-metodin sisällä aloitamme varaamalla taulukon `capacity`-argumentissa
määritellyllä kapasiteetilla.""",
    8: """### `push`-operaation toteutus

Nyt kun olemme kirjoittaneet peruslogiikan uuden `Stack`-olion luomiseen,
voimme alkaa kirjoittaa push-operaation suorittavaa logiikkaa.
Muista, että push-operaatio pinorakenteessa on operaatio,
joka lisää uuden arvon pinoon.

Miten voimme lisätä uuden arvon `Stack`-olioomme?
Alla oleva `push()`-funktio on mahdollinen vastaus tähän kysymykseen.
Muista @sec-what-stack-osiossa käsitellystä, että arvot lisätään aina pinon päälle.
Tämä tarkoittaa, että `push()`-funktion täytyy aina löytää taustataulukosta elementti,
joka edustaa pinon ylintä kohtaa, ja lisätä syötearvo sinne.

Funktiossa on ensin if-lause. Tämä if-lause tarkistaa,
täytyykö meidän laajentaa taustataulukkoa tallentaaksemme
uuden arvon, jonka lisäämme pinoon. Toisin sanoen ehkä
taustataulukolla ei ole tarpeeksi kapasiteettia tallentaa tätä uutta
arvoa, ja tällöin meidän täytyy laajentaa taulukkoa saadaksemme tarvitsemamme kapasiteetin.

Jos if-lauseen looginen testi palauttaa true, taulukolla ei ole tarpeeksi kapasiteettia,
ja meidän täytyy laajentaa sitä ennen uuden arvon tallentamista.
If-lauseen sisällä suoritamme tarvittavat lausekkeet taustataulukon laajentamiseksi.
Huomaa, että käytämme allokaattorioletta varaamaan uuden taulukon, joka on kaksi kertaa suurempi
kuin nykyinen taulukko (`self.capacity * 2`).

Sen jälkeen käytämme sisäänrakennettua funktiota nimeltä `@memcpy()`. Tämä sisäänrakennettu funktio
vastaa C Standard Libraryn `memcpy()`-funktiota[^cmemcpy]. Sitä käytetään
kopioimaan arvot yhdestä muistilohkosta toiseen. Toisin sanoen
voit käyttää tätä funktiota kopioimaan arvot yhdestä taulukosta toiseen.

[^cmemcpy]: <https://www.tutorialspoint.com/c_standard_library/c_function_memcpy.htm>

Käytämme `@memcpy()`-sisäänrakennettua funktiota kopioimaan pinon olion taustataulukossa (`self.items`)
tällä hetkellä olevat arvot uuteen ja suurempaan varaamaamme taulukkoon (`new_buf`). Kun olemme suorittaneet tämän funktion, `new_buf` sisältää kopion
`self.items`-kohdassa olevista arvoista.

Kun olemme varmistaneet kopion nykyisistä arvoistamme `new_buf`-oliossa, voimme
vapauttaa `self.items`-kohdassa varatun muistin. Sen jälkeen meidän täytyy vain
määrätä uusi ja suurempi taulukko `self.items`-jäseneksi. Tämä on tarvittava
vaihejärjestys taulukon laajentamiseksi.""",
    9: """Kun olemme varmistaneet, että meillä on tarpeeksi tilaa tallentaa uusi arvo,
jonka lisäämme pinoon, meidän täytyy vain määrätä
tämä arvo pinon ylimmälle elementille ja kasvattaa
`length`-attribuutin arvoa yhdellä. Löydämme pinon ylimmän elementin
`length`-attribuutin avulla.



### `pop`-operaation toteutus

Nyt voimme toteuttaa pinooliomme pop-operaation.
Tämä on paljon helpompi operaatio toteuttaa, ja alla oleva `pop()`-metodi tiivistää
koko tarvittavan logiikan.

Meidän täytyy vain löytää taustataulukosta elementti, joka edustaa pinon ylintä kohtaa,
ja asettaa tämä elementti arvoon "undefined" osoittaaksemme, että
elementti on "tyhjä". Sen jälkeen meidän täytyy myös vähentää
pinon `length`-attribuuttia yhdellä.

Jos pinon nykyinen pituus on nolla, pinossa ei ole tällä hetkellä
tallennettuna arvoja. Tällöin voisimme vain palata funktiosta eikä tehdä mitään.
Tätä funktion sisällä oleva if-lause tarkistaa.""",
    10: """### `deinit`-metodin toteutus

Olemme toteuttaneet metodit, jotka vastaavat pinorakenteen kahta pääoperaatiota,
eli `pop()` ja `push()`, sekä metodin, joka luo
uuden `Stack`-olion, eli `init()`-metodin.

Nyt meidän täytyy toteuttaa myös metodi, joka tuhoaa
`Stack`-olion. Zigissä tämä tehtävä liitetään yleensä
`deinit()`-nimiseen metodiin. Useimmilla struct-olioilla Zigissä on tällainen metodi, ja sitä
kutsutaan usein "destructor-metodiksi".

Teoriassa ainoa, mitä meidän täytyy tehdä `Stack`-olion tuhoamiseksi, on varmistaa,
että vapautamme taustataulukolle varatun muistin käyttämällä
`Stack`-olion sisällä olevaa allokaattorioletta.
Alla oleva `deinit()`-metodi tekee juuri tämän.""",
    11: """## Geneeriseksi tekeminen

Nyt kun olemme toteuttaneet pinorakenteen perusrungon,
voimme keskittyä siihen, miten teemme siitä geneerisen. Miten saamme
tämän perusrungon toimimaan paitsi `u32`-arvojen myös minkä tahansa muun
haluamamme datatyypin kanssa?
Esimerkiksi saatamme tarvita pinoolion, joka tallentaa `User`-arvoja.
Miten tämä on mahdollista? Vastaus on geneerisyyden ja `comptime`-avainsanan käytössä.

Kuten kuvasin @sec-generic-struct-osiossa, perusajatus on kirjoittaa geneerinen
funktio, joka palauttaa struct-määrittelyn tuloksena.
Teoriassa emme tarvitse paljoa muuttaaksemme `Stack`-structimme geneeriseksi
tietorakenteeksi. Ainoa, mitä meidän täytyy tehdä, on muuttaa pinon taustataulukko
geneeriseksi taulukoksi.

Toisin sanoen tämän taustataulukon täytyy olla "kameleontti". Sen täytyy sopeutua
ja muuttua minkä tahansa haluamamme datatyypin taulukoksi. Jos meidän täytyy luoda
pino, joka tallentaa `u8`-arvoja, taustataulukon täytyy olla
`u8`-taulukko (eli `[]u8`). Mutta jos meidän täytyy tallentaa `User`-arvoja,
taulukon täytyy olla `User`-taulukko (eli `[]User`). Ja niin edelleen.

Teemme sen geneerisellä funktiolla. Koska geneerinen funktio voi vastaanottaa datatyypin
syötteenä, voimme välittää tämän datatyypin `Stack`-oliomme struct-määrittelyyn.
Siksi voimme käyttää geneeristä funktiota luomaan `Stack`-olion, joka voi tallentaa
haluamamme datatyypin. Jos haluamme luoda pinorakenteen, joka tallentaa `User`-arvoja,
annamme `User`-datatyypin tälle geneeriselle funktiolle, ja se luo meille
struct-määrittelyn, joka kuvaa `Stack`-oliota, joka voi tallentaa `User`-arvoja.

Katso alla olevaa koodiesimerkkiä. Olen jättänyt pois osia `Stack`-struct-määrittelystä
lyhyyden vuoksi. Jos jokin osa `Stack`-structistamme ei näy tässä
esimerkissä, se johtuu siitä, ettei kyseinen osa muuttunut edellisestä esimerkistä.
Se pysyy samana.""",
    12: """Huomaa, että olemme luoneet tässä esimerkissä funktion nimeltä `Stack()`. Tämä funktio
ottaa tyypin syötteenä ja välittää sen `Stack`-oliomme
struct-määrittelyyn. Jäsen `items` on nyt tyyppiä `T` oleva taulukko, eli
datatyyppi, jonka olemme antaneet funktiolle syötteenä. Funktion argumentti
`val` `push()`-funktiossa on nyt myös tyyppiä `T` oleva arvo.

Voimme antaa funktiolle datatyypin, ja se luo `Stack`-olion määrittelyn,
joka voi tallentaa antamamme datatyypin arvoja. Alla olevassa esimerkissä luomme
`Stack`-olion määrittelyn,
joka voi tallentaa `u8`-arvoja. Tämä määrittely tallennetaan `Stacku8`-oliossa.
`Stacku8`-oliosta tulee uusi struct, jota käytämme
`Stack`-oliomme luomiseen.""",
    13: """Jokainen Zig Standard Libraryn geneerinen tietorakenne (`ArrayList`, `HashMap`, `SinlyLinkedList` jne.)
on toteutettu tällä logiikalla. Ne käyttävät geneeristä funktiota luomaan struct-määrittelyn, joka toimii
syötteenä antamasi datatyypin kanssa.




## Yhteenveto

Tässä luvussa käsitellyn pinorakenteen täysi lähdekoodi on vapaasti saatavilla tämän kirjan virallisessa
repositoriossa. Katso [`stack.zig`](https://github.com/pedropark99/zig-book/tree/main/ZigExamples/data-structures/stack.zig)[^zig-stack]
pinomme `u32`-versiolle
ja [`generic_stack.zig`](https://github.com/pedropark99/zig-book/tree/main/ZigExamples/data-structures/generic_stack.zig)[^zig-stack2]
geneeriselle versiolle repositorion `ZigExamples`-kansiossa.


[^zig-stack]: <https://github.com/pedropark99/zig-book/tree/main/ZigExamples/data-structures/stack.zig>
[^zig-stack2]: <https://github.com/pedropark99/zig-book/tree/main/ZigExamples/data-structures/generic_stack.zig>""",
}