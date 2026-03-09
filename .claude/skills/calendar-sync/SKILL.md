# Calendar Sync Skill

**Trigger:**
- "sync kalender"
- "legg blokker i kalenderen"
- "planlegg i jobbkalendar"
- "skriv timeplan til kalender"
- eller via en MCP‑melding som sier "time block to calendar" eller lignende.

**Formål:**
Ta en time‑blocking‑plan (generert av time-blocking-assistant) og opprette eller oppdatere tilsvarende hendelser i brukers MCP-kalender. Sørge for at ledige intervaller fylles med blokker, og at eksisterende relevante møter beholdes.

## Beskrivelse

Når skillen aktiveres, gjør du følgende:

1. **Hent eller generer plan:**
   - Hvis kommandoen ble trigget direkte, be time-blocking-assistant om å generere dagens plan.
   - Alternativt, bruk en tidligere cached plan fra sesjonsminnet (f.eks. generert i løpet av morgenen).

2. **Filtrer plan:**
   - Fjern eventuelle private/"Lunsj"-blokker dersom brukeren ønsker det (spør ved behov).
   - Ikke overskriv eksisterende kalenderelementer som ikke ble opprettet av skillen tidligere (bruk en spesiell tag eller beskrivelse som merker blokker du opprettet).

3. **Opprett/oppdater hendelser:**
   - For hver blokk i planen, send en MCP-kommando til å opprette/oppdatere et kalenderarrangement med:
     - Tittel, start- og sluttid, eventuell beskrivelse/etikett.
   - Bruk MCP-kommandosyntaks tilgjengelig via Claude Desktop/CLI. Eksempel (pseudokode):
     ```
     mcp.calendar.create {
       "title": "Deep Work: internkontroll",
       "start": "2026-03-15T08:00",
       "end": "2026-03-15T09:30",
       "tags": ["timeblock"]
     }
     ```
   - Hvis en blokk allerede finnes (sjekk på tag og starttid), oppdater den i stedet for å opprette en duplikat.

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
- Krever at Claude Desktop/CLI har MCP-aksess til jobbkalendar.
- Mål: minimal støy etter første kjøring, ved senere kjøringer oppdaterer eksisterende blokker i stedet for å lage duplikater.
- Hvis en blokk kolliderer med en eksisterende uten tag, spør brukeren om duplikat eller overskriv.
- Fremtidig forbedring: gi brukeren mulighet til å sette egne tidspreferanser (f.eks. tannlegetime) som ekskluderes.

---

Dette er en høy-nivå beskrivelse; implementeringen av MCP-kommandoer avhenger av tilgjengelig API i desktop/CLI.