---
name: pbidesktop
description: Power BI Desktop – Power Query M-skript og datamodell mot GitLab, med scheduled refresh via Power BI Pro. Trigger når brukeren vil koble Power BI mot GitLab, lage rapport fra issues/milepæler, eller sier "pbi", "powerbi", "power query", "lag rapport" o.l.
allowed-tools: Bash, Read, Write
---

# Power BI Desktop – GitLab-integrasjon

Kobler Power BI Desktop mot GitLab REST API for rapportering på issues, milepæler og Kanban-status.

---

## Starte Power BI Desktop

Power BI er installert via Microsoft Store. Åpnes slik:

```bash
start "" "shell:AppsFolder\Microsoft.MicrosoftPowerBIDesktop_8wekyb3d8bbwe!Microsoft.MicrosoftPowerBIDesktop"
```

---

## Konfigurasjon

```
GITLAB_URL   = https://gitlab.sigma2.no/api/v4
PROJECT_ID   = 1035   (ecodream/erpsystem)
GROUP        = ecodream
TOKEN        = settes som credential i Power BI Service (ikke hardkodes)
```

---

## Power Query M – Issues (ERPsystem)

```powerquery
let
    BaseUrl = "https://gitlab.sigma2.no/api/v4/projects/1035/issues",
    Token   = "GITLAB_TOKEN_HER",  // Byttes ut med credential i Service

    HentSide = (side as number) =>
        let
            Svar = Json.Document(Web.Contents(BaseUrl, [
                Headers = [#"Private-Token" = Token],
                Query   = [per_page = "100", page = Number.ToText(side), state = "all"]
            ]))
        in Svar,

    // Hent alle sider (pagination)
    Side1    = HentSide(1),
    Side2    = HentSide(2),
    AlleSider = Side1 & Side2,   // Utvid ved behov

    Tabell = Table.FromList(AlleSider, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    Utvidet = Table.ExpandRecordColumn(Tabell, "Column1",
        {"iid", "title", "state", "due_date", "created_at", "updated_at",
         "closed_at", "labels", "milestone", "description"},
        {"ID", "Tittel", "Status", "Ferdigdato", "Opprettet", "Oppdatert",
         "Lukket", "Labels", "Milepæl", "Beskrivelse"}),

    // Milepæl-tittel
    MedMilepæl = Table.AddColumn(Utvidet, "Milepæl_tittel", each
        if [Milepæl] = null then null
        else Record.Field([Milepæl], "title")),

    // Startdato fra beskrivelse (**Startdato:** YYYY-MM-DD)
    MedStart = Table.AddColumn(MedMilepæl, "Startdato", each
        let
            m = Text.AfterDelimiter([Beskrivelse] ?? "", "**Startdato:** ")
        in if m = "" then null else Text.Start(m, 10)),

    // Kanban-kolonne (første label som er kanban)
    KanbanLabels = {"fremtidige", "ikke starta", "iarbeid", "complete"},
    MedKanban = Table.AddColumn(MedStart, "Kanban", each
        let
            lbls = [Labels],
            treff = List.Select(lbls, each List.Contains(KanbanLabels, _))
        in if List.Count(treff) > 0 then treff{0} else null),

    // Datokonvertering
    MedDatoer = Table.TransformColumnTypes(MedKanban, {
        {"Ferdigdato", type date},
        {"Startdato",  type date},
        {"Opprettet",  type datetimezone},
        {"Oppdatert",  type datetimezone}
    })

in MedDatoer
```

---

## Power Query M – Gruppemilepæler

