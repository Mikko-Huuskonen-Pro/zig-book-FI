# Chapter 12 Finnish translations - loaded by fi_10_12_translations.py

t(
"""# Filesystem and Input/Output (IO) {#sec-filesystem}

In this chapter we are going to discuss how you can can execute filesystem operations
and also handle input/output (IO) using the cross-platform structs and functions
from the Zig Standard Library. Most of these functions and structs
comes from the `std.Io` module.

## Input/Output basics {#sec-io-basics}

If you have some experience in any high-level programming language, you have certainly used
some input or output functionality before. In other words, you certainly have
been in a situation where you needed to send some output to the user, or, to receive an input
from the user of your program.

For example, in Python we can receive some input from the user by using the `input()` built-in
function. But we can also print (or "show") some output to the user by using the `print()`
built-in function. So yes, if you have programmed before in Python, you certainly have
used these functions once before.

But do you know how these functions relate back to your operating system (OS)? How exactly
they are interacting with the resources of your OS to receive or sent some input/output.
In essence, these input/output functions from high-level languages are just abstractions
over the *standard output* and *standard input* channels of your operating system.

This means that we receive an input, or send some output, through the operating system.
It's the OS that makes the bridge between the user and your program. Your program
does not have a direct access to the user. It's the OS that intermediates every
message exchanged between your program and the user.

The *standard output* and *standard input* channels of your OS are commonly known as the
`stdout` and `stdin` channels of your OS, respectively. In some contexts, they are also
called the *standard output device* and the *standard input device*. As the name suggests,
the *standard output* is the channel through which output flows, while the *standard input*
is the channel in which input flows.

Furthermore, OS's also normally create a dedicated channel for exchanging error messages, which is known as the
*standard error* channel, or, the `stderr` channel. This is the channel to which error and warning messages
are usually sent to. These are the messages that are normally displayed in red-like or orange-like colors
into your terminal.

Normally, every OS (e.g. Windows, macOS, Linux, etc.) creates a dedicated and separate set of
*standard output*, *standard error* and *standard input* channels for every single program (or process) that runs in your computer.
This means that every program you write have a dedicated `stdin`, `stderr` and `stdout` that are separate
from the `stdin`, `stderr` and `stdout` of other programs and processes that are currently running.

This is a behaviour from your OS. This does not come from the programming language that you are using.
Because as I said earlier, input and output in programming languages, especially
in high-level ones, are just a simple abstraction over the `stdin`, `stderr` and `stdout` from your current OS.
That is, your OS is the intermediary between every input/output operation made in your program,
regardless of the programming language that you are using.




## The writer and reader pattern {#sec-writer-reader}

In Zig, there is a pattern around input/output (IO). I (the author of this book) don't know if there
is an official name for this pattern. But here, in this book, I will call it the "writer and reader pattern".
In essence, every IO operation in Zig is made through either a `Reader` or a `Writer` object[^gen-zig].

These two data types are actually interfaces, and they come from the `std.Io` module of the Zig Standard Library. As their names suggests, a
`Reader` is an object that offers tools to read data from "something" (or "somewhere"), while a `Writer`
offers tools to write data into this "something". This "something" might be different things: like a
file that exists in your filesystem; or, it might be a network socket in your system[^sock]; or,
a continuous stream of data, like a standard input device from your system, that might be constantly
receiving new data from users, or, as another example, a live chat in a game that is constantly
receiving and displaying new messages from the players of the game.

[^gen-zig]: Previously, these objects were known as the `GenericReader` and `GenericWriter` objects. But both of these types were deprecated in 0.15.
[^sock]: The socket objects that we have created in @sec-create-socket, are examples of network sockets.

So, if you want to **read** data from something, or somewhere, it means that you need to use a `Reader` object.
But if you need instead, to **write** data into this "something", then, you need to use a `Writer` object instead.
Both of these objects are normally created from a file descriptor object. More specifically, through the `writer()` and `reader()`
methods of this file descriptor object. If you are not familiar with file descriptors, go to the next section.

Every `Writer` object has methods like `print()`, which allows you to write/send a formatted string
(i.e., this formatted string is like a `f` string in Python, or, similar to the `printf()` C function)
into the "something" (file, socket, stream, etc.) that you are using. It also has a `writeAll()` method, which allows you to
write a string, or, an array of bytes into the "something".

Likewise, every `Reader` object have methods like `readSliceAll()`, which allows you to read
data from the "something" (file, socket, stream, etc.) until it fills a particular array (i.e., a "buffer") object.
In other words, if you provide an array object of 300 `u8` values to `readSliceAll()`, then, this method attempts to read 300 bytes
of data from the "something", and it stores them into the array object that you have provided.

Another useful method is `takeDelimiterExclusive()`. In this method, you specify a "delimiter character".
The idea is that this function will attempt to read as many bytes of data as possible from the "something"
until it finds the "delimiter character" that you have specified, and, it returns a slice with the data to you.


This is just a quick description of the methods present in these types of objects. But I recommend you
to read the official docs, both for
[`Writer`](https://ziglang.org/documentation/master/std/#std.Io.Writer)[^gen-write] and
[`Reader`](https://ziglang.org/documentation/master/std/#std.Io.Reader)[^gen-read].
I also think it's a good idea to read the source code of the modules in the Zig Standard Library
that defines the methods present in these objects, which are the
[`Reader.zig`](https://codeberg.org/ziglang/zig/src/branch/master/lib/std/Io/Reader.zig)[^mod-read]
and [`Writer.zig`](https://codeberg.org/ziglang/zig/src/branch/master/lib/std/Io/Writer.zig)[^mod-write].

[^gen-read]: <https://ziglang.org/documentation/master/std/#std.Io.Reader>.
[^gen-write]: <https://ziglang.org/documentation/master/std/#std.Io.Writer>.
[^mod-read]: <https://codeberg.org/ziglang/zig/src/branch/master/lib/std/Io/Reader.zig>.
[^mod-write]: <https://codeberg.org/ziglang/zig/src/branch/master/lib/std/Io/Writer.zig>.



## The new `io` argument {#sec-new-io-backend}

Since Zig 0.15, the Zig development team initiated a movement to change completely how IO operations are made in Zig.
With this big movement, a completely new IO interface was introduced into the language, which was the introduction of the `Reader` and `Writer`
interfaces that we described on @sec-writer-reader. Not only that has happened, but also, since Zig 0.16 a new big step into this new IO interface
was made, with the introduction of the new `io` argument, from which you can choose the "IO backend implementation" that
you want to use, with `std.Io.Evented`, `std.Io.Threaded`, and others.

Let's make a quick comparison here. You've probably noticed from @sec-memory-chap that, allocators are an essential type of object in Zig.
They appear everywhere, and they are essential to any kind of task that needs to allocate some memory to
complete. Well, with the introduction of this new IO interface, choosing an "IO backend implementation" also became an essential
task in Zig code, like choosing an allocator.

So now, you usually start your Zig code by choosing both an allocator, and also, an "IO backend implementation" to use.
In the example below, I'm choosing an IO implementation that is based on thread pools. But I could also (if I wanted to) use
`std.Io.Evented`, which is based on queue rings.

The key objects in this code snippet exposed below are `allocator` and `io`.""",
"""# Tiedostojärjestelmä ja syöte/tuloste (IO) {#sec-filesystem}

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

Alla olevan koodinpätkän keskeiset oliot ovat `allocator` ja `io`.""")

