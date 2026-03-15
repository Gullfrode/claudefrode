---
name: erpsystem
description: ERP-prosjektstyring – synkroniser Microsoft Project (.mpp) med GitLab ERPsystem-prosjektet. Trigger når brukeren vil oppdatere issues, milepæler eller Kanban-board fra projectfil, eller sier "oppdater erp", "synkroniser prosjektplan", "erpsystem gitlab" o.l.
allowed-tools: Bash, Read, Write, Edit
---

# ERPsystem – Prosjektstyring via GitLab

Kobler Microsoft Project-filer (.mpp) mot GitLab-prosjektet `ecodream/erpsystem`.

---

## Konfigurasjon

```
GITLAB_URL   = https://gitlab.sigma2.no/api/v4
PROJECT_ID   = 1035          (ecodream/erpsystem)
GROUP        = ecodream       (gruppe – brukes for gruppemilepæler)
ENV_PATH     = ~/Library/Mobile Documents/com~apple~CloudDocs/scripts/snippets/laggitlabissues/.env
MPP_DEFAULT  = ~/Desktop/Økonomisystem_plan.mpp
```

**Token:** Gruppe-bot i `.env` (må ha Maintainer+ på gruppe for å oppdatere gruppemilepæler)

---

## Les MPP-fil

MPP er binærformat – bruk `mpxj` via Python:

```bash
pip install mpxj
```

```python
from mpxj import ProjectReader
reader = ProjectReader()
project = reader.read("/path/to/fil.mpp")
for task in project.tasks:
    print(task.id, task.name, task.start, task.finish, task.duration)
```

**Milepæler i MPP:** Oppgaver med `M`-prefiks i navn og 1-dags varighet.

---

## Kanban-board

**Board ID:** 470 | **Lister (pos 0–3):**

| Posisjon | Label | Farge |
|---|---|---|
| 0 | `fremtidige` | `#6699CC` |
| 1 | `ikke starta` | `#d9534f` |
| 2 | `iarbeid` | `#f0ad4e` |
| 3 | `complete` | `#5cb85c` |

**Regel:** Issues med `due_date > i dag + 7 dager` → `fremtidige`. Øvrige åpne → `ikke starta`.

---

## Gruppemilepæler (ERP-spesifikke)

| GitLab id | iid | Tittel |
|---|---|---|
| 374 | 17 | M7 RFI publisert |
| 370 | 13 | M6 DG 3.1 Konkurransedokumenter |
| 371 | 14 | M8 Konkurranse kunngjort i Doffin/TED |
| 372 | 15 | M9 Utsendelse av konkurransegrunnlag |
| 373 | 16 | M10 Forhandling 1 gjennomført |
| 376 | 19 | M11 DG3.2 Tildelingsbeslutning |
| 375 | 18 | M12 Tildelingsbrev sendt |
| 377 | 20 | M13 Kontrakt signert |
| 379 | 22 | M14 Idriftsettelse |
| 378 | 21 | M15 Gammelt system utfaset |
| 380 | 23 | M16 DG5 End project report |

**NB:** Milepæler kan ikke slettes av prosjekt-bot – krever gruppe-Maintainer+.
**NB:** `due_date` må være > `start_date` (GitLab-begrensning).
**NB:** Enkeltdags-milepæler (start=due) avvises – sett start én dag før.

---

## Issues – format

Hvert issue har:
- `**Startdato:** YYYY-MM-DD` i beskrivelsen (workaround – `start_date` er Premium)
- `due_date` satt via API
- Label: `erp` + kanban-label (`fremtidige`/`ikke starta`/`iarbeid`/`complete`)
- Milepæl: gruppenivå-milepæl

---

## Oppdatere fra ny MPP-fil

Arbeidsflyt ved oppdatert prosjektplan:

1. **Les MPP** og ekstraher oppgaver/milepæler med startdato + ferdigdato
2. **Sammenlign** med eksisterende issues (tittel-matching)
3. **Oppdater** `due_date` og `description` (startdato) på endrede issues
4. **Oppdater** gruppemilepæl-datoer ved endring
5. **Kjør** kanban-labeling (fremtidige vs ikke starta)

```python
# Skjelett – oppdater datoer på eksisterende issues
for iid, new_start, new_due in changes:
    requests.put(f'{GITLAB_URL}/projects/{PROJECT_ID}/issues/{iid}',
        headers=HEADERS,
        json={
            'due_date': new_due,
            'description': f'**Startdato:** {new_start}\n\n{existing_desc}'
        })
```

---

## Automatisering – fremtidige → ikke starta

**Skript:** `~/Library/Mobile Documents/com~apple~CloudDocs/scripts/snippets/laggitlabissues/erp_fremtidige_auto.py`
**Kjøres:** Daglig kl. 07:00 via launchd (`no.sigma2.erp-fremtidige-auto`)
**Terskel:** 7 dager før `due_date`
**Log:** `~/Library/Logs/erp_fremtidige_auto.log`

---

## Planlagte integrasjoner

- [ ] **Teams/SharePoint:** Hente oppdatert MPP fra SharePoint-bibliotek automatisk
- [ ] **Webhook:** Oppdatere GitLab ved endring i prosjektfil
- [ ] **Rapportering:** Ukentlig statusrapport fra GitLab til Teams-kanal

---

## Kjente begrensninger

| Begrensning | Årsak | Workaround |
|---|---|---|
| `start_date` på issues | GitLab CE – Premium-funksjon | Tekst i beskrivelse |
| Slette issues | Krever Admin/Owner | Lukk i stedet |
| Oppdatere gruppemilepæler | Krever gruppe-Maintainer+ | Bruk gruppe-bot-token |

---

*Sist oppdatert: 2026-03-15*
