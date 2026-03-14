#!/usr/bin/env python3
"""
Agresso Web Login Automation
Logger inn i Unit4 ERP via HTTP POST og overfører session til Safari.
"""

import subprocess
import sys
import time
import urllib.request
import urllib.parse
import http.cookiejar
import re

URL      = "https://agresso.public.cloudservices.no/Uninettweb/"
SERVICE  = "agresso-citrix"
USERNAME = "frodegs"
COMPANY  = "25"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

# ── Credentials ───────────────────────────────────────────────────────────────

def get_password():
    r = subprocess.run(
        ["security", "find-generic-password", "-s", SERVICE, "-a", "citrix_password", "-w"],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print("[!] Passord ikke funnet i keychain.")
        print("    Legg inn med: security add-generic-password -s agresso-citrix -a citrix_password -w")
        sys.exit(1)
    return r.stdout.strip()

# ── HTTP-innlogging ────────────────────────────────────────────────────────────

def http_login(password):
    """Logg inn via HTTP POST og returner session-cookies."""
    login_url = URL + "Login/Login.aspx?ReturnUrl=%2fUninettweb%2f"

    jar    = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    # Hent login-siden for VIEWSTATE + cookies
    req  = urllib.request.Request(login_url, headers=HEADERS)
    resp = opener.open(req)
    html = resp.read().decode("utf-8", errors="replace")

    def find(pattern):
        m = re.search(pattern, html)
        return m.group(1) if m else ""

    viewstate   = find(r'id="__VIEWSTATE"\s+value="([^"]*)"')
    vsgenerator = find(r'id="__VIEWSTATEGENERATOR"\s+value="([^"]*)"')
    eventval    = find(r'id="__EVENTVALIDATION"\s+value="([^"]*)"')

    # POST skjema
    data = urllib.parse.urlencode({
        "__VIEWSTATE":          viewstate,
        "__VIEWSTATEGENERATOR": vsgenerator,
        "__EVENTVALIDATION":    eventval,
        "ctl10$name":           USERNAME,
        "ctl10$client":         COMPANY,
        "ctl10$password":       password,
        "ctl10$next":           "Logg inn",
    }).encode("utf-8")

    post_req = urllib.request.Request(
        resp.url, data=data,
        headers={**HEADERS,
                 "Content-Type": "application/x-www-form-urlencoded",
                 "Referer": resp.url}
    )
    post_resp = opener.open(post_req)

    if "login" in post_resp.url.lower():
        print("[!] Innlogging feilet. Sjekk brukernavn/passord.")
        sys.exit(1)

    return {c.name: c.value for c in jar}

# ── AppleScript-hjelper ───────────────────────────────────────────────────────

def run_applescript(script):
    r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    return r.stdout.strip(), r.stderr.strip()

APP_BUNDLE = "Meny startskjerm - Unit4 ERP"

def safari_js(js):
    """Kjør JavaScript i Safari (krever 'Tillat JavaScript fra Apple Events')."""
    js_escaped = js.replace("\\", "\\\\").replace('"', '\\"')
    out, err = run_applescript(f'tell application "Safari" to do JavaScript "{js_escaped}" in front document')
    return out, err

# ── Safari-session-overføring (bakgrunn) ──────────────────────────────────────

def inject_cookies_background(cookies):
    """Åpner Safari-fane i bakgrunn, setter cookies, lukker fanen, åpner webapp."""
    login_url = URL + "Login/Login.aspx"
    domain    = "agresso.public.cloudservices.no"

    # Åpne Safari-fane uten å aktivere den
    run_applescript(f'''
    tell application "Safari"
        if (count of windows) = 0 then
            make new document with properties {{URL:"{login_url}"}}
        else
            tell front window
                set newTab to make new tab with properties {{URL:"{login_url}"}}
                set current tab to newTab
            end tell
        end if
    end tell
    ''')
    time.sleep(3)

    # Bygg cookie-JS
    cookie_js = ""
    for name, value in cookies.items():
        cookie_js += f"document.cookie='{name}={value}; path=/; domain={domain}'; "

    out, err = safari_js(cookie_js)
    if err and "not authorized" in err.lower():
        print("[!] Safari JS ikke autorisert.")
        print("    Safari > Innstillinger > Utvikler > Tillat JavaScript fra Apple Events")
        sys.exit(1)

    time.sleep(1)

    # Naviger fanen til autentisert side (ikke lukk den)
    out, err = safari_js(f"window.location.href='{URL}';")
    time.sleep(1)
    run_applescript('tell application "Safari" to activate')

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    password = get_password()

    print("[..] Logger inn via HTTP...")
    cookies = http_login(password)
    print(f"[..] Innlogget. Injiserer session ({len(cookies)} cookies) og åpner i Safari...")

    inject_cookies_background(cookies)
    time.sleep(3)

    title, _ = run_applescript('tell application "Safari" to get name of front document')
    if "logg inn" in title.lower() or "login" in title.lower():
        print(f"[!] Fremdeles på innloggingssiden: {title}")
        sys.exit(1)

    print(f"[OK] Innlogget. Side: {title}")

if __name__ == "__main__":
    main()
