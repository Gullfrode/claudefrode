---
name: miro
description: Miro REST API – jobbe med Miro-boards via REST API. Trigger når brukeren vil åpne Miro, jobbe med Miro-boards, lage sticky notes, shapes, connectors, eller sier "åpne Miro", "vis Miro-board", "lag i Miro" o.l.
---

# Miro Skill

Miro-integrasjonen bruker REST API direkte (ikke MCP). Token hentes fra `~/.claude/miro_token.json`.

## Sjekk token

```bash
python3 ~/claude/.claude/skills/miro/miro_api.py boards
```

Hvis tokenet er utløpt (401), kjør OAuth-flyten på nytt:

```bash
python3 ~/claude/.claude/skills/miro/oauth.py
```

## Bruk

All kommunikasjon med Miro skjer via `miro_api.py`:

```bash
# List boards
python3 ~/claude/.claude/skills/miro/miro_api.py boards

# Hent items på et board
python3 ~/claude/.claude/skills/miro/miro_api.py items <board_id>

# Opprett sticky note
python3 ~/claude/.claude/skills/miro/miro_api.py sticky <board_id> "Tekst her" [farge]

# Generelt API-kall (GET)
python3 ~/claude/.claude/skills/miro/miro_api.py get /v2/boards

# Generelt API-kall (POST med JSON-body)
python3 ~/claude/.claude/skills/miro/miro_api.py post /v2/boards/<id>/sticky_notes '{"data":{"content":"test"}}'
```

## Farger for sticky notes
`yellow`, `red`, `blue`, `green`, `orange`, `pink`, `violet`, `gray`, `dark_blue`, `dark_green`, `dark_red`
