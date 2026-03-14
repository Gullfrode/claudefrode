#!/usr/bin/env python3
"""Miro REST API helper. Bruk: python3 miro_api.py <kommando> [args]"""

import json, os, sys, urllib.request, urllib.error

TOKEN_FILE = os.path.expanduser("~/.claude/miro_token.json")
BASE = "https://api.miro.com"


def token():
    if not os.path.exists(TOKEN_FILE):
        print("FEIL: Ingen token-fil. Kjør oauth.py på nytt.")
        sys.exit(1)
    return json.load(open(TOKEN_FILE))["access_token"]


def req(method, path, body=None):
    url = BASE + path if path.startswith("/") else path
    data = json.dumps(body).encode() if body else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Authorization", f"Bearer {token()}")
    r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"FEIL {e.code}: {e.read().decode()}")
        sys.exit(1)


def boards():
    data = req("GET", "/v2/boards?limit=50")
    for b in data.get("data", []):
        print(f"{b['id']}\t{b['name']}")


def items(board_id):
    data = req("GET", f"/v2/boards/{board_id}/items?limit=50")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def sticky(board_id, content, color="yellow"):
    body = {
        "data": {"content": content, "shape": "square"},
        "style": {"fillColor": color},
    }
    result = req("POST", f"/v2/boards/{board_id}/sticky_notes", body)
    print(f"Opprettet sticky: {result.get('id')}")


def get(path):
    print(json.dumps(req("GET", path), indent=2, ensure_ascii=False))


def post(path, body_str):
    body = json.loads(body_str)
    print(json.dumps(req("POST", path, body), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Bruk: miro_api.py boards | items <id> | sticky <id> <tekst> [farge] | get <path> | post <path> <json>")
        sys.exit(0)
    cmd = args[0]
    if cmd == "boards":
        boards()
    elif cmd == "items" and len(args) >= 2:
        items(args[1])
    elif cmd == "sticky" and len(args) >= 3:
        sticky(args[1], args[2], args[3] if len(args) > 3 else "yellow")
    elif cmd == "get" and len(args) >= 2:
        get(args[1])
    elif cmd == "post" and len(args) >= 3:
        post(args[1], args[2])
    else:
        print(f"Ukjent kommando: {cmd}")
        sys.exit(1)
