# Excelerator GL-bilag – Strukturnotat

## Konsept
Excelerator er et Excel-grensesnitt mot UBW Agresso (Citrix). Man åpner en .xlsx-fil inne i Citrix/Excel, og systemet leser og bokfører innholdet direkte i Agresso via BI-interface.

Eksempelfiler: `2025 03 Bilag 12600030.xlsx` og `12600031.xlsx`

---

## Filstruktur

### Ark 1: `_control`
Globale parametere. Kun rad 7, 8 og 9 (batch_id, period, voucher_date) endres per bilag.

| Rad | Kolonne A | Kolonne B (key) | Kolonne C (value) | Kommentar |
|-----|-----------|-----------------|-------------------|-----------|
| 6 | setdefault | client | client | Firmakode – fast |
| 7 | setdefault | batch_id | **20260300** | Unik bunt-ID. Format: YYYYMM + løpenr (00, 01, 02...) |
| 8 | setdefault | period | **202603** | Periode YYYYMM (1–12, noen år periode 13) |
| 9 | setdefault | voucher_date | **2026-03-02** | Bokføringsdato |
| 10 | setdefault | voucher_no | None | Auto-tildeles av Agresso (vouch_flag=Y) |
| 11 | setdefault | voucher_type | GL | Bilagsart – GL for General Ledger |
| 12 | setdefault | user_id | user_id | Bruker – fast |
| 13 | setdefault | currency | NOK | Valuta – fast |
| 14 | setdefault | vouch_flag | Y | Y = Agresso tildeler bilagsnr automatisk |
| 15 | setdefault | variant_number | 9 | Post-back parameter for GL07 – fast |
| 16 | setdefault | trans_type | GL | Transaksjonstype – fast |
| 17 | setdefault | interface | BI | Forsystem – fast |

### Ark 2: `Postering til UBW`
- Rad 1–8: Tomme / overskrift ("Hovedbokstransaksjoner" i rad 2 kolonne C)
- **Rad 9**: Kolonneoverskrifter (update_columns)
- **Rad 10+**: Posteringslinjer (update_data)

#### Rad 9 – kolonneoverskrifter:
```
update_columns | account | dim_1 | dim_2 | dim_3 | dim_4 | dim_6 | tax_code | amount | cur_amount | description
```

#### Rad 10+ – posteringslinjer:
```
update_data | [konto] | [dim1] | [dim2] | [dim3] | [dim4] | [dim6] | [mva] | [beløp] | [beløp] | [tekst]
```

- `amount` = `cur_amount` (samme tall, NOK)
- Debet = positivt tall, Kredit = negativt tall
- Bilaget må balansere (sum = 0)
- `dim_3` = ressursnr/leverandørnr (f.eks. 39026 for Basir)

---

## Eksempler

### Bilag 12600030 – Egenandel iPhone
```
update_data | 65500 | S1 | S2910001 | 39038 | | | | -1798 | -1798 | Egenandel iPhone 17 Pro Max
update_data | 15791 |    |          |       | | | |  1798 |  1798 | Egenandel iPhone 17 Pro Max
```
- 65500 krediteres (reduserer kostnad), dim3=ansattnr
- 15791 debiteres (fordring på ansatt)

### Bilag 12600031 – Trekk utkjøp PC
```
update_data | 65500 | S1 | S2910001 | 39023 | | | | -500 | -500 | Trekk utkjøp PC
update_data | 15791 |    |          |       | | | | -500 | -500 | Trekk utkjøp PC
```

---

## Regler
- **batch_id** må være unik – format YYYYMM + 2-sifret løpenr (f.eks. 20260300)
- **period** = YYYYMM. Periode 1–12, noen år finnes periode 13
- **voucher_date** = dato i cellen (Excel datetime)
- Kun GL-bilag (variantnr 9, voucher_type GL)
- Rad 1–9 i ark "Postering til UBW" kan stå fast – kun endre fra rad 10
- Overskriftene i rad 9 teller – ikke rad 1–8

---

## Dimensjoner (Dim)
- dim_1 = Koststed (f.eks. S1)
- dim_2 = Prosjekt (f.eks. S2910001)
- dim_3 = Ressursnr / Leverandørnr (f.eks. 39026 = Basir Sedighi)
- dim_4, dim_6 = sjelden brukt, settes til None

---

## Typiske GL-bilag
- Krysspostering av forskudd (EG → kryssing av åpne 29300-poster)
- Egenandeler (trekk fra ansatt via 15791)
- Manuelle korreksjoner

---

## Neste steg (skill-utvikling)
- [ ] Lag Python-funksjon som genererer xlsx fra input (periode, dato, linjer)
- [ ] batch_id-logikk: hent høyeste brukte og inkrementer
- [ ] Validering: sum = 0, påkrevde felt, gyldig periode
- [ ] Output til Desktop eller definert mappe
