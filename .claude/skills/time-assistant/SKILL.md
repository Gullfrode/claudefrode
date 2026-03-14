# Time-assistent – UBW Agresso timerapport

**Trigger:** Spørsmål om timer, timeføring, prosjekttid, flex, ressursbruk, uke-rapporter, eller tilsvarende.

---

## Datakilder

| Fil | Innhold |
|---|---|
| `/Users/frodesolem/Library/CloudStorage/OneDrive-Deltebiblioteker–Sikt/Sigma2 - Økonomi - Lønnstransaksjoner/{YYYY} AlleTimetransaksjoner.csv` | Timetransaksjoner per år |
| `.../Sigma2 - Økonomi - Dimensjoner/DimensjonProsjektregister.csv` | Prosjektnavn og beskrivelse |
| `.../Sigma2 - Økonomi - Dimensjoner/DimensjonProsjektleder.csv` | Prosjektleder per prosjekt |
| `.../Sigma2 - Økonomi - Dimensjoner/DimensjonRessurser.csv` | Ressursnavn (ansatte) |

Alle filer er **tab-separert** (`\t`). Desimalskilletegn er **komma** (norsk format).

---

## Nøkkelfelter i AlleTimetransaksjoner.csv

| Kolonne | Beskrivelse |
|---|---|
| `Prosjekt` | Prosjektkode (S-prefix = Sigma2) |
| `Ressnr` | Ressursnummer (ansatt-ID) |
| `Periode` | YYYYWW-format (uke 10 i 2025 = 202510) |
| `Bilagsdato` | DD.MM.YYYY |
| `Timer` | Antall timer (komma som desimal) |

## Viktige koder

| Kode | Betydning |
|---|---|
| `S9990015` | **Flexitid** – negative timer = flex-uttak, positive = flex-opptjening |
| `S291xxxx` | **Interne prosjekter** (admin, kompetanse, ledelse, etc.) |
| `S201xxxx` | **Operative prosjekter** (HPC, NRIS, tjenester) |

## Frode Solem
- **Ressursnr:** `39036`
- **Standarduke:** 37,5 timer

---

## Instruksjoner til Claude

### Generelt
- Les alltid riktig årsbasert fil basert på perioden brukeren spør om
- Hvis perioden spenner over flere år, les alle relevante årsbaserte filer
- Bruk Python via Bash for parsing – håndter komma som desimaltegn

### Periodesyntaks
- Uke 2 i 2022 = `202202`
- Uke 25 i 2025 = `202525`
- Brukeren kan oppgi periode som enkeltuke, rekke (202501–202512), eller fritekst ("januar 2025", "Q1 2025")
- Konverter fritekst til YYYYWW-format før analyse

### Standard Python-snippet for parsing

```python
import csv, sys
from collections import defaultdict

TRANS_BASE = "/Users/frodesolem/Library/CloudStorage/OneDrive-Deltebiblioteker\u2013Sikt/Sigma2 - \u00d8konomi - L\u00f8nnstransaksjoner"
DIM_BASE = "/Users/frodesolem/Library/CloudStorage/OneDrive-Deltebiblioteker\u2013Sikt/Sigma2 - \u00d8konomi - Dimensjoner"

def les_csv(fil):
    with open(fil, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f, delimiter='\t'))

def til_timer(s):
    return float(s.replace(',', '.')) if s.strip() else 0.0

# Last dimensjoner
prosjekter = {r['Prosjekt']: r['Beskrivelse'] for r in les_csv(f"{DIM_BASE}/DimensjonProsjektregister.csv")}
ressurser = {r['Ressnr']: r['Navn'] for r in les_csv(f"{DIM_BASE}/DimensjonRessurser.csv")}

# Prosjektledere: {prosjektkode: ledernavn}
pl_rows = les_csv(f"{DIM_BASE}/DimensjonProsjektleder.csv")
prosjektledere = {r['Prosjekt']: r['Ressnr(T)'] for r in pl_rows}
```

### Analyse-typer

**1. Timer per uke for Frode (ressursnr 39036)**
- Summer `Timer` per `Periode` og `Prosjekt`
- Skill ut `S9990015` (flex) og vis separat
- Vis totalt fakturerbart vs. intern/admin tid

**2. Timer per prosjekt (periode)**
- Grupper på `Prosjekt`, slå opp `Beskrivelse` fra DimensjonProsjektregister
- Legg til prosjektleder fra DimensjonProsjektleder

**3. Ressursbruk på prosjekt**
- Grupper på `Ressnr`, slå opp navn fra DimensjonRessurser
- Nyttig for å se hvem som jobber på et prosjekt

**4. Flex-saldo**
- Hent alle rader med `Prosjekt = S9990015`
- Summer `Timer` – negativt = flex-uttak, positivt = opptjening
- Saldo = sum over valgt periode

---

## Output-format

```
TIMER – [PERIODE / NAVN]
Ressurs: [Navn] (Ressnr: XXXXX)

PROSJEKT                  BESKRIVELSE                  TIMER
S2010607                  [Prosjektnavn]               XX,X t
S2910001                  Generell administrasjon      XX,X t
...
─────────────────────────────────────────────────────
Total arbeidstid:         XX,X t
Flex (S9990015):          ±X,X t
Netto arbeid:             XX,X t

Arbeidsuke-norm:          37,5 t/uke × [N uker] = XXX t
Avvik fra norm:           ±X,X t
```

---

## Tone & Stil

- Kortfattet og strukturert
- Punkt-lister / tabeller
- Ingen utropstegn
- Flagg avvik fra normen (for mye/lite tid ført)

---

## Tekniske notat

- Filer er tab-separert med norsk desimalkomma
- Encoding: `utf-8-sig` (BOM)
- Årsbasert filnavn: `{YYYY} AlleTimetransaksjoner.csv`
- `AlleTimetransaksjoner.csv` (uten årsprefix) kan inneholde alle år – bruk årsfilene for ytelse
- Datoformat i filen: `DD.MM.YYYY`
- Type-kolonne (T/A/B): ignoreres normalt, men B = bokført/godkjent
