---
name: accounting-assistant
description: Regnskapsassistent – UBW Agresso / Sigma2. Hjelper med regnskapsoppfølging, bilagsbehandling, kontoanalyse og rapportering i UBW Agresso.
---

# Regnskapsassistent

Hjelper med regnskapsoppfølging og bilagsbehandling i UBW Agresso for Sigma2.

## Oppgaver
- Kontoanalyse og saldosjekk
- Bilagsbehandling og godkjenning
- Budsjettkontroll og avviksanalyse
- Periodeavslutning og rapportering
- GL-bilag og kostnadsfordeling

## Kontoplan

Ved spørsmål om hvilken konto som skal brukes, slå alltid opp i **Sigma2s kontoplan**:

```
~/Library/CloudStorage/OneDrive-Deltebiblioteker–Sikt/Sigma2 - Økonomi - Dimensjoner/DimensjonKontoplan.csv
```

Søk med Python:
```python
import csv
with open('/Users/frodesolem/Library/CloudStorage/OneDrive-Deltebiblioteker–Sikt/Sigma2 - Økonomi - Dimensjoner/DimensjonKontoplan.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))
for r in rows:
    if 'søkeord' in r['Beskrivelse'].lower():
        print(f"{r['Konto']}  {r['Beskrivelse']}  [{r['Regel']}]")
```

Bruk alltid Sigma2s kontoplan som kilde – ikke generell norsk standard kontoplan.

## Kundereskontro

Filer:
```
~/Library/CloudStorage/OneDrive-Deltebiblioteker–Sikt/Sigma2 - Økonomi - Hovedbok/Komplett kundereskontro.csv
~/Library/CloudStorage/OneDrive-Deltebiblioteker–Sikt/Sigma2 - Økonomi - Hovedbok/Kunderoversikt.csv
```

**Bilagstyper i kundereskontro:**
- **Fakturanr** er alltid **6-sifret** og starter på **4 eller 5** – positivt beløp
- **Kreditnota** er alltid **6-sifret** og starter på **4 eller 5** – negativt beløp
- Alt annet (ikke 6-sifret fakturanr) er **innbetalinger** – skal ikke tas med i omsetningsanalyse

**Kontobruk i kundereskontro:**
- Konto **15-serien** – kundefordringer/fakturering (omsetning)
- Konto **29-serien** – avsetninger (ikke omsetning; filtreres bort i omsetningsanalyse)

**Filterregler for omsetningsanalyse:**
- Fakturanr: 6 siffer, starter på 4 eller 5
- Beløp > 0 (positive poster = fakturaer; negative = kreditnotaer)
- Konto 15-serien (ikke 29-serien)
- **Norges forskningsråd** (og NFR Prefinansiering) utelates – dette er statlig finansiering, ikke en kunde
- Universiteter (UiO, UiB, UiT, NTNU) utelates ved analyse av eksterne kunder

**BOTT-universiteter** (egne analyser):
| Forkortelse | Navn | Kundenr |
|---|---|---|
| UiO | Universitetet i Oslo | 1010 |
| UiB | Universitetet i Bergen | 1011 |
| NTNU | Norges Teknisk-Naturvitenskapelige Universitet | 1046, 1224 |
| UiT | UiT Norges arktiske universitet | 1012 |

## Leverandørreskontro

Filer:
```
~/Library/CloudStorage/OneDrive-Deltebiblioteker–Sikt/Sigma2 - Økonomi - Hovedbok/Komplett leverandørreskontro.csv
~/Library/CloudStorage/OneDrive-Deltebiblioteker–Sikt/Sigma2 - Økonomi - Hovedbok/Leverandøreroversikt.csv
```

**Bilagstyper i leverandørreskontro – skilles på Bilagsnr:**
- **Bilagsnr 3YYxxxxx** – inngående faktura – negativt beløp (kostnad)
  - YY = årets to siste siffer (2019→319, 2025→325, 2026→326 osv.)
  - Kode: `bnr.startswith(f'3{str(aar)[2:]}')`
- **Bilagsnr 500xxxxx** – betaling – positivt beløp (utbetaling mot gjeld)
- **Bilagsnr 200xxxxx** – manuelle posteringer/justeringer

**Kontobruk:**
- Konto **24-serien** – leverandørgjeld/kostnadsføring

**Filterregler for kostnadsanalyse:**
- Bilagsnr starter på 319 (inngående faktura)
- Beløp < 0 (negativt = kostnad), bruk abs() for summering
- Konto 24-serien

**BOTT-universiteter som leverandører:**
| Lev.nr | Navn |
|---|---|
| 10588 | UNIVERSITETET I BERGEN (UiB) |
| 10783 | NTNU |
| 11192 | Universitetet i Oslo (UiO) |
| 11049 | Universitetet i Oslo – kun driftsstøtte |
| 12762 | UiT Norges Arktiske Universitet |
| 10844 | UNIVERSITETET I TROMSØ (gammel, erstattet av 12762) |

## Referanser
- Excelerator GL-skill for bilagsimport
- Agresso-login for tilgang til systemet
