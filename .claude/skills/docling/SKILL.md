---
name: docling
description: Konverter dokumenter (PDF, Word, PowerPoint, bilder, HTML, CSV, XLSX m.fl.) til Markdown eller andre formater ved hjelp av docling. Bruk når brukeren vil konvertere et dokument, "gjør om til md", "lag markdown av denne", "konverter PDF", eller vil ha tekst ut av en fil.
allowed-tools: Bash
---

# Docling – dokumentkonvertering

Konverter dokumenter til Markdown (eller andre formater) med docling.

## Script

```
/Users/frodesolem/Library/Mobile Documents/com~apple~CloudDocs/scripts/docling
```

## Bruk

```bash
# Enkel konvertering til Markdown (standard)
docling <fil>

# Spesifiser output-format
docling --to md <fil>
docling --to json <fil>
docling --to html <fil>

# Spesifiser output-mappe
docling --output /sti/til/mappe <fil>

# Fra URL
docling https://example.com/dokument.pdf
```

## Input-formater som støttes

`pdf`, `docx`, `pptx`, `html`, `image` (PNG/JPG), `csv`, `xlsx`, `md`, `asciidoc`

## Output-formater

`md` (standard), `json`, `yaml`, `html`, `text`, `doctags`

## Bilder

Obsidian Filer-mappe: `/Users/frodesolem/Library/Mobile Documents/iCloud~md~obsidian/Documents/Mi Casa/Filer`

Bilder skal legges **flatt** i Filer-mappen (ikke i undermappe). Navngiving: `<dokumentnavn>-1.png`, `<dokumentnavn>-2.png` osv. Hvis en fil med samme navn allerede finnes, fortsett løpenummeret fra der det slutter.

Siden docling legger bilder i en undermappe automatisk, gjør dette etterpå:

1. Kjør docling med `--image-export-mode referenced` og `/tmp` som output
2. Flytt bildene fra `/tmp/<dokumentnavn>-images/` flatt til Filer-mappen med riktig navngiving
3. Oppdater bildereferansene i den genererte `.md`-filen til å peke på Filer-mappen
4. Flytt/lagre `.md`-filen til ønsket destinasjon

```python
import os, re, shutil
from pathlib import Path

FILER = Path("/Users/frodesolem/Library/Mobile Documents/iCloud~md~obsidian/Documents/Mi Casa/Filer")
docname = "dokument"  # dokumentnavn uten extension
img_dir = Path(f"/tmp/{docname}-images")
md_file = Path(f"/tmp/{docname}.md")

# Finn neste ledige løpenummer for dette dokumentet
existing = [f.stem for f in FILER.glob(f"{docname}-*.png")] + \
           [f.stem for f in FILER.glob(f"{docname}-*.jpeg")]
nums = [int(s.rsplit("-", 1)[-1]) for s in existing if s.rsplit("-", 1)[-1].isdigit()]
next_num = max(nums, default=0) + 1

# Flytt bilder og bygg mapping gammel→ny referanse
ref_map = {}
for i, img in enumerate(sorted(img_dir.glob("*")), start=next_num):
    new_name = f"{docname}-{i}{img.suffix}"
    shutil.move(str(img), str(FILER / new_name))
    ref_map[img.name] = new_name

# Oppdater referanser i markdown-filen
md_text = md_file.read_text()
for old, new in ref_map.items():
    md_text = md_text.replace(old, new)
md_file.write_text(md_text)

# Rydd opp tom bildemappe
if img_dir.exists():
    shutil.rmtree(img_dir)
```

Bruk dette Python-snippetet via Bash etter docling-kjøringen. Tilpass `docname` til faktisk dokumentnavn.

For dokumenter uten bilder kan du bruke `/tmp` direkte uten post-prosessering.

## Fremgangsmåte

1. Finn filen brukeren refererer til (sjekk skrivebordet, Downloads, eller spør)
2. Bestem output-format (Markdown er standard)
3. Sjekk om dokumentet sannsynligvis inneholder bilder (PDF med layout, Word med figurer, etc.)
   - Med bilder → kjør docling til `/tmp`, deretter flytt bilder flatt til Filer med Python-snippetet
   - Uten bilder → kjør docling direkte til ønsket mappe
4. Kjør docling med Bash
5. Post-prosesser bilder om nødvendig
6. Les den konverterte filen og presenter innholdet, eller lagre den der brukeren ønsker

## Typiske eksempler

**PDF med bilder:**
```bash
DOCNAME="dokument"
"/Users/frodesolem/Library/Mobile Documents/com~apple~CloudDocs/scripts/docling" \
  --to md --image-export-mode referenced --output /tmp \
  "/Users/frodesolem/Desktop/${DOCNAME}.pdf" 2>&1 | grep -v "INFO\|WARNING\|NotOpen\|^2026"
# Deretter: kjør Python-snippetet over med docname = "$DOCNAME"
```

**Enkel PDF uten bilder:**
```bash
"/Users/frodesolem/Library/Mobile Documents/com~apple~CloudDocs/scripts/docling" \
  --output /tmp \
  "/Users/frodesolem/Desktop/dokument.pdf" 2>&1 | grep -v "INFO\|WARNING\|NotOpen\|^2026"
```

## Merk

- Logg-output fra docling er verbose – filtrer bort INFO/WARNING-linjer ved presentasjon
- OCR-støtte er tilgjengelig for bilder og skannede PDFer (bruker `ocrmac` på Mac)
- Output-fil får samme navn som input, men med ny extension (f.eks. `dokument.md`)
- Obsidian finner bilder i Filer-mappen automatisk via filnavn (ingen full sti nødvendig i `![[]]`-referanser)
