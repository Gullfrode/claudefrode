#!/usr/bin/env python3
"""
Agresso Login Automation
AppleScript + Chrome → Citrix StoreFront → ICA-fil → Citrix Workspace
"""

import subprocess
import sys
import time
import os

STORE_URL   = "https://ctxext.public.cloudservices.no/Citrix/StoreWeb/"
EDUVPN_UUID = "903A7F6B-D4E8-4FC9-9B66-877F97302273"
SERVICE     = "agresso-citrix"
APP_NAME    = "UBW M7"

# ── Credentials ───────────────────────────────────────────────────────────────

def get_credential(key):
    r = subprocess.run(
        ["security", "find-generic-password", "-s", SERVICE, "-a", key, "-w"],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print(f"[!] Credential '{key}' ikke funnet. Kjør: python3 agresso_login.py --setup")
        sys.exit(1)
    return r.stdout.strip()

def save_credential(key, value):
    subprocess.run(
        ["security", "add-generic-password", "-s", SERVICE, "-a", key, "-w", value, "-U"],
        check=True
    )

def setup():
    print("=== Agresso Login – Første gangs oppsett ===\n")
    import getpass
    username     = input("Brukernavn (AD/Citrix): ").strip()
    domain       = input("Domene (f.eks. sigma2, blank hvis ikke brukt): ").strip()
    password     = getpass.getpass("Passord (Citrix StoreFront): ")
    citrix_pw    = getpass.getpass("Passord inne i Citrix/Agresso (blank = samme): ")
    save_credential("username",        username)
    save_credential("domain",          domain)
    save_credential("password",        password)
    save_credential("citrix_password", citrix_pw or password)
    print("\n[OK] Lagret i macOS Keychain under 'agresso-citrix'.")

# ── VPN ───────────────────────────────────────────────────────────────────────

def vpn_status():
    r = subprocess.run(
        ["scutil", "--nc", "status", EDUVPN_UUID],
        capture_output=True, text=True
    )
    return r.stdout.strip().split("\n")[0]

def ensure_vpn():
    status = vpn_status()
    if status == "Connected":
        print("[OK] eduVPN tilkoblet.")
        return
    print(f"[..] eduVPN ikke tilkoblet ({status}). Prøver å koble til...")
    subprocess.run(["scutil", "--nc", "start", EDUVPN_UUID], capture_output=True)
    for i in range(30):
        time.sleep(2)
        if vpn_status() == "Connected":
            print("[OK] eduVPN tilkoblet.")
            return
        print(f"     Venter på VPN... ({(i+1)*2}s)")
    print("[..] Auto-tilkobling feilet. Åpner eduVPN-appen – koble til manuelt.")
    subprocess.run(["open", "-a", "eduVPN"])
    for i in range(60):
        time.sleep(2)
        if vpn_status() == "Connected":
            print("[OK] eduVPN tilkoblet.")
            return
        if i % 5 == 4:
            print(f"     Venter på manuell VPN-tilkobling... ({(i+1)*2}s)")
    print("[!] VPN ikke tilkoblet etter 120 sek. Avbryter.")
    sys.exit(1)

# ── AppleScript-hjelper ───────────────────────────────────────────────────────

def run_applescript(script, timeout=30):
    r = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=timeout
    )
    return r.stdout.strip(), r.stderr.strip()

def chrome_js(js):
    """Kjør JavaScript i aktiv Chrome-fane."""
    script = f'''
    tell application "Google Chrome"
        execute active tab of front window javascript "{js}"
    end tell
    '''
    return run_applescript(script)

# ── Nettleserautomatisering ───────────────────────────────────────────────────

def open_citrix_page():
    print(f"[..] Åpner Citrix StoreFront i Chrome...")
    script = f'''
    tell application "Google Chrome"
        activate
        if (count of windows) = 0 then
            make new window
        end if
        set theTab to make new tab at end of tabs of front window
        set URL of theTab to "{STORE_URL}"
        set active tab index of front window to index of theTab
    end tell
    '''
    run_applescript(script)
    time.sleep(5)

def wait_for_page_load(expected_text, timeout=20):
    """Venter til siden inneholder forventet tekst."""
    for _ in range(timeout):
        out, _ = chrome_js(f"document.title + ' | ' + document.body.innerText.substring(0, 200)")
        if expected_text.lower() in out.lower():
            return True
        time.sleep(1)
    return False

def already_logged_in(timeout=5):
    """Sjekker om vi allerede er på appslisten (aktiv sesjon)."""
    for _ in range(timeout):
        out, _ = chrome_js("document.querySelectorAll('p.storeapp-name').length.toString()")
        try:
            if int(out.strip()) > 0:
                return True
        except ValueError:
            pass
        time.sleep(1)
    return False

