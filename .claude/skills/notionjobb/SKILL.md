---
name: notionjobb
description: Tilgang til Sigma2 HQ i Notion – søk, les, opprett og oppdater sider. Trigger når brukeren vil se, finne, legge til eller redigere noe i Notion-arbeidsområdet, eller sier "Notion", "Sigma2 HQ", "jobb-wiki", "notionjobb" e.l.
---

# Notionjobb – Sigma2 HQ i Notion

## Konfigurasjon

```
ENV_PATH = ~/.claude/skills/notionjobb/.env
```

| Variabel | Beskrivelse |
|---|---|
| `NOTION_TOKEN` | Internal integration secret (jobb-konto) |
| `NOTION_ROOT_PAGE_ID` | Sigma2 HQ database-ID |
| `NOTION_ROOT_URL` | Full URL til Sigma2 HQ |

**Merk:** Root-siden (`2d82cfff5fe780818989d0ad5513745a`) er en **database**, ikke en side. Bruk `/databases/` endepunkt for rotnivå, `/pages/` for undersider.

---

## Standard Python-snippet

```python
import os
import requests
from dotenv import load_dotenv

ENV_PATH = os.path.expanduser("~/.claude/skills/notionjobb/.env")
load_dotenv(dotenv_path=ENV_PATH)

TOKEN   = os.getenv("NOTION_TOKEN")
ROOT_ID = os.getenv("NOTION_ROOT_PAGE_ID", "2d82cfff5fe780818989d0ad5513745a")
BASE    = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def get(path, **kwargs):
    r = requests.get(f"{BASE}/{path}", headers=HEADERS, **kwargs)
    r.raise_for_status()
    return r.json()

def post(path, **kwargs):
    r = requests.post(f"{BASE}/{path}", headers=HEADERS, **kwargs)
    r.raise_for_status()
    return r.json()

def patch(path, **kwargs):
    r = requests.patch(f"{BASE}/{path}", headers=HEADERS, **kwargs)
    r.raise_for_status()
    return r.json()
```

---

## Operasjoner

### Hent Sigma2 HQ (database)
```python
db = get(f"databases/{ROOT_ID}")
print(db["title"][0]["plain_text"])
```

### Søk i hele workspace
```python
results = post("search", json={"query": "søketekst", "page_size": 20})
for r in results["results"]:
    title = r.get("properties", {}).get("title") or r.get("title") or []
    print(r["id"], r["object"], title[0]["plain_text"] if title else "–")
```

### Hent en side
```python
page = get(f"pages/{page_id}")
```

### Hent blokk-innhold fra en side
```python
blocks = get(f"blocks/{page_id}/children")
for b in blocks["results"]:
    btype = b["type"]
    text = b.get(btype, {}).get("rich_text", [])
    print(btype, "".join(t["plain_text"] for t in text))
```

### Søk i database (filtrert)
```python
rows = post(f"databases/{ROOT_ID}/query", json={
    "filter": {"property": "Status", "select": {"equals": "Aktiv"}},
    "page_size": 50,
})
for row in rows["results"]:
    props = row["properties"]
    name = props.get("Name", {}).get("title", [{}])[0].get("plain_text", "–")
    print(row["id"], name)
```

### Opprett ny side under Sigma2 HQ
```python
ny = post("pages", json={
    "parent": {"database_id": ROOT_ID},
    "properties": {
        "Name": {"title": [{"text": {"content": "Ny side"}}]},
    },
})
print("Opprettet:", ny["url"])
```

### Oppdater side-property
```python
patch(f"pages/{page_id}", json={
    "properties": {
        "Status": {"select": {"name": "Ferdig"}},
    },
})
```

### Legg til tekstblokk på en side
```python
post(f"blocks/{page_id}/children", json={
    "children": [{
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": "Ny tekst her"}}]
        }
    }]
})
```

---

## Tone & Stil
- Kortfattet og strukturert
- Presenter sidestruktur som punktliste med innrykk
- Vis alltid Notion-lenker der det er praktisk
- Formell tone, ingen utropstegn

---

## Tekniske notat

- **Root:** `2d82cfff5fe780818989d0ad5513745a` er en **database** (Sigma2 HQ) – bruk `/databases/` og `/databases/{id}/query`
- **Undersider** er vanlige pages – bruk `/pages/{id}` og `/blocks/{id}/children`
- **Autentisering:** `NOTION_TOKEN` fra `.env` – internal integration, jobb-workspace
- **Notion-Version header:** alltid `2022-06-28`
- **Side-ID format:** 32 hex-tegn uten bindestreker i URL, med bindestreker i API-respons
- **Paginering:** sjekk `has_more` + `next_cursor` ved mange resultater
- **Kjør Python:** `/opt/homebrew/opt/python@3.14/bin/python3.14`
