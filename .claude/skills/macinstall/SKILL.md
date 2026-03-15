---
name: macinstall
description: "Mac fresh install guide for frodesolem. Dokumenterer og automatiserer oppsett av ny Mac – SSH-nøkler, Homebrew, apper, shell-konfig, MCP-servere og Claude Code. Trigger når brukeren sier 'sett opp ny mac', 'fresh install', 'macinstall', 'installer mac' o.l."
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# macinstall – Fresh install for frodesolem

Bruker: `frodesolem` | Maskin: MacBook Pro (Apple Silicon)

Denne skill-en guider deg gjennom komplett oppsett av ny Mac etter fresh install. Kjøres i Claude Code etter at Xcode Command Line Tools og Homebrew er installert.

---

## Fase 0 – Forberedelser (manuelt)

1. Logg inn med Apple ID
2. Aktiver iCloud – vent til `~/Library/Mobile Documents/com~apple~CloudDocs/scripts/` er synkronisert
3. Installer Xcode Command Line Tools:
   ```bash
   xcode-select --install
   ```
4. Installer Homebrew:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
5. Legg til brew i PATH (Apple Silicon):
   ```bash
   echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
   eval "$(/opt/homebrew/bin/brew shellenv)"
   ```

---

## Fase 1 – Homebrew pakker

### Formulae
```bash
brew install \
  git node python@3.14 python@3.12 uv pipx \
  pandoc ffmpeg tesseract \
  tree hugo \
  glab \
  coder \
  zeromq
```

> Øvrige formulae (lyd, video-libs, etc.) installeres automatisk som avhengigheter.

### Casks
```bash
brew install --cask \
  alt-tab \
  mactex \
  shortcat \
  swiftbar
```

---

## Fase 2 – SSH-nøkler

Alle nøkler er ED25519. Generer med disse navnene og kommentarene:

```bash
ssh-keygen -t ed25519 -C "macbook"            -f ~/.ssh/id_ed25519
ssh-keygen -t ed25519 -C "github"             -f ~/.ssh/id_github
ssh-keygen -t ed25519 -C "gitlab"             -f ~/.ssh/id_gitlab
ssh-keygen -t ed25519 -C "homeassistant"      -f ~/.ssh/id_homeassistant
ssh-keygen -t ed25519 -C "frodesolem@nuc"     -f ~/.ssh/id_nuc
ssh-keygen -t ed25519 -C "frodesolem@pi"      -f ~/.ssh/id_pi
ssh-keygen -t ed25519 -C "frodesolem@qnap"    -f ~/.ssh/id_qnap
ssh-keygen -t ed25519 -C "udmp"               -f ~/.ssh/id_udmp
ssh-keygen -t ed25519 -C "claude@surface-fedora" -f ~/.ssh/id_fedora
```

> **Merk:** Disse er nye nøkler. Legg til public keys på hver tjeneste:
> - `id_github.pub` → GitHub > Settings > SSH Keys
> - `id_gitlab.pub` → gitlab.sigma2.no > Preferences > SSH Keys
> - `id_homeassistant.pub` → authorized_keys på hai7 og hai3
> - `id_nuc.pub` → authorized_keys på alle Proxmox-noder (pvei7, pvei3, pvei3, pvebeebox, pvegamer, pvedell, pbs)
> - `id_pi.pub` → authorized_keys på octo1, octo2, z2mqtt*
> - `id_qnap.pub` → authorized_keys på flode, flodo, flida (bruker: admin)
> - `id_udmp.pub` → authorized_keys på UDMP