def fill_login_form(username, password, domain):
    print("[..] Fyller inn innloggingsskjema...")
    time.sleep(2)

    # Prøv ulike felt-IDer (Citrix StoreFront varierer)
    login_js = f"""
    (function() {{
        var u = document.getElementById('username') ||
                document.querySelector('input[name=username]') ||
                document.querySelector('input[type=text]');
        var p = document.getElementById('password') ||
                document.querySelector('input[name=password]') ||
                document.querySelector('input[type=password]');
        var d = document.getElementById('domain') ||
                document.querySelector('input[name=domain]') ||
                document.querySelector('select[name=domain]');
        if (u) {{ u.value = '{username}'; u.dispatchEvent(new Event('input', {{bubbles:true}})); }}
        if (p) {{ p.value = '{password}'; p.dispatchEvent(new Event('input', {{bubbles:true}})); }}
        if (d && '{domain}') {{ d.value = '{domain}'; }}
        var btn = document.getElementById('loginBtn') ||
                  document.querySelector('input[type=submit]') ||
                  document.querySelector('button[type=submit]') ||
                  document.querySelector('.loginBtn');
        if (btn) {{ btn.click(); return 'klikket'; }}
        return 'btn ikke funnet';
    }})()
    """
    out, err = chrome_js(login_js.replace('\n', ' ').replace('"', '\\"'))
    print(f"     Login-status: {out or err}")
    time.sleep(2)
    # Trykk Enter for å sende skjemaet (ingen synlig submit-knapp)
    run_applescript('''
    tell application "Google Chrome" to activate
    delay 0.3
    tell application "System Events"
        tell process "Google Chrome"
            key code 36
        end tell
    end tell
    delay 0.5
    tell application "Google Chrome"
        set miniaturized of front window to true
    end tell
    ''')
    time.sleep(2)

def find_and_click_agresso():
    print(f"[..] Leter etter '{APP_NAME}' i ressurslisten...")
    find_js = f"""
    (function() {{
        var items = Array.from(document.querySelectorAll('p.storeapp-name'));
        var el = items.find(function(e) {{ return e.innerText && e.innerText.trim() === '{APP_NAME}'; }});
        if (el) {{
            el.parentElement.click();
            return 'klikket: ' + el.innerText.trim();
        }}
        return 'ikke funnet. Tilgjengelig: ' + items.map(function(e) {{ return e.innerText.trim(); }}).join(' | ');
    }})()
    """
    out, err = chrome_js(find_js.replace('\n', ' '))
    print(f"     {out or err}")
    if "klikket" not in (out or ""):
        return False
    # Klikk "Open"-dialogen som dukker opp
    time.sleep(1)
    print("[..] Klikker Open-dialog...")
    run_applescript('''
    tell application "Google Chrome"
        set miniaturized of front window to false
        activate
    end tell
    delay 0.5
    ''')
    open_js = "var btn = Array.from(document.querySelectorAll('a, button, input')).find(function(e){ return (e.innerText||e.value||'').toLowerCase().match(/open|launch/); }); if (btn) { btn.click(); 'klikket: ' + (btn.innerText||btn.value); } else { 'ingen open-knapp'; }"
    out2, _ = chrome_js(open_js)
    print(f"     {out2}")
    # Minimer Chrome igjen etter at ICA-nedlastingen er trigget
    run_applescript('''
    delay 1
    tell application "Google Chrome"
        set miniaturized of front window to true
    end tell
    ''')
    return True

def send_esc_to_citrix(count=30):
    """Sender ESC-taster til Citrix Viewer for å hoppe over intro-faner."""
    print(f"[..] Sender {count}x Esc til Citrix Viewer...")
    run_applescript(f'''
    tell application "Citrix Viewer" to activate
    delay 2
    tell application "System Events"
        tell process "Citrix Viewer"
            repeat {count} times
                key code 53
                delay 0.5
            end repeat
        end tell
    end tell
    ''', timeout=120)
    print("[OK] Esc-sekvens sendt.")

# ── Citrix passord ────────────────────────────────────────────────────────────

def fill_citrix_password(citrix_password):
    print("[..] Venter paa Citrix passord-dialog...")
    script = f"""
    tell application "System Events"
        set citrixProcs to {{"Citrix Workspace Launcher", "Citrix Workspace", "Citrix Viewer"}}
        repeat 60 times
            delay 1
            set frontApp to name of first application process whose frontmost is true
            if frontApp is in citrixProcs then
                delay 0.5
                keystroke "{citrix_password}"
                delay 0.3
                key code 36
                return "OK"
            end if
        end repeat
        return "timeout"
    end tell
    """
    out, _ = run_applescript(script, timeout=90)
    if out == "OK":
        print("[OK] Citrix-passord fylt inn automatisk.")
    else:
        print("[!] Automatisk passord-utfylling feilet - fyll inn manuelt.")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if "--setup" in sys.argv:
        setup()
        return

    username        = get_credential("username")
    password        = get_credential("password")
    domain          = get_credential("domain")
    citrix_password = get_credential("citrix_password")

    ensure_vpn()
    open_citrix_page()

    if already_logged_in():
        print("[OK] Aktiv sesjon – hopper over innlogging.")
    else:
        print("[..] Venter på innloggingssiden...")
        if not wait_for_page_load("log", timeout=15):
            print("[!] Innloggingssiden lastet ikke. Sjekk VPN og URL.")
            sys.exit(1)
        fill_login_form(username, password, domain)
        print("[..] Venter på ressurssiden...")
        time.sleep(3)

    clicked = find_and_click_agresso()
    if not clicked:
        print("[!] Klikket ikke automatisk. Klikk på UBW M7 manuelt og trykk Open-dialogen.")
        sys.exit(1)

    # Vent på Citrix Viewer og fyll inn passord
    fill_citrix_password(citrix_password)

    # Send 30x Esc (0.5 sek mellomrom) for å hoppe over intro-faner
    send_esc_to_citrix(30)

    print("\n[OK] Ferdig. Agresso er åpent.")

if __name__ == "__main__":
    main()
