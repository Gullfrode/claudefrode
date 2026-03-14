---
name: pandoc
description: Konverter Obsidian Markdown-filer til Word (docx), PDF eller PowerPoint (pptx) med Sigma2-maler via Pandoc. Bruk når brukeren vil eksportere eller konvertere en md-fil til et Office-format, lage presentasjon fra Markdown, eller si "lag en Word av denne", "eksporter til PDF", "lag PowerPoint", "konverter til pptx" o.l.
allowed-tools: Bash
---

# Pandoc – Markdown til Office-formater

Konverter Obsidian Markdown-filer til Word, PDF eller PowerPoint med Sigma2s dokumentmaler.

**Alle script tar én Markdown-fil som argument og lagrer output på skrivebordet.**

## Scriptoversikt

| Script | Output | Mal |
|--------|--------|-----|
| `pandocdocx` | `.docx` | Sigma2 brevmal |
| `pandocpdf` | `.pdf` | Sigma2 bakgrunn (XeLaTeX) |
| `pandocpptd` | `.pptx` | Sigma2 dark |
| `pandocpptl` | `.pptx` | Sigma2 white/light |
| `pandocpptki` | `.pptx` | KIfabrikken |

**Scriptmappe:** `/Users/frodesolem/Library/Mobile Documents/com~apple~CloudDocs/scripts/`

## Bruk

```bash
SCRIPTS="/Users/frodesolem/Library/Mobile Documents/com~apple~CloudDocs/scripts"

# Word
"$SCRIPTS/pandocdocx" "/sti/til/fil.md"

# PDF
"$SCRIPTS/pandocpdf" "/sti/til/fil.md"

# PowerPoint – Sigma2 dark
"$SCRIPTS/pandocpptd" "/sti/til/fil.md"

# PowerPoint – Sigma2 white
"$SCRIPTS/pandocpptl" "/sti/til/fil.md"

# PowerPoint – KIfabrikken
"$SCRIPTS/pandocpptki" "/sti/til/fil.md"
```

Output lagres alltid på: `/Users/frodesolem/Desktop/<filnavn>.<ext>`

## Hvilken mal skal brukes?

Spør brukeren hvis det ikke fremgår av konteksten:
- **Word** → `pandocdocx` (brev, rapporter, notater)
- **PDF** → `pandocpdf` (ferdig dokument med Sigma2-design)
- **Presentasjon** → spør om dark (`pandocpptd`), white (`pandocpptl`) eller KIfabrikken (`pandocpptki`)
  - Dark er standard Sigma2-presentasjon
  - White brukes til lysere varianter
  - KIfabrikken brukes til KI-fabrikken-relaterte presentasjoner

## Obsidian-bilder

Scriptene konverterer automatisk Obsidian-bildelenker `![[bilde.png]]` til standard Markdown før konvertering. Bilder hentes fra:
`/Users/frodesolem/Library/Mobile Documents/iCloud~md~obsidian/Documents/Mi Casa/Filer`

## PowerPoint-struktur i Markdown

For pptx gjelder:
- `#` = tittelslide
- `##` = ny slide (tittel)
- Innhold under `##` = slideinnhold
- `pandocpptki` bruker `--slide-level=2` eksplisitt

## Fremgangsmåte

1. Finn markdown-filen (sjekk Obsidian-vault eller spør)
2. Avklar ønsket format og mal
3. Kjør riktig script med full filsti
4. Output ligger på skrivebordet

## Merk

- Filen må være `.md` – scriptene stripper extension og legger til riktig output-extension
- PDF krever XeLaTeX (`/Library/TeX/texbin/xelatex`) – må være installert
- Scriptene kjører i filens katalog, så relative referanser i Markdown fungerer