### SSH config
```bash
cat > ~/.ssh/config << 'EOF'
# LAN-snarveier (IP-nøkler)
Host 192
    HostName 10.0.1.192
    User root
    IdentityFile ~/.ssh/id_homeassistant
    IdentitiesOnly yes

Host 197
    HostName 10.0.1.197
    User root
    IdentityFile ~/.ssh/id_homeassistant
    IdentitiesOnly yes

Host 199
    HostName 10.0.1.199
    User root
    IdentityFile ~/.ssh/id_nuc
    IdentitiesOnly yes

Host 200
    HostName 10.0.1.200
    User root
    IdentityFile ~/.ssh/id_nuc
    IdentitiesOnly yes

Host 204
    HostName 10.0.1.204
    User root
    IdentityFile ~/.ssh/id_nuc
    IdentitiesOnly yes

# Git-tjenester
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_github
  IdentitiesOnly yes

Host gitlab.no
  HostName gitlab.sigma2.no
  User git
  IdentityFile ~/.ssh/id_gitlab
  IdentitiesOnly yes

# QNAP NAS (LAN)
Host flode
    HostName 10.0.1.40
    User admin
    IdentityFile ~/.ssh/id_qnap
    IdentitiesOnly yes

Host flodo
    HostName 10.0.1.41
    User admin
    IdentityFile ~/.ssh/id_qnap
    IdentitiesOnly yes

Host flida
    HostName 10.0.1.42
    User admin
    IdentityFile ~/.ssh/id_qnap
    IdentitiesOnly yes

# Tailscale-noder (ingen nøkkel nødvendig for noder med tailscale --ssh)
Host pvei7
  HostName 100.118.152.51
  User root

Host pvei3
  HostName 100.101.102.102
  User root

Host pvebeebox
  HostName 100.116.78.22
  User root

Host pvegamer
  HostName 100.94.219.101
  User root

Host pvedell
  HostName 100.118.168.11
  User root

Host pbs
  HostName 100.77.101.48
  User root

Host hai7
  HostName 100.127.123.118
  User root
  IdentityFile ~/.ssh/id_homeassistant

Host hai3
  HostName 100.109.101.29
  User root
  IdentityFile ~/.ssh/id_homeassistant

Host dockeri7
  HostName 100.114.9.40
  User root

Host dockeri3
  HostName 100.109.212.58
  User root

Host ollama
  HostName 100.97.177.80
  User root

Host n8n
  HostName 100.113.175.30
  User root

Host octo1
  HostName 100.86.45.101
  User root
  IdentityFile ~/.ssh/id_pi

Host octo2
  HostName 100.112.32.83
  User root
  IdentityFile ~/.ssh/id_pi

Host flode
  HostName 100.70.217.57
  User admin
  IdentityFile ~/.ssh/id_qnap

Host flodo
  HostName 100.118.11.29
  User admin
  IdentityFile ~/.ssh/id_qnap

Host flida
  HostName 100.98.254.114
  User admin
  IdentityFile ~/.ssh/id_qnap

Host udmp
  HostName 100.75.137.81
  User root
  IdentityFile ~/.ssh/id_udmp

Host z2mqttgarasje
  HostName 100.125.69.89
  User root
  IdentityFile ~/.ssh/id_pi

Host z2mqttkvisten
  HostName 100.64.205.80
  User root
  IdentityFile ~/.ssh/id_pi

Host grafana
  HostName 100.67.169.33
  User root

Host beszel
  HostName 100.73.48.49
  User root

Host paperless
  HostName 100.81.61.18
  User root
EOF
chmod 600 ~/.ssh/config
```

> Full `~/.ssh/config` med alle Tailscale-noder regenereres automatisk av `ts-sync`-skriptet etter at Tailscale er installert.

---

## Fase 3 – Shell-konfigurasjon

### ~/.zprofile
```bash
cat >> ~/.zprofile << 'EOF'

# Homebrew
eval "$(/opt/homebrew/bin/brew shellenv)"

# Obsidian CLI
export PATH="$PATH:/Applications/Obsidian.app/Contents/MacOS"
EOF
```

