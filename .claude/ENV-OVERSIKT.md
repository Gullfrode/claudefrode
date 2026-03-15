# .env-filer – oversikt

*Sist oppdatert: 2026-03-15*

---

## Sentral skill-.env

**Fil:** `~/claude/.claude/.env`
**Git:** Ignorert (`.gitignore`)
**Synk:** Manuell kopiering til ny Mac

Inneholder alle tokens for skills:

| Nøkkel | Tjeneste |
|---|---|
| `GITLAB_PRIVATE_TOKEN` + `GITLAB_URL` + `PROJECT_ID` | GitLab ecodream (prosjekt-bot) |
| `GITLAB_HOST` + `GITLAB_PROJECT_ID` + `GITLAB_PROJECT_PATH` + `GITLAB_TOKEN` | GitLab ERP-prosjekt |
| `NOTION_TOKEN` + `NOTION_WEBHOOK` + `NOTION_ROOT_PAGE_ID` + `NOTION_ROOT_URL` | Notion |
| `MIRO_CLIENT_ID` + `MIRO_CLIENT_SECRET` | Miro |
| `RT_TOKEN` + `RT_URL` | RT / sak.sikt.no |

Skills som peker hit:
- `skills/notionjobb/.env` → kopi/symlink
- `skills/miro/.env` → kopi/symlink

---

## iCloud-filer (synkroniseres automatisk)

**Mappe:** `~/Library/Mobile Documents/com~apple~CloudDocs/scripts/snippets/`

| Fil | Innhold |
|---|---|
| `laggitlabissues/.env` | `GITLAB_PRIVATE_TOKEN` + `GITLAB_URL` – gruppe-bot for ERP-prosjekt |
| `gitlab/.env` | `GITLAB_HOST` + `GITLAB_PROJECT_ID` + `GITLAB_PROJECT_PATH` + `GITLAB_TOKEN` |
| `RT/.env` | `TOKEN` – RT / sak.sikt.no |

---

## Lokale filer (ikke iCloud, ikke git)

| Fil | Innhold | Manuell kopiering |
|---|---|---|
| `~/.claude/homelab.env` | `HA_TOKEN`, `HA_URL`, `HA_URL_TS`, `TAILSCALE_API_KEY`, `TAILSCALE_TAILNET` | Ja |
| `~/.config/beszel/beszel-agent.env` | `KEY`, `LISTEN` – Beszel monitoring agent | Ja |

---

## Ny Mac – sjekkliste

- [ ] Kopier `~/claude/.claude/.env` (sentral)
- [ ] Kopier `~/.claude/homelab.env`
- [ ] Kopier `~/.config/beszel/beszel-agent.env` (hvis Beszel brukes)
- [ ] iCloud-filer synkroniseres automatisk
- [ ] Kjør `launchctl load ~/Library/LaunchAgents/no.sigma2.erp-fremtidige-auto.plist`
- [ ] Installer avhengigheter: `pip install mpxj python-dotenv requests`
