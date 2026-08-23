# Suomennoksen rakenne ja työnkulku

Tämä fork on [Introduction to Zig](https://github.com/pedropark99/zig-book) -kirjan suomenkielinen versio. Rakenne on suunniteltu niin, että upstream-muutokset voidaan hakea helposti, käännökset pitää ajan tasalla ja GitHub Pages julkaisee automaattisesti.

## Periaate: yksi lähde, kaksi kieliversiota

```
zig-book-FI/
├── Chapters/          # ENGLANTI — synkronoidaan upstreamista, älä muokkaa käsin
├── index.qmd          # ENGLANTI — synkronoidaan upstreamista
├── ZigExamples/       # JAETTU — koodiesimerkit (ei käännetä)
├── Figures/           # JAETTU — kuvat
├── Cover/             # JAETTU — kansikuva
├── Assets/            # JAETTU — teema, bibliografia, painikkeet (fi-override: fi/Assets/)
├── zig_engine.R       # JAETTU — knitr/Zig-moottori
├── _quarto.yml        # ENGLANTI — upstreamin Quarto-konfiguraatio
│
├── fi/                # SUOMI — ainoa paikka johon tehdään käännöstyötä
│   ├── _quarto.yml    # Suomenkielinen kirjan konfiguraatio
│   ├── index.qmd
│   ├── Chapters/      # Suomennetut .qmd-tiedostot (sama tiedostonimi kuin EN)
│   ├── Assets/        # Vain suomennetut HTML-pätkät (painikkeet ym.)
│   └── _freeze/       # Suomennoksen renderöintivälimuisti
│
├── scripts/
│   ├── sync-upstream.sh       # Hae ja yhdistä upstream
│   ├── translation-status.sh  # Näytä käännösten tila
│   └── new-translation.sh     # Luo uusi käännösluku pohjalta
│
└── docs/              # JULKAISTU sivusto (CI renderöi fi/-projektista)
```

### Miksi näin?

| Ongelma | Ratkaisu |
|---------|----------|
| Upstream päivittyy | Englanti pysyy repojuuressa; `git merge upstream/main` tuo muutokset |
| Konfliktit käännöksissä | Suomennos on erillisessä `fi/`-puussa; konfliktit harvoin koskevat sitä |
| Koodiesimerkit | Yksi `ZigExamples/`-kopio; ei duplikaatteja |
| Julkaisu | `fi/_quarto.yml` kirjoittaa `docs/`-hakemistoon |
| Käännöksen seuranta | Jokaisessa `fi/*.qmd`-tiedostossa `translation`-metatiedot |

## Alkuasetukset (kerran)

```bash
git remote add upstream https://github.com/pedropark99/zig-book.git
git fetch upstream
```

GitHub Pages -asetukset repossa:

1. **Settings → Pages → Build and deployment**
2. Source: **GitHub Actions** (workflow `.github/workflows/publish-fi.yml`)

## Päivittäinen työnkulku

### 1. Hae upstream-muutokset

```bash
./scripts/sync-upstream.sh
```

Tämä hakee `pedropark99/zig-book` ja yhdistää `main`-haaraan. Ratkaise mahdolliset konfliktit **vain** jaetuissa tiedostoissa (`ZigExamples/`, `Figures/` jne.) — älä muokkaa juuren `Chapters/`-tiedostoja käsin.

### 2. Tarkista käännösten tila

```bash
./scripts/translation-status.sh
```

Tila | Merkitys
-----|----------
`PUUTTUU` | Upstreamissa on luku, jolle ei ole suomennosta
`VANHENTUNUT` | Englannin `source_sha256` on muuttunut
`LUONNOS` | Suomennos on aloitettu mutta ei valmis
`VALMIS` | Käännös vastaa nykyistä upstream-versiota

### 3. Luo tai päivitä käännös

Uusi luku:

```bash
./scripts/new-translation.sh Chapters/01-zig-weird.qmd
```

Päivitä vanhentunut luku:

1. Avaa vastaava `fi/Chapters/*.qmd`
2. Vertaa englanninkieliseen `Chapters/*.qmd`-versioon (`git diff Chapters/foo.qmd`)
3. Päivitä suomennos (teksti, otsikot, alaviitteet — **älä** käännä Zig-koodia)
4. Päivitä frontmatter:

```yaml
translation:
  source: Chapters/01-zig-weird.qmd
  source_sha256: "<sha256sum Chapters/01-zig-weird.qmd>"
  status: complete   # draft | in_progress | complete
```

### 4. Rakenna ja tarkista paikallisesti

```bash
# Nix-ympäristö (suositeltu)
nix develop
Rscript dependencies.R
quarto render
```

Avaa `docs/index.html` selaimessa.

### 5. Julkaise

Push `main`-haaraan → GitHub Actions renderöi ja julkaisee automaattisesti.

## Mitä käännetään ja mitä ei

**Käännetään:**
- Otsikot ja kappaleteksti
- Kuvatekstit ja alaviitteet
- Käyttöliittymätekstit (`fi/Assets/`-painikkeet)
- Kirjan metadata (`fi/_quarto.yml`: title, subtitle)

**Ei käännetä:**
- `ZigExamples/` -koodi
- Koodilohkot `.qmd`-tiedostoissa
- Tiedostonimet ja polut
- `Assets/references.bib` (viittaukset säilyvät)

## Käännösmetatiedot

Jokaisessa suomennetussa `.qmd`-tiedostossa:

```yaml
---
translation:
  source: Chapters/01-zig-weird.qmd   # vastaava englanninkielinen tiedosto
  source_sha256: abc123...            # englannin tiedoston hash merge-jälkeen
  status: draft                         # draft | in_progress | complete
---
```

Kun upstream päivittyy, `source_sha256` ei enää täsmää → `translation-status.sh` merkitsee luvun vanhentuneeksi.

## Polkujen muistilista (`fi/`-hakemistosta)

| Tiedosto | `zig_engine.R` | `Assets/zig.xml` |
|----------|----------------|------------------|
| `fi/index.qmd` | `../zig_engine.R` | `../Assets/zig.xml` |
| `fi/Chapters/*.qmd` | `../../zig_engine.R` | `../../Assets/zig.xml` |

`new-translation.sh` säätää nämä automaattisesti.

## Lisenssi ja attribuutio

Alkuperäinen kirja: CC-BY 4.0, Pedro Duarte Faria. Suomennos on johdannaisteos; mainitse alkuperäinen teos ja tekijä. Katso [CONTRIBUTING.md](CONTRIBUTING.md) upstreamin käytännöistä.
