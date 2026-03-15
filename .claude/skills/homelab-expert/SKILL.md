---
name: homelab-expert
description: Homelab-ekspert for dingo-smoot.ts.net. Trigger når brukeren spør om homelaben, servere, tjenester, Proxmox, Home Assistant, Docker, Tailscale, nettverk, printer, NAS, overvåking, eller sier "hjelp meg med homelaben", "noe er nede", "fikse", "restart", "sjekk status" e.l. i privat kontekst. IKKE trigger for Sigma2/jobb-oppgaver.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Homelab-ekspert – dingo-smoot.ts.net

Du er homelab-ekspert for Frode Solem sitt privat hjemmelab. Hjelp med feilsøking, vedlikehold, konfigurasjon og overvåking av alle tjenester.

## Miljøvariabler

Les hemmeligheter fra `~/.claude/homelab.env`:

```bash
source ~/.claude/homelab.env
# Gir tilgang til: HA_TOKEN, HA_URL, HA_URL_TS, TAILSCALE_API_KEY
```

---

## Nettverksoversikt

- **Tailnet:** `dingo-smoot.ts.net`
- **LAN:** `10.0.1.0/24`
- **Gateway:** `10.0.1.1` (UniFi Dream Machine Pro)

### Fysiske maskiner

| Vert | LAN IP | Tailscale IP | Rolle |
|------|--------|--------------|-------|
| UDMP | 10.0.1.1 | 100.75.137.81 | Ruter/gateway (UniFi Dream Machine Pro) |
| pvei7 | 10.0.1.205 | 100.118.152.51 | Proxmox VE hypervisor (i7) |
| pvei3 | 10.0.1.199 | 100.101.102.102 | Proxmox VE hypervisor (i3) – NIC-problemer, brukes Shelly-støpsel |
| pvebeebox | 10.0.1.200 | 100.116.78.22 | Proxmox VE hypervisor (Beebox) |
| pvegamer | 10.0.1.191 | 100.94.219.101 | Proxmox VE hypervisor (Gamer) |
| pvedell | 10.0.1.194 | 100.118.168.11 | Proxmox VE hypervisor (Dell) – Coral TPU |
| pbs | 10.0.1.204 | 100.77.101.48 | Proxmox Backup Server |
| flode | 10.0.1.40 | 100.70.217.57 | QNAP NAS |
| flodo | 10.0.1.41 | 100.118.11.29 | QNAP NAS |
| flida | 10.0.1.42 | 100.98.254.114 | QNAP NAS |

### VMs og Docker-hosts

| Vert | LAN IP | Tailscale IP | Hypervisor |
|------|--------|--------------|------------|
| dockeri7 | 10.0.1.210 | 100.114.9.40 | pvei7 |
| dockeri3 | 10.0.1.29 | 100.109.212.58 | pvei3 |
| dockerbeebox | – | 100.89.62.18 | pvebeebox |
| hai7 | 10.0.1.192 | 100.127.123.118 | pvei7 – Home Assistant primær |
| hai3 | 10.0.1.197 | 100.109.101.29 | pvei3 – Home Assistant sekundær |
| ollama | – | 100.97.177.80 | pvei7 – Ollama + Whisper + Piper |

### Raspberry Pi

| Vert | LAN IP | Tailscale IP | Rolle |
|------|--------|--------------|-------|
| octo1 | 10.0.1.149 | 100.86.45.101 | OctoPrint – Ender 3 V2 #1 |
| octo2 | – | 100.112.32.83 | OctoPrint – Ender 3 V2 #2 |
| z2mqttgarasje | – | 100.125.69.89 | Zigbee/Z-Wave – garasje |
| z2mqttkvisten | – | 100.64.205.80 | Zigbee/Z-Wave – kvisten |

---

## SSH-nøkler

| Nøkkel | Brukes til |
|--------|-----------|
| `~/.ssh/id_homeassistant` | hai7 (`root@10.0.1.192`), hai3 (`root@10.0.1.197`) |
| `~/.ssh/id_nuc` | Proxmox: pvei7, pvei3, pvebeebox, pvegamer, pvedell, pbs (alle root) |
| `~/.ssh/id_pi` | Raspberry Pi: octo1, z2mqttgarasje, z2mqttkvisten (root) |
| `~/.ssh/id_qnap` | QNAP NAS: flode, flodo, flida (admin, ikke root) |

**Snarveier i `~/.ssh/config`:**
- `ssh 192` → hai7 (id_homeassistant)
- `ssh 197` → hai3 (id_homeassistant)

**Tailscale SSH (ingen nøkkel nødvendig):**
- `ssh root@pvei7` / `ssh root@pvei7.dingo-smoot.ts.net`
- `ssh root@dockeri7` osv. (noder med `tailscale up --ssh`)

---

## Tjenesteoversikt

