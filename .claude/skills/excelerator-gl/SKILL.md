# Excelerator GL-bilag – UBW Agresso / Sigma2

**Trigger:** Bruker vil lage et GL-bilag / journal entry / krysspostering / manuelt bilag i Agresso via Excelerator.

---

## Konsept

Excelerator er et Excel-grensesnitt mot UBW Agresso. Filen åpnes i Excel inne i Citrix og importeres direkte. Skillen genererer en klar .xlsx-fil på Skrivebordet.

**Generator:** `.claude/skills/excelerator-gl/generate_gl_bilag.py`

---

## Fremgangsmåte

1. **Spør bruker om:**
   - Periode (YYYYMM, f.eks. 202603) – eller utled fra kontekst/dato
   - Bokføringsdato (DD.MM.YYYY)
   - Posteringslinjer: konto, dim1/dim2/dim3, beløp (debet+/kredit−), tekst
   - Eventuelt filnavn (autogenereres ellers)

2. **Generer filen** med Python-scriptet via Bash

3. **Bekreft** filsti og sum = 0

---

## Filstruktur

### Ark `_control` – kun disse endres:

| Felt | Format | Eksempel |
|---|---|---|
| `batch_id` | YYYYMM + 2-sifret løpenr | `20260300` |
| `period` | YYYYMM | `202603` |
| `voucher_date` | datetime | `2026-03-02` |

Alt annet er fast: `voucher_type=GL`, `variant_number=9`, `vouch_flag=Y`, `interface=BI`

### Ark `Postering til UBW`

- Rad 9: `update_columns` – kolonneoverskrifter (fast)
- Rad 10+: `update_data` – én linje per postering

Kolonner: `account | dim_1 | dim_2 | dim_3 | dim_4 | dim_6 | tax_code | amount | cur_amount | description`

---

## Dimensjoner

| Dim | Innhold | Eksempel |
|---|---|---|
| dim_1 | Koststed | `S1` |
| dim_2 | Prosjekt | `S2910001` |
| dim_3 | Ressursnr / Leverandørnr | `39026` (Basir) |
| dim_4, dim_6 | Sjelden brukt | None |

---

## Periodesyntaks

| Bruker sier | Tolkes som |
|---|---|
| "mars 2026" | 202603 |
| "januar" | 202601 (inneværende år) |
| "forrige måned" | utled fra today() |

Perioder: 1–12. Noen år finnes periode 13 (avslutningsperiode).

---

## Valideringsregler

- **Sum må være 0** (bilaget balanserer)
- `batch_id` må være unik – scriptet finner neste ledige automatisk
- `account`, `amount`, `description` er påkrevde felt per linje
- Beløp: debet = positivt, kredit = negativt

---

## Typiske brukstilfeller

### Krysspostering av åpne GL-forskudd (29300)
Brukes når GL-bilag med forskudd ikke er formelt krysset mot reiseregning.
```
update_data | 29300 | | | | | | | -9789 | -9789 | Kryssing Stockholm 21.-23.10.25
update_data | 29300 | | | | | | |  9789 |  9789 | Kryssing Stockholm 21.-23.10.25
```

### Egenandel fra ansatt (trekk i lønn / fordring)
```
update_data | 65500 | S1 | S2910001 | 39026 | | | | -1798 | -1798 | Egenandel iPhone
update_data | 15791 |    |          |       | | | |  1798 |  1798 | Egenandel iPhone
```

---

## Python-eksempel (direkte kjøring)

```python
from generate_gl_bilag import lag_gl_bilag
from datetime import datetime

fil = lag_gl_bilag(
    periode=202603,
    bokføringsdato=datetime(2026, 3, 10),
    linjer=[
        {"account": 29300, "amount": -9789.0, "description": "Kryssing Stockholm"},
        {"account": 29300, "amount":  9789.0, "description": "Kryssing Stockholm"},
    ]
)
print(f"Lagret: {fil}")
```

---

## Output

Fil lagres på `~/Desktop/` med navn: `YYYY MM Bilag {batch_id}.xlsx`

---

## Tekniske notat

- `amount = cur_amount` alltid (kun NOK støttes)
- `voucher_no = None` → Agresso tildeler automatisk
- Filen må åpnes i Excel inne i **Citrix** for å importeres
- batch_id-logikk: scriptet scanner Desktop etter eksisterende xlsx med `_control`-ark

---

*Basert på eksempelfiler: `2025 03 Bilag 12600030.xlsx` og `12600031.xlsx`*
