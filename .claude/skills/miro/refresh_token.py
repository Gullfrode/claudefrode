#!/usr/bin/env python3
"""Refresher Miro access token og oppdaterer Claude Code MCP-config."""

import json, os, urllib.request, urllib.parse, sys

TOKEN_FILE = os.path.expanduser("~/.claude/miro_token.json")
CONFIG_FILE = os.path.expanduser("~/.claude.json")
CACHE_FILE = os.path.expanduser("~/.claude/mcp-needs-auth-cache.json")

def refresh():
    if not os.path.exists(TOKEN_FILE):
        print("FEIL: Ingen token-fil funnet. Kjør OAuth-flyten på nytt.")
        sys.exit(1)

    token_data = json.load(open(TOKEN_FILE))
    refresh_token = token_data.get("refresh_token")
    client_id = token_data.get("client_id")
    client_secret = token_data.get("client_secret")

    if not refresh_token:
        print("FEIL: Ingen refresh_token i token-filen.")
        sys.exit(1)

    data = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode()

    req = urllib.request.Request("https://mcp.miro.com/token", data=data)
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req) as r:
            resp = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"FEIL ved token-refresh: {e.code} {e.read().decode()}")
        sys.exit(1)

    resp.setdefault("client_id", client_id)
    resp.setdefault("client_secret", client_secret)
    json.dump(resp, open(TOKEN_FILE, "w"), indent=2)

    c = json.load(open(CONFIG_FILE))
    c["mcpServers"]["miro"] = {
        "type": "http",
        "url": "https://mcp.miro.com",
        "headers": {"Authorization": f"Bearer {resp['access_token']}"},
    }
    json.dump(c, open(CONFIG_FILE, "w"), indent=2)

    if os.path.exists(CACHE_FILE):
        d = json.load(open(CACHE_FILE))
        d.pop("miro", None)
        json.dump(d, open(CACHE_FILE, "w"), indent=2)

    print(f"Token refreshet OK. Utloper om {resp.get('expires_in', '?')} sekunder.")

if __name__ == "__main__":
    refresh()