| Tjeneste | Host | URL |
|----------|------|-----|
| Home Assistant | hai7 | https://hai7.dingo-smoot.ts.net |
| Home Assistant | hai3 | https://hai3.dingo-smoot.ts.net |
| Grafana | dockeri7 | https://grafana.dingo-smoot.ts.net |
| Prometheus | dockeri7 | https://prometheus.dingo-smoot.ts.net |
| Beszel | dockeri7 | https://beszel.dingo-smoot.ts.net |
| Paperless | dockeri7 | https://paperless.dingo-smoot.ts.net |
| Paperless AI | dockeri7 | https://paperlessai.dingo-smoot.ts.net |
| Mealie | dockeri7 | https://mealie.dingo-smoot.ts.net |
| Frigate | dockeri7 | https://frigate.dingo-smoot.ts.net |
| Coder | dockeri7 | https://coder.dingo-smoot.ts.net |
| deCONZ | dockeri7 | https://deconz.dingo-smoot.ts.net |
| n8n | dockeri3 | https://n8n.dingo-smoot.ts.net |
| AdGuard Home | dockeri3 | https://adguardi3.dingo-smoot.ts.net |
| Ollama / Open WebUI | ollama VM | https://ollama.dingo-smoot.ts.net |
| Whisper STT | ollama VM | whisper.dingo-smoot.ts.net:10300 |
| Piper TTS | ollama VM | whisper.dingo-smoot.ts.net:10200 |
| OctoPrint 1 | octo1 | https://octo1.dingo-smoot.ts.net |
| OctoPrint 2 | octo2 | https://octo2.dingo-smoot.ts.net |
| UDMP | udmp | https://udmp.dingo-smoot.ts.net |
| Portainer | z2mqttgarasje | https://z2mqttgarasje.dingo-smoot.ts.net |
| Portainer | z2mqttkvisten | https://z2mqttkvisten.dingo-smoot.ts.net |
| Zigbee2MQTT garasje | z2mqttgarasje | https://zigbee2mqttgarasje.dingo-smoot.ts.net |
| Zigbee2MQTT kvisten | z2mqttkvisten | https://zigbee2mqttkvist.dingo-smoot.ts.net |
| Z-Wave garasje | z2mqttgarasje | https://zwavejs2mqttgarasje.dingo-smoot.ts.net |
| Z-Wave kvisten | z2mqttkvisten | https://zwavejs2mqttkvist.dingo-smoot.ts.net |

---

## Home Assistant API

```bash
source ~/.claude/homelab.env

# GET state
curl -s -H "Authorization: Bearer $HA_TOKEN" \
  "$HA_URL/api/states/switch.plug_nuci3"

# POST service call
curl -s -X POST -H "Authorization: Bearer $HA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "switch.plug_nuci3"}' \
  "$HA_URL/api/services/switch/turn_off"
```

**Nyttige entities:**
- `switch.plug_nuci3` – Shelly støpsel pvei3/nuci3 (av/på)
- `sensor.plug_nuci3_power` – effekt i W
- `sensor.plug_nuci3_energy` – energiforbruk kWh

**Shelly direkte API (10.0.2.160):**
```bash
# Slå av pvei3
curl -s -X POST http://10.0.2.160/rpc/Switch.Set \
  -H "Content-Type: application/json" \
  -d '{"id":0,"on":false}'
# Vent 5 sek, slå på igjen
sleep 5
curl -s -X POST http://10.0.2.160/rpc/Switch.Set \
  -H "Content-Type: application/json" \
  -d '{"id":0,"on":true}'
```

---

## Vanlige feilsituasjoner og løsninger

### pvei3 NIC-krasj (e1000e)
1. Sjekk SSH til pvei3: `ssh -i ~/.ssh/id_nuc root@10.0.1.199`
2. Hvis ingen svar: strømsykl via Shelly (se HA API over)
3. Berørte tjenester ved krasj: pvei3, dockeri3, n8n, adguardi3, adguardhome-sync, hai3, openclaw

### Tailscale-ruting LAN-problem
Symptom: SSH til LAN-IP feiler selv om Tailscale er oppe.
Løsning på berørt node:
```bash
ip rule add to 10.0.1.0/24 lookup main priority 5260
```
Persistent: legg til i `/etc/network/interfaces`:
```
post-up ip rule add to 10.0.1.0/24 lookup main priority 5260
pre-down ip rule del to 10.0.1.0/24 lookup main priority 5260 2>/dev/null || true
```

### Docker-container offline (Tailscale sidecar)
Sjekk `cap_add: NET_ADMIN, NET_RAW` og `/dev/net/tun` i compose.

### QNAP NAS Tailscale nede etter reboot
Start manuelt (flode/flida bruker userspace-networking – se startup-scripts på hver NAS).

### pvei3 bonding (TODO – Nordic USB-C/A RTL8153 mottatt)
```bash
# Finn USB-adapter interface-navn
ip link show | grep enx
# Opprett bond0 med eno1 + enx... i active-backup
```

---

## Monitorering

- **Tailscale status:** `tailscale status`
- **Beszel:** https://beszel.dingo-smoot.ts.net
- **Grafana:** https://grafana.dingo-smoot.ts.net
- **Prometheus:** https://prometheus.dingo-smoot.ts.net

---

## Instruksjoner til Claude

1. **Sjekk alltid Tailscale-tilkobling** for berørt node før du forsøker SSH
2. **Bruk riktig SSH-nøkkel** basert på nøkkel-tabellen over
3. **Source .env** ved alle HA API-kall
4. **Logg hva du gjør** – forklar hvert steg kortfattet
5. **Ikke gjett** – si ifra hvis du mangler info (IP, passord, token)
6. Foreslå alltid **persistent løsning** etter midlertidig fix
7. Tailscale SSH fungerer uten nøkkel for noder med `tailscale up --ssh`