### ~/.zshrc
```bash
cat > ~/.zshrc << 'EOF'
# Reset stty control characters (fix for macOS Sequoia regression)
[[ -t 0 ]] && stty intr '^C' eof '^D' susp '^Z' 2>/dev/null

# Google Cloud
export GOOGLE_CLOUD_PROJECT="gemini-frode"

# PATH
export PATH="$HOME/Library/Mobile Documents/com~apple~CloudDocs/scripts:$PATH"
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/bin:$PATH"
export NODE_PATH="/opt/homebrew/lib/node_modules"

# Aliaser
alias tailscale="/Applications/Tailscale.app/Contents/MacOS/Tailscale"
alias astabellbredde='osascript "$HOME/Library/Mobile Documents/com~apple~CloudDocs/scripts/astabellbredde.scpt"'
alias astabellbreddeppt='osascript "$HOME/Library/Mobile Documents/com~apple~CloudDocs/scripts/astabellbreddeppt.scpt"'
alias asmålkort='osascript "$HOME/Library/Mobile Documents/com~apple~CloudDocs/scripts/asmålkort.scpt"'

# VS Code: åpne ~/claude som default
code() {
    if [ $# -eq 0 ]; then
        /usr/local/bin/code "$HOME/claude"
    else
        /usr/local/bin/code "$@"
    fi
}

# LDAP / Entra ID-oppslag
_ldap_pass() {
    local pass
    pass=$(security find-generic-password -s ldap-sikt -a frgri -w 2>/dev/null)
    if [ -z "$pass" ]; then
        echo -n "LDAP Password: " >&2
        read -rs pass
        echo "" >&2
    fi
    echo "$pass"
}

ldap() {
    if [ $# -eq 0 ]; then
        echo "Usage: ldap <username>"
        return 1
    fi
    local pass
    pass=$(_ldap_pass)
    ldapsearch -x -LLL -H ldaps://ldap.sikt.no -b dc=sikt,dc=no -w "$pass" -D uid=frgri,ou=users,dc=sikt,dc=no "(|(uid=*$*)(cn=*$*))"
}

ldapmanager() {
    if [ $# -eq 0 ]; then
        echo "Usage: ldapmanager <username>"
        return 1
    fi
    local manager_uid="$1"
    local pass
    pass=$(_ldap_pass)
    local manager_dn
    manager_dn=$(ldapsearch -x -LLL -H ldaps://ldap.sikt.no -b dc=sikt,dc=no -w "$pass" -D uid=frgri,ou=users,dc=sikt,dc=no "(uid=$manager_uid)" dn | grep "^dn:" | head -1 | sed 's/^dn: //')
    [ -z "$manager_dn" ] && echo "Fant ikke: $manager_uid" && return 1
    ldapsearch -x -LLL -H ldaps://ldap.sikt.no -b dc=sikt,dc=no -w "$pass" -D uid=frgri,ou=users,dc=sikt,dc=no "(manager=$manager_dn)" cn uid mail title
}
EOF
```

> **Scripts i iCloud** (`~/Library/Mobile Documents/com~apple~CloudDocs/scripts/`) er tilgjengelige globalt via PATH uten videre oppsett – synkes automatisk av iCloud.

---

## Fase 4 – ~/bin/ (MCP-binærfiler)

```bash
mkdir -p ~/bin
```

Kopier disse fra iCloud backup eller gammel maskin:
- `~/bin/CheICalMCP` – kalender/påminnelser MCP-server
- `~/bin/mfp-mcp` – MyFitnessPal MCP-server

Sett kjørbare:
```bash
chmod +x ~/bin/CheICalMCP ~/bin/mfp-mcp
```

> Gi **Vibetunnel** tillatelse til Reminders i Systeminnstillinger > Personvern > Påminnelser.

---

## Fase 5 – Claude Code og konfigurasjon

### Installer Claude Code
```bash
npm install -g @anthropic-ai/claude-code
```

### Klon konfig-repo
```bash
git clone git@github.com:Gullfrode/claudefrode.git ~/claude
```