```powerquery
let
    Url    = "https://gitlab.sigma2.no/api/v4/groups/ecodream/milestones",
    Token  = "GITLAB_TOKEN_HER",

    Svar   = Json.Document(Web.Contents(Url, [
        Headers = [#"Private-Token" = Token],
        Query   = [per_page = "50"]
    ])),

    Tabell  = Table.FromList(Svar, Splitter.SplitByNothing()),
    Utvidet = Table.ExpandRecordColumn(Tabell, "Column1",
        {"id", "iid", "title", "state", "start_date", "due_date"},
        {"ID", "IID", "Tittel", "Status", "Startdato", "Ferdigdato"}),

    // Filtrer kun ERP-milepæler (M6–M16)
    ERPFilter = Table.SelectRows(Utvidet, each
        Text.StartsWith([Tittel], "M6") or Text.StartsWith([Tittel], "M7") or
        Text.StartsWith([Tittel], "M8") or Text.StartsWith([Tittel], "M9") or
        Text.StartsWith([Tittel], "M10") or Text.StartsWith([Tittel], "M11") or
        Text.StartsWith([Tittel], "M12") or Text.StartsWith([Tittel], "M13") or
        Text.StartsWith([Tittel], "M14") or Text.StartsWith([Tittel], "M15") or
        Text.StartsWith([Tittel], "M16")),

    MedDatoer = Table.TransformColumnTypes(ERPFilter, {
        {"Startdato",  type date},
        {"Ferdigdato", type date}
    })

in MedDatoer
```

---

## Publisering og scheduled refresh

1. **Power BI Desktop:** Fil → Publiser → velg workspace
2. **Power BI Service:** Datasett → Innstillinger → Datakildelegitimasjon
   - Type: **Web**
   - URL: `https://gitlab.sigma2.no`
   - Autentisering: **Anonym** med header `Private-Token: <token>`
   - *(Alternativt: Basic med token som passord)*
3. **Planlagt oppdatering:** Opptil 8×/dag med Pro-lisens
4. **Ingen gateway** nødvendig – GitLab er skybasert

---

## Anbefalte visninger

- **Gantt-lignende:** Startdato + Ferdigdato per issue, gruppert på milepæl
- **Kanban-status:** Stablede stolper – fremtidige / ikke starta / iarbeid / complete
- **Milepæl-tidslinje:** Milepæler som punkter på tidslinje med status
- **Overdue-flagg:** `Ferdigdato < I dag AND Status = "opened"`

---

## GPU-bytte på pvegamer

**pvegamer** (`root@pvegamer.dingo-smoot.ts.net`) kjører enten W11 eller Ollama med GPU-passthrough – ikke begge samtidig. GPU konfigureres i Proxmox og krever reboot av hypervisoren.

**VM:** `w11gamer` (VMID 215, 30 GB RAM)

### Skript (iCloud: `~/Library/Mobile Documents/com~apple~CloudDocs/scripts/`)

| Skript | Funksjon | Proxmox-skript på server |
|---|---|---|
| `gpuw11` | GPU → W11, rebootes Proxmox, starter w11gamer | `/usr/local/bin/gpu_to_windows.sh` |
| `gpuollama` | GPU → host (Ollama), rebootes Proxmox | `/usr/local/bin/gpu_to_host.sh` |

### Bruk fra terminal

```bash
# Start Windows 11 med GPU
~/Library/Mobile\ Documents/com~apple~CloudDocs/scripts/gpuw11

# Bytt tilbake til Ollama
~/Library/Mobile\ Documents/com~apple~CloudDocs/scripts/gpuollama
```

### Hva skriptene gjør
1. SSH inn på `root@pvegamer.dingo-smoot.ts.net`
2. Kjører server-side skript som rekonfigurerer VM-config (`hostpci`-parametere)
3. Rebootes Proxmox – GPU er tilgjengelig i riktig VM etter oppstart

**NB:** Proxmox må rebootees – tar 1–2 min før W11/Ollama er tilgjengelig.

### Tilkobling til W11
Koble til via **RustDesk** etter at VM er oppe:
```bash
open "rustdesk://100.82.11.47"
```

---

## Fremtidige integrasjoner

- [ ] SharePoint-bibliotek som datakilde (MPP-filer)
- [ ] Teams-webhook for refresh-varsler
- [ ] Koble Ollama-modeller mot PBI via Python-script i Power Query

---

*Sist oppdatert: 2026-03-15*
