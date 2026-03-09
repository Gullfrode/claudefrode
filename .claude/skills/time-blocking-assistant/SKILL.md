# Time-Blocking Assistant Skill

**Trigger:** "time blocking", "timeblock", "plan dagen", "lag timeplan", "timeblokk" eller lignende.

**Mål:** Hjelpe Frode med å strukturere arbeidsdagen ved å sette opp konkrete tidsblokker for prioriterte aktiviteter basert på dagens agenda og fokusområder.

## Instruksjoner for Claude

Når brukeren ber om timeblocking:

1. **Samle informasjon:**
   - Se på dagens møter fra MCP-kalender.
   - Sjekk dagens oppgaver/forfall fra MCP-task.
   - Hent dagens fokusområder fra `context/current-priorities.md` (max 2 nå).

2. **Foreslå blokker:**
   - Predefinerte blokker:
     - Deep Work (90 min)
     - Administrative (60 min)
     - Delegering & Oppfølging (30–45 min)
   - Plasser dem rundt møtene:
     - Morgen: Deep Work rett etter morgenbriefing (08:00–09:30)
     - Før/etter møter: Administrative eller Delegering basert på kontekst
   - Inkluder pauser (minst 15 min hver 2.5 time).
   - Sørg for at alle "I DAG"-oppgaver er dekket i en administrativ blokk.

3. **Format:**
```
TIME-BLOCKING FOR [DATO]

08:00–09:30  Deep Work: [fokusområde 1]
09:30–10:00  Pause / E-post
10:00–11:00  Administrative: [oppgave eller møtenavn]
11:00–12:30  Deep Work: [fokusområde 2]
12:30–13:00  Lunsj
13:00–14:00  Møte: [møtenavn] (organiser som en blokk)
14:00–15:00  Administrative: [forfallsoppgaver]
15:00–15:15  Pause
15:15–16:00  Delegering & Oppfølging: [hvem og hva]
16:00–16:30  Dag-oppsummering / Plan neste dag
```

4. **Tips & påminnelser:**
   - Flag eventuelle overlappende møter og foreslå omprioritering.
   - Advar om lange kontinuerlige blokker (>2 t) uten pause.
   - Oppfordre til å bruke "Morning briefing" først.

5. **Skriftlig dagbok:**
   - Tilby å generere en mal for loggføring av hva som faktisk ble utført (oppfølging senere).

6. **Tone & stil:**
   - Kortfattet oppsett, punktlister.
   - Norsk, formell intern tone.
   - Unngå utropstegn; bruk tørr humor ved behov.

---

## Eksempel-resultat
```
TIME-BLOCKING FOR 13. mars 2026

08:00–09:30  Deep Work: Gjennomgang internkontroll
09:30–10:00  Pause / Svar e-post (Calle)
10:00–11:00  Administrative: Ferdig kravspesifikasjon ERP
11:00–12:30  Deep Work: Analyse RFI-prioritering
12:30–13:00  Lunsj
13:00–14:00  Møte: ERP-status med ledelse
14:00–15:00  Administrative: Signering av dokumenter
15:00–15:15  Pause
15:15–16:00  Delegering: Oppfølging Calle (RFI)
16:00–16:30  Dag-oppsummering & forberedelse neste dag
```

---

## Tekniske notat

- Må kunne hente data fra MCP-integrasjoner (kalender, tasks).
- Bruker samme dato-format som morning-briefing.
- Lagrer anbefalt plan i sesjonsminnet for referanse senere.