### MCP-konfig (~/.claude.json)
```bash
cat > ~/.claude.json << 'EOF'
{
  "mcpServers": {
    "che-ical-mcp": {
      "type": "stdio",
      "command": "/Users/frodesolem/bin/CheICalMCP",
      "args": [],
      "env": {}
    },
    "mfp-mcp": {
      "type": "stdio",
      "command": "/Users/frodesolem/bin/mfp-mcp",
      "args": [],
      "env": {}
    },
    "miro": {
      "type": "http",
      "url": "https://mcp.miro.com",
      "headers": {
        "Authorization": "Bearer <MIRO_TOKEN>"
      }
    }
  }
}
EOF
```

> Hent Miro-token fra gammel maskin: `cat ~/.claude.json | grep Bearer`

---

## Fase 6 – Apper (manuell installasjon)

Disse installeres manuelt – enten fra App Store, vendor-nettsted eller MDM:

### Fra App Store
- Magnet
- Itsycal
- Shottr
- Notion
- Notion Calendar
- Notion Mail
- 1Password 7
- Bartender 6
- iStat Menus
- Microsoft To Do
- Perplexity
- Health Auto Export
- Color Picker
- Jojo
- Mark And Scribble
- Comet

### Direkte nedlasting / vendor
| App | Kilde |
|-----|-------|
| Microsoft 365 (Word, Excel, PowerPoint, Outlook, Teams, OneNote, OneDrive) | office.com eller Company Portal |
| Slack | slack.com |
| Zoom | zoom.us |
| Discord | discord.com |
| Spotify | spotify.com |
| Telegram | telegram.org |
| Obsidian | obsidian.md |
| Visual Studio Code | code.visualstudio.com |
| GitHub Desktop | desktop.github.com |
| ForkLift | binarynights.com |
| Docker Desktop | docker.com |
| Tailscale | tailscale.com |
| eduVPN | eduvpn.org |
| Citrix Workspace | citrix.com |
| RustDesk | rustdesk.com |
| Jump Desktop | jumpdesktop.com |
| Jump Desktop Connect | jumpdesktop.com |
| Termius | termius.com |
| Claude | claude.ai/download |
| ChatGPT | openai.com |
| VibeTunnel | vibetunnel.app |
| Alfred 5 | alfredapp.com |
| AppCleaner | freemacsoft.net |
| AltTab | alt-tab-macos.netlify.app |
| Ollama | ollama.ai |
| MQTT Explorer | mqtt-explorer.com |
| Home Assistant | home-assistant.io |
| DisplayLink Manager | synaptics.com |
| FreeCAD | freecad.org |
| Miro | miro.com |
| SwiftBar | swiftbar.app |
| Shortcat | shortcatapp.com |
| Wispr Flow | wispr.ai |
| Grab2Text | grab2text.app |
| A Better Finder Rename 12 | publicspace.net |
| Paperparrot | paperparrot.app |
| Nebula for Mac | nebula.tv |
| Live Home 3D | belight.net |
| UltiMaker Cura | ultimaker.com |
| Company Portal / Self Service | IT/MDM |
| Microsoft Defender | IT/MDM |
| CodeMeter / WIBUKEY | wibu.com |

---

## Fase 7 – SwiftBar plugins

Plugins ligger i `~/swiftbar-plugins/`. Opprett mappen og legg inn disse tre:

```bash
mkdir -p ~/swiftbar-plugins
```

### eduvpn.1m.sh
Viser oransje/grå prikk i menylinjen avhengig av om eduVPN er tilkoblet.

```bash
cat > ~/swiftbar-plugins/eduvpn.1m.sh << 'EOF'
#!/bin/bash
# <xbar.title>EduVPN Status</xbar.title>
# <xbar.desc>Viser oransje prikk om EduVPN er tilkoblet, grå om ikke.</xbar.desc>

STATUS=$(scutil --nc list 2>/dev/null | grep 'org.eduvpn.app' | grep -o '(Connected)\|(Disconnected)')

if [[ "$STATUS" == "(Connected)" ]]; then
    echo "● | color=#FF8C00 bash=open param1=-a param2=eduVPN terminal=false"
else
    echo "● | color=#888888 bash=open param1=-a param2=eduVPN terminal=false"
fi
EOF
chmod +x ~/swiftbar-plugins/eduvpn.1m.sh
```

