# Calendar Sync Skill

**Trigger:**
- "sync kalender"
- "legg blokker i kalenderen"
- "planlegg i jobbkalendar"
- "skriv timeplan til kalender"
- eller via en MCP‑melding som sier "time block to calendar" eller lignende.

**Formål:**
Ta en time‑blocking‑plan (generert av time-blocking-assistant) og eksportere den som en ICS-fil for import til kalender. Sørge for at ledige intervaller fylles med blokker, og at eksisterende relevante møter beholdes.

## Beskrivelse

Når skillen aktiveres, gjør du følgende:

1. **Hent eller generer plan:**
   - Hvis kommandoen ble trigget direkte, be time-blocking-assistant om å generere dagens plan.
   - Alternativt, bruk en tidligere cached plan fra sesjonsminnet (f.eks. generert i løpet av morgenen).

2. **Filtrer plan:**
   - Fjern eventuelle private/"Lunsj"-blokker dersom brukeren ønsker det (spør ved behov).
   - Ikke inkluder eksisterende kalenderelementer som ikke ble opprettet av skillen tidligere.

3. **Generer ICS-fil:**
   - Opprett en ICS-fil (iCalendar-format) med hver blokk som et VEVENT.
   - Bruk følgende struktur for hver blokk:
     ```
     BEGIN:VEVENT
     UID:timeblock-[uuid]
     DTSTART:20260315T080000
     DTEND:20260315T093000
     SUMMARY:Deep Work: Gjennomgang internkontroll-dokumentasjon
     DESCRIPTION:Time-block generert av Claude-assistent
     END:VEVENT
     ```
   - Lagre filen som `time-blocks-[dato].ics` i workspace-roten eller en spesifisert mappe.
   - Inkluder alle blokker i én fil for enkel import.

4. **Bekreftelse:**
   - Gi brukeren en kortliste over hendelser som ble lagt til i ICS-filen.
   - Instruer hvordan importere: "Importer time-blocks-[dato].ics til Outlook/Google Calendar etc."
   - Hvis handling mislykkes, informer brukeren.

5. **Deaktivere når ferdig:**
   - Legg resultatet i sesjonsminnet slik at morning-briefing eller time-blocking kan referere til det senere.

## Eksempel-dialog
```
Bruker: "Sync kalender"
Assistent: "Genererer plan og eksporterer til ICS..."
Assistent: "Opprettet time-blocks-2026-03-15.ics med 6 arrangementer. Importer til kalenderen din."
```

## Notater
- Ingen nettverkskall nødvendig; filen lagres lokalt.
- Mål: enkel import uten å åpne ekstra apper.
- Fremtidig forbedring: gi brukeren mulighet til å sette egne tidspreferanser (f.eks. tannlegetime) som ekskluderes.

---

Dette er en høy-nivå beskrivelse; implementeringen bruker standard ICS-format for kompatibilitet.