t(
"""\n\n\nTherefore, since Zig 0.16, you will find different functions that perform some IO operation across the Zig Standard Library\nthat takes an argument named `io` of type `std.Io`. A big example of that is the `reader()` method that you find in `std.Io.File`. This method is responsible\nfor creating the `Reader` object through which you can read data from the file represented by the `std.Io.File` object.\nAnd this method now has an `io` argument, in which you should provide the "IO backend implementation" that you\nwant to use while reading the file.\n\nIn the example below, I'm demonstrating the use of this `io` argument by opening a file in my computer and reading it. Notice that I provide an\n"IO backend implementation" (i.e. the `io` object) to the `reader()` method. This is just one\nexample. You will find this pattern of "providing an IO backend implementation" in many other kinds of tasks.\nFunctions related to networking are another instance where you will commonly find this `io` argument.\n""",
"""\n\n\nZig 0.16:sta lähtien löydät Zig Standard Librarystä eri funktioita, jotka suorittavat IO-operaatioita ja
ottavat argumentin nimeltä `io`, jonka tyyppi on `std.Io`. Hyvä esimerkki on `std.Io.File`-tyypin `reader()`-metodi. Tämä metodi on vastuussa
`Reader`-olion luomisesta, jonka kautta voit lukea dataa `std.Io.File`-olion edustamasta tiedostosta.
Ja tällä metodilla on nyt `io`-argumentti, johon sinun pitäisi antaa "IO-backend-toteutus", jota
haluat käyttää tiedostoa lukiessasi.

Alla olevassa esimerkissä demonstroin tämän `io`-argumentin käyttöä avaamalla tiedoston tietokoneellani ja lukemalla sen. Huomaa, että annan
"IO-backend-toteutuksen" (eli `io`-olion) `reader()`-metodille. Tämä on vain yksi
esimerkki. Löydät tämän "IO-backend-toteutuksen antamisen" mallin monista muistakin tehtävistä.
Verkkoihin liittyvät funktiot ovat toinen tapaus, jossa näet usein tämän `io`-argumentin.
""")

t(
"""\n\n\n## Using a default IO implementation\n\nSometimes, is just a hassle to write all the necessary code to properly instantiate a IO\nimplementation. And sometimes, you just don't really care much about how the IO operations are being done under the hood,\nand you just wish to use an IO backend with default settings. If that is your case,\nthere are currently three easy ways to quickly get an IO backend with default settings, which are:\n\n- use the the default IO implementation for the target configuration.\n- use a single threaded IO implementation with default configuration.\n- use the IO implementation from the `std.testing` module.\n\n\n### Using the IO implementation from `std.testing`\n\nAs the name suggests, the IO implementation from the `std.testing` module should be\nused only inside "unit tests context". If you try to use them inside any other type of context,\nyou normally end up with a compilation error.\n""",
"""\n\n\n## Oletusarvoisen IO-toteutuksen käyttö\n\nJoskus on vaivalloista kirjoittaa kaikki tarvittava koodi IO-toteutuksen
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
""")

t(
"""\n\n\n### Using the single threaded IO implementation\n\nThere is an easy an quick way to get a single threaded IO implementation.\nAll you have to do is to instantiate a `std.Io.Threaded` object with the value\n`.init_single_threaded`, and then, call the `io()` method from the resulting\nobject, as the code example below demonstrates:\n""",
"""\n\n\n### Yksisäikeisen IO-toteutuksen käyttö\n\nYksisäikeisen IO-toteutuksen saaminen on helppoa ja nopeaa.
Sinun tarvitsee vain luoda `std.Io.Threaded`-olio arvolla
`.init_single_threaded` ja kutsua sitten syntyneen
olion `io()`-metodia, kuten alla oleva koodiesimerkki osoittaa:
""")

t(
"""\n\n### Using the default IO implementation for your target\n\nIn more recent versions of Zig, a new "default argument" for the main function was introduced,\nwhich is the `init` argument. In summary, you can write a main function that receives\nan object of type `std.process.Init` as input.\n\nThis `std.process.Init` object is essentially an object that comes with a set of pre-initialized\nAPIs for your program to take advantage of. You can use this argument to easily get a pre-defined\nand pre-initialized IO implementation for your IO operations. This implementation is accessible at the\n`io` attribute of this `init` argument.\n""",
"""\n\n### Kohteesi oletusarvoisen IO-toteutuksen käyttö\n\nUudemmissa Zig-versioissa main-funktiolle otettiin käyttöön uusi "oletusargumentti",
joka on `init`-argumentti. Yhteenvetona voit kirjoittaa main-funktion, joka vastaanottaa
`std.process.Init`-tyyppisen olion syötteenä.

`std.process.Init`-olio on pohjimmiltaan olio, joka sisältää joukon valmiiksi alustettuja
API-rajapintoja, joita ohjelmasi voi hyödyntää. Voit käyttää tätä argumenttia saadaksesi helposti ennalta määritellyn
ja valmiiksi alustetun IO-toteutuksen IO-operaatioillesi. Tämä toteutus on käytettävissä
tämän `init`-argumentin `io`-attribuutissa.
""")