### mail.1m.sh
Viser antall uleste epost fra M365 Jobb-kontoen i Apple Mail.

```bash
cat > ~/swiftbar-plugins/mail.1m.sh << 'EOF'
#!/bin/bash
# <xbar.title>Unread Mail</xbar.title>
# <xbar.desc>Viser antall uleste epost fra alle kontoer i Apple Mail</xbar.desc>
# <xbar.dependencies>bash,osascript</xbar.dependencies>

UNREAD=$(osascript <<'APPLESCRIPT'
tell application "Mail"
    set unreadCount to 0
    repeat with anAccount in accounts
        if name of anAccount is "M365 Jobb" then
            try
                set unreadCount to unreadCount + (unread count of inbox of anAccount)
            end try
        end if
    end repeat
    return unreadCount
end tell
APPLESCRIPT
)

if [[ "$UNREAD" -gt 0 ]]; then
    echo "$UNREAD | sfimage=envelope.fill bash=open param1=-a param2=Mail terminal=false"
else
    echo " | sfimage=envelope bash=open param1=-a param2=Mail terminal=false"
fi
EOF
chmod +x ~/swiftbar-plugins/mail.1m.sh
```

### wan-status.5m.sh
Viser grønn/rosa prikk basert på om fiber-WAN (eth9) på UDMP er oppe. Kun synlig på hjemmenettverket (10.0.1.x).

```bash
cat > ~/swiftbar-plugins/wan-status.5m.sh << 'EOF'
#!/bin/bash
# <xbar.title>WAN Status</xbar.title>
# <xbar.desc>Viser aktiv WAN med farget nettverksikon. Kun synlig på Ma maison-nettet.</xbar.desc>

LOCAL_IP=$(ifconfig | grep 'inet 10\.0\.1\.' | awk '{print $2}')
if [[ -z "$LOCAL_IP" ]]; then
    exit 0
fi

CARRIER=$(ssh -o ConnectTimeout=3 -o BatchMode=yes udmp \
    "cat /sys/class/net/eth9/carrier 2>/dev/null" 2>/dev/null)

if [[ "$CARRIER" == "1" ]]; then
    echo "● | color=#00C853 href=https://udmp.dingo-smoot.ts.net"
else
    echo "● | color=#FF6B9D href=https://udmp.dingo-smoot.ts.net"
fi
EOF
chmod +x ~/swiftbar-plugins/wan-status.5m.sh
```

### Pek SwiftBar til plugin-mappen
Åpne SwiftBar > Preferences > Plugin Directory og velg `~/swiftbar-plugins/`.

---

## Fase 8 – Tailscale og ts-sync

1. Installer Tailscale (se over)
2. Logg inn: `tailscale login`
3. Kjør ts-sync for å regenerere `~/.ssh/config` med alle Tailscale-noder:
   ```bash
   ~/Library/Mobile\ Documents/com~apple~CloudDocs/scripts/ts-sync
   ```

---

## Fase 9 – Verifisering

```bash
# Claude Code fungerer
claude --version

# SSH til GitHub
ssh -T git@github.com

# SSH til GitLab
ssh -T git@gitlab.sigma2.no

# Homebrew ok
brew doctor

# iCloud-scripts tilgjengelig globalt
which pandocpdf
which ts-sync
```

---

## Notater

- **LDAP-passord** lagres i Keychain: `security add-generic-password -s ldap-sikt -a frgri -w`
- **homelab.env** (`~/.claude/homelab.env`) kopieres fra gammel maskin – inneholder HA_TOKEN, TAILSCALE_API_KEY m.m.
- **Obsidian-vault** synkroniseres via iCloud automatisk
- **Agresso-web script** ligger i skills-mappen via `~/claude` repo – trenger `eduVPN` og Python 3.14
