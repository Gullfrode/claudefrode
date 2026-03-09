# Calendar Sync Skill

**Trigger:**
- "sync kalender"
- "legg blokker i kalenderen"
- "planlegg i jobbkalendar"
- "skriv timeplan til kalender"
- eller via en MCP‑melding som sier "time block to calendar" eller lignende.

**Formål:**
Ta en time‑blocking‑plan (generert av time-blocking-assistant) og opprette eller oppdatere tilsvarende hendelser i brukers innebygde kalenderapp via MCP-integrasjoner. Sørge for at ledige intervaller fylles med blokker, og at eksisterende relevante møter beholdes.

## Beskrivelse

Når skillen aktiveres, gjør du følgende:

1. **Hent eller generer plan:**
   - Hvis kommandoen ble trigget direkte, be time-blocking-assistant om å generere dagens plan.
   - Alternativt, bruk en tidligere cached plan fra sesjonsminnet (f.eks. generert i løpet av morgenen).

2. **Filtrer plan:**
   - Fjern eventuelle private/"Lunsj"-blokker dersom brukeren ønsker det (spør ved behov).
   - Ikke overskriv eksisterende kalenderelementer som ikke ble opprettet av skillen tidligere (bruk en spesiell tag eller beskrivelse som merker blokker du opprettet).

3. **Generer AppleScript for kalender:**
   - Opprett en AppleScript-fil (.scpt) med kommandoer for å legge til/oppdatere hendelser i "Kalender".
   - Bruk følgende struktur for hver blokk:
     ```
     tell application "Calendar"
         tell calendar "Kalender"
             make new event with properties {summary:"Deep Work: Gjennomgang internkontroll-dokumentasjon", start date:date "mandag 9. mars 2026 08:00", end date:date "mandag 9. mars 2026 09:00", description:"Time-block generert av Claude-assistent"}
         end tell
     end tell
     ```
   - Lagre filen som `sync-calendar-[dato].scpt` i workspace-roten.
   - Instruer brukeren å kjøre scriptet manuelt: `osascript sync-calendar-[dato].scpt`.
   - Hvis en blokk allerede finnes, oppdater den (sjekk på tittel og dato).
   - Notat: Brukeren synkroniserer "Kalender" annenhver time med gullfrode@gmail.com-gcalen og frgri@nris.no – ikke rapporter duplikater fra disse.

4. **Bekreftelse:**
   - Gi brukeren en kortliste over hendelser som ble lagt til/oppdatert.
   - Hvis handling mislykkes (manglende tillatelse, nettverksfeil), informer brukeren og foreslå manuell løsning.

5. **Deaktivere når ferdig:**
   - Legg resultatet i sesjonsminnet slik at morning-briefing eller time-blocking kan referere til det senere.

## Eksempel-dialog
```
Bruker: "Sync kalender"
Assistent: "Genererer plan og oppdaterer kalender..."
Assistent: "Legg til 6 arrangementer i jobbkalendar; ferdig."
```

## Notater
- Bruker MCP-integrasjoner mot innebygde apper (Mail, Calendar, Reminders på macOS).
- Mål: minimal støy etter første kjøring, ved senere kjøringer oppdaterer eksisterende blokker i stedet for å lage duplikater.
- Hvis en blokk kolliderer med en eksisterende uten tag, spør brukeren om duplikat eller overskriv.
- Fremtidig forbedring: gi brukeren mulighet til å sette egne tidspreferanser (f.eks. tannlegetime) som ekskluderes.

---

Dette kjøres i Claude CLI/Desktop med MCP-tilgang til kalenderapp.