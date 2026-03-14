# ecoissues – GitLab Issues Ecodream

**Trigger:** Spørsmål om GitLab-saker, issues, oppgaver, milepæler eller status i ecodream-prosjektet.

---

## Konfigurasjon

```
ENV_PATH    = ~/Library/Mobile Documents/com~apple~CloudDocs/scripts/snippets/laggitlabissues/.env
GITLAB_URL  = https://gitlab.sigma2.no/api/v4
PROJECT_ID  = 1020        (ecodream-prosjektet)
GROUP_PATH  = ecodream    (gruppen – brukes for gruppemilepæler)
```

| Variabel | Kilde |
|---|---|
| `GITLAB_PRIVATE_TOKEN` | `.env`-filen over |
| `GITLAB_URL` | `.env`-filen over |
| `PROJECT_ID` | `.env` (default `1020`) |
| `GROUP_PATH` | hardkodet `ecodream` |

---

## Standard Python-snippet

```python
import requests
import datetime
import os
from dotenv import load_dotenv

ENV_PATH = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/scripts/snippets/laggitlabissues/.env"
)
load_dotenv(dotenv_path=ENV_PATH)

GITLAB_URL = os.getenv("GITLAB_URL")
TOKEN      = os.getenv("GITLAB_PRIVATE_TOKEN")
PROJECT_ID = os.getenv("PROJECT_ID", "1020")
GROUP_PATH = "ecodream"
HEADERS    = {"Private-Token": TOKEN, "Content-Type": "application/json"}

def api(method, path, **kwargs):
    url = f"{GITLAB_URL}/projects/{PROJECT_ID}/{path}"
    r = getattr(requests, method)(url, headers=HEADERS, **kwargs)
    r.raise_for_status()
    return r.json()

def group_api(method, path, **kwargs):
    url = f"{GITLAB_URL}/groups/{GROUP_PATH}/{path}"
    r = getattr(requests, method)(url, headers=HEADERS, **kwargs)
    r.raise_for_status()
    return r.json()

def milestone_id(navn):
    """Søker først i prosjektmilepæler, deretter i gruppemilepæler."""
    # Prosjektmilepæler
    ms = api("get", "milestones", params={"search": navn, "state": "active"})
    for m in ms:
        if m["title"].lower() == navn.lower():
            return m["id"]
    # Gruppemilepæler
    ms = group_api("get", "milestones", params={"search": navn, "state": "active"})
    for m in ms:
        if m["title"].lower() == navn.lower():
            return m["id"]
    return None

def fmt_dato(iso):
    """2026-04-01 → 01.04.2026"""
    if not iso: return "–"
    return datetime.date.fromisoformat(iso).strftime("%d.%m.%Y")
```

---

## Analyse-typer

### 1. Hent åpne issues
```python
issues = api("get", "issues", params={"state": "opened", "per_page": 100})
```

### 2. Filtrer på label / person
```python
issues = api("get", "issues", params={"labels": "Frode", "state": "opened", "per_page": 100})
```

### 3. Søk på tittel
```python
issues = api("get", "issues", params={"search": "søketekst", "state": "opened"})
```

### 4. Overdue (forfalt, fortsatt åpen)
```python
i_dag   = datetime.date.today().isoformat()
alle    = api("get", "issues", params={"state": "opened", "per_page": 100})
overdue = [s for s in alle if s.get("due_date") and s["due_date"] < i_dag]
```

### 5. Issues for milepæl
```python
mid    = milestone_id("Q2 2026")
issues = api("get", "issues", params={"milestone_id": mid, "per_page": 100})
```

### 6. Opprett issue
```python
ny = api("post", "issues", json={
    "title": "Tittel",
    "labels": "Frode,ikke starta",
    "due_date": "2026-04-01",
    "milestone_id": milestone_id("Q2 2026"),
    "description": "Valgfri beskrivelse",
})
print(f"#{ny['iid']} opprettet")
```

### 7. Oppdater issue
```python
api("put", f"issues/{iid}", json={
    "title": "Ny tittel",
    "labels": "Frode,complete",
    "due_date": "2026-05-01",
    "state_event": "close",     # eller "reopen"
})
```

### 8. Legg til kommentar
```python
api("post", f"issues/{iid}/notes", json={"body": "Kommentartekst"})
```

### 9. List prosjektmilepæler
```python
ms = api("get", "milestones", params={"state": "active"})
for m in ms:
    print(f"  ID {m['id']}: {m['title']}")
```

### 10. List gruppemilepæler
```python
ms = group_api("get", "milestones", params={"state": "active"})
for m in ms:
    print(f"  ID {m['id']}: {m['title']} (gruppe)")
```

---

## Output-format

```
ECODREAM ISSUES – [FILTER/PERIODE]

#    TITTEL                          LABELS           FORFALL      STATUS
123  Implementer internkontroll      Frode,Q2 2026    01.04.2026   åpen
124  Fakturering mars                Calle            –            åpen
...
Totalt: N saker  |  Overdue: N
```

---

## Tone & Stil
- Kortfattet og strukturert
- Datoer vises som DD.MM.YYYY
- Flagg overdue-saker tydelig

---

## Tekniske notat
- API-base: `https://gitlab.sigma2.no/api/v4`
- Autentisering: `Private-Token`-header fra `.env`
- Project ID `1020` = ecodream-prosjektet; kan overstyres med `PROJECT_ID` i `.env`
- Gruppe `ecodream` – milepæler på gruppenivå nås via `/groups/ecodream/milestones`
- `milestone_id()` søker prosjektmilepæler først, deretter gruppemilepæler
- Issue-nummer: bruk `iid` (intern, prosjektspesifikk) – ikke global `id`
- Labels: kommaseparert streng inn/ut fra API
- Datoformat: `YYYY-MM-DD` mot API, vis som `DD.MM.YYYY`
- Paginering: `per_page=100`; sjekk `X-Next-Page`-header ved mange saker
- SSH-tilgang til GitLab: `ssh gitlab` (konfigurert i `~/.ssh/config`)
