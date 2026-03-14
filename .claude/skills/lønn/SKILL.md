# Lønnsmedarbeider – Sigma2

**Trigger:** Spørsmål om lønn, lønnstransaksjoner, lønnarter, ansatte, ressnr, lønnsperiode, eller tilsvarende.

---

## Datakilder

```
LONN_TRANS = "/Users/frodesolem/Library/CloudStorage/OneDrive-Deltebiblioteker–Sikt/Sigma2 - Økonomi - Lønnstransaksjoner/AlleLønnstransaksjoner.csv"
DIM        = "/Users/frodesolem/Library/CloudStorage/OneDrive-Deltebiblioteker–Sikt/Sigma2 - Økonomi - Dimensjoner"
```

### Dimensjonsfiler (tab-separert om ikke annet)

| Fil | Kolonner |
|---|---|
| `DimensjonLonnart.csv` | Lønnart, Tekst, Konto, Motkonto |
| `DimensjonKontoplan.csv` | Konto, Beskrivelse, Regel, Gruppe, Type |
| `DimensjonKontostandardkobling.csv` | Konto, NS4120, NS4120 tekst, Regnskapsloven (**semikolon**-sep) |
| `DimensjonProsjektleder.csv` | Tjeneste, Prosjekt, Prosjekt(T), Ressnr(T) |
| `DimensjonRessurser.csv` | Ressnr, Navn, Ressurstype, Status |
| `DimensjonPårørende.csv` | Navn, Ressnr, Ressnr(T), Forhold, Adresse, Telefon, Mobil |
| `DimensjonProsjektRessurser.csv` | Ressnr, Navn, RT, Lev.nr, Dato fra, Dato til |

---

## Transaksjonskolonner (tab-separert)

`T | Ressnr | Lønnart | Tekst | Periode | Bilagsnr | S | T | P0 Ant/Gr.lag | Beløp`

| Kolonne | Beskrivelse |
|---|---|
| `T` | Type – `C` = lønnspost |
| `Ressnr` | Ressursnummer (ansatt-ID) |
| `Lønnart` | Kode for lønnsart |
| `Periode` | YYYYMM (f.eks. 202312 = desember 2023) |
| `Beløp` | Komma som desimaltegn |

---

## Standard Python-snippet

```python
import csv
from collections import defaultdict

LONN_TRANS = "/Users/frodesolem/Library/CloudStorage/OneDrive-Deltebiblioteker\u2013Sikt/Sigma2 - \u00d8konomi - L\u00f8nnstransaksjoner/AlleLønnstransaksjoner.csv"
DIM = "/Users/frodesolem/Library/CloudStorage/OneDrive-Deltebiblioteker\u2013Sikt/Sigma2 - \u00d8konomi - Dimensjoner"

def les_tab(fil):
    with open(fil, encoding='latin-1') as f:
        return list(csv.DictReader(f, delimiter='\t'))

def les_sc(fil):
    with open(fil, encoding='latin-1') as f:
        return list(csv.DictReader(f, delimiter=';'))

def til_beløp(s):
    return float(s.strip().replace('\xa0','').replace(' ','').replace(',','.')) if s.strip() else 0.0

# Dimensjoner
ressurser  = {r['Ressnr']: r for r in les_tab(f"{DIM}/DimensjonRessurser.csv")}
lonnarter  = {r['Lønnart']: r for r in les_tab(f"{DIM}/DimensjonLonnart.csv")}
kontoplan  = {r['Konto']: r for r in les_tab(f"{DIM}/DimensjonKontoplan.csv")}

# Transaksjoner
trans = les_tab(LONN_TRANS)
```

---

## Analyse-typer

### 1. Ansattoppslag
- Søk case-insensitivt på navn i `DimensjonRessurser` → finn `Ressnr`
- Hent alle transaksjoner for `Ressnr`
- Grupper på periode og lønnart

### 2. Lønnsoversikt per ansatt
- Filtrer transaksjoner på `Ressnr`
- Grupper på `Periode` og `Lønnart`
- Summer `Beløp`
- Slå opp lønnartsbeskrivelse fra `DimensjonLonnart`

### 3. Periodesummering
- Grupper transaksjoner på `Periode` og `Lønnart`
- Vis totaler per år eller måned
- Filtrer på `T = C` for rene lønnsposter

### 4. Prosjektkoblinger
- `DimensjonProsjektleder` kobler `Ressnr(T)` (format "Etternavn, Fornavn") mot prosjekter
- `DimensjonProsjektRessurser` kobler `Ressnr` mot prosjektperioder (`Dato fra`/`Dato til`)

### 5. Kontoplankoblinger
- `Lønnart` → `DimensjonLonnart` (Konto) → `DimensjonKontoplan` (Beskrivelse) → `DimensjonKontostandardkobling` (NS4120, Regnskapsloven)

### 6. Pårørende-oppslag
- Finn `Ressnr` fra `DimensjonRessurser` → slå opp i `DimensjonPårørende`
- Vis kun når eksplisitt spurt om

---

## Periodesyntaks

| Bruker sier | Tolkes som |
|---|---|
| "mars 2025" | Periode = 202503 |
| "Q1 2025" | Periode 202501–202503 |
| "2025" | Alle perioder 202501–202512 |
| "YTD" | Januar t.o.m. inneværende måned i inneværende år |

---

## Output-format

```
LØNNSOVERSIKT – [NAVN] – [PERIODE]

PERIODE    LØNNART    BESKRIVELSE          BELØP
202501     100        Fastlønn             XX XXX kr
202501     520        Overtid              X XXX kr
...
Sum:                                       XX XXX kr
```

---

## Tekniske notat

- Encoding: `latin-1` på de fleste filer
- Beløp: komma som desimaltegn – bruk `decimal=','` i pandas, eller `replace(',','.')` ved csv-lesing
- Non-breaking space (`\xa0`) kan forekomme som tusenskilletegn – strip dette
- `DimensjonKontostandardkobling.csv` er **semikolon**-separert, alle andre er tab-separert
- Vis beløp i norsk format: mellomrom som tusenskilletegn, komma som desimal
- Sensitiv personalinfo (pårørende, adresse): vis kun når eksplisitt spurt om
