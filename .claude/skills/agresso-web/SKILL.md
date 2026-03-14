---
name: agresso-web
description: Logg inn i Agresso/Unit4 ERP via Safari Web App (ikke Citrix). Bruk når brukeren vil åpne eller logge inn i Agresso-webappen direkte, eller sier "åpne Agresso web", "logg inn i Unit4 web" e.l.
allowed-tools: Bash
---

# Agresso Web Login

Automatisk innlogging i Unit4 ERP via Safari Web App.

## Forutsetninger

- Safari Web App "Meny startskjerm - Unit4 ERP" er installert
- Passord lagret i macOS Keychain under service `agresso-citrix`, account `citrix_password`
- eduVPN er ikke nødvendig (web-URL er offentlig tilgjengelig)

## Kjøring

```bash
/opt/homebrew/opt/python@3.14/bin/python3.14 /Users/frodesolem/claude/.claude/skills/agresso-web/agresso_web_login.py
```

## Hva scriptet gjør

1. Åpner Safari Web App via `open -a "Meny startskjerm - Unit4 ERP"`
2. Sjekker om bruker allerede er innlogget (tittelsjekk)
3. Venter på at innloggingssiden lastes
4. Fyller inn firma (`25`), brukernavn (`frodegs`) og passord via JavaScript
5. Klikker submit-knappen (eller trykker Enter som fallback)

## Feilsøking

| Problem | Tiltak |
|---|---|
| Credential ikke funnet | Kjør `python3 agresso_login.py --setup` (Citrix-scriptet for oppsett) |
| Innloggingssiden lastet ikke | Sjekk at Web App er installert og URL er tilgjengelig |
| Submit-knapp ikke funnet | Scriptet prøver Enter som fallback automatisk |
| Allerede innlogget | Scriptet avslutter uten feil |

## Forskjell fra agresso-login

- **agresso-login** – Bruker Citrix-klienten (krever eduVPN)
- **agresso-web** – Bruker Safari Web App direkte (ingen VPN nødvendig)
