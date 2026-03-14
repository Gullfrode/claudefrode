# agresso-login – Automatisk innlogging i Agresso via Citrix

**Trigger:** Når brukeren vil logge inn i Agresso / starte Agresso / åpne UBW / koble til Citrix.

---

## Script

```
/Users/frodesolem/claude/.claude/skills/agresso-login/agresso_login.py
```

**Python:** `/opt/homebrew/opt/python@3.14/bin/python3.14`
**Avhengigheter:** `requests` (allerede installert i brew Python)

---

## Kjør innlogging

```bash
python3 /Users/frodesolem/claude/.claude/skills/agresso-login/agresso_login.py
```

---

## Første gangs oppsett (bare én gang)

```bash
python3 /Users/frodesolem/claude/.claude/skills/agresso-login/agresso_login.py --setup
```

Lagrer disse i macOS Keychain under service `agresso-citrix`:
- `username` – Citrix/AD-brukernavn
- `domain` – AD-domene (f.eks. `sigma2`, blank hvis ikke brukt)
- `password` – Citrix StoreFront-passord
- `citrix_password` – Passord inne i Citrix Workspace (blank = samme som over)

Sjekk/slett lagrede credentials:
```bash
# Se hva som er lagret
security find-generic-password -s agresso-citrix -a username

# Slett og start på nytt
security delete-generic-password -s agresso-citrix -a username
security delete-generic-password -s agresso-citrix -a password
security delete-generic-password -s agresso-citrix -a domain
security delete-generic-password -s agresso-citrix -a citrix_password
```

---

## Hva scriptet gjør

1. **VPN-sjekk** – sjekker om eduVPN (UUID `903A7F6B...`) er tilkoblet
   - Hvis ikke: prøver `scutil --nc start` → poller i 60 sek
   - Fallback: åpner eduVPN-appen og ber deg koble til manuelt
2. **Citrix StoreFront API** – logger inn på `ctxext.public.cloudservices.no`
   - Henter CSRF-token, kaller `ExplicitAuth/LoginAttempt`
   - Henter ressursliste, finner Agresso automatisk
3. **ICA-fil** – henter og åpner `.ica`-filen → Citrix Workspace starter
4. **Passord i Citrix** – fyller inn via AppleScript GUI-scripting (System Events)

---

## Kjente begrensninger / feilsøking

| Problem | Tiltak |
|---|---|
| Login feilet (HTTP 401/403) | Sjekk credentials med `--setup` på nytt |
| Ingen ressurser funnet | Sjekk at VPN er oppe, prøv å gå manuelt til URL-en |
| ICA-filen åpner ikke | Sjekk at Citrix Workspace er installert (`/Applications/Citrix Workspace.app`) |
| Citrix passord-dialog ikke funnet | Fyll inn manuelt, script timer ut og gir beskjed |
| Domain-felt: prøv blank | Noen Citrix-oppsett bruker kun brukernavn uten domene |

Manuell URL: `https://ctxext.public.cloudservices.no/Citrix/StoreWeb/`

---

## eduVPN UUID

```
903A7F6B-D4E8-4FC9-9B66-877F97302273
```

Sjekk status: `scutil --nc status 903A7F6B-D4E8-4FC9-9B66-877F97302273`

---

## Tone & Stil

Kortfattet statusmeldinger under kjøring, flagg feil tydelig.
