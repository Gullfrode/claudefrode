# Morning Briefing Skill

**Trigger:** "Morning briefing" eller "Briefing" eller tilsvarende morgenkommando.

**Output:** Strukturert oversikt over dagen – epost, deadlines, møter, fokus.

---

## Instruksjoner til Claude

Når brukeren ber om morning briefing, skal du:

### 1. Header
```
☕ MORNING BRIEFING – [DATO]
Tidssone: GMT+1 (Trondheim)
```

### 2. Innkommende epost (sist 24 timer)
**Fra MCP epost-integrasjon:**
- Hent epost sist 24 timer
- Sorter etter avsender (Calle først, deretter Suzan, deretter ledelse, deretter øvrig)
- Flag handlingsbehov (svar, gjøre noe, delegere) med emne og kort sammendrag
- Hvis tittelen er rød: høy prioritet
- Hvis tittelen er gul: kan vente til senere

**Format:**
```
EPOST (sist 24t)
- [AVSENDER] [EMNE] — [HANDLING: Svar / Gjøre / Delegere]
- [AVSENDER] [EMNE] — [HANDLING]
```

Hvis ingen epost: "Ingen nye e-poster."

### 3. Oppgaver og deadlines
**Fra to kilder – hent parallelt:**

**a) MCP Påminnelser (che-ical-mcp):**
- Oppgaver som forfaller i dag → flag som "I DAG"
- Oppgaver som forfaller denne uken → flag som "DENNE UKA"
- Varsling hvis noe er overdue → "OVERDUE"

**b) GitLab / Ecodream (ecoissues-skill eller direkte API, prosjekt ID 1020):**
- Hent åpne issues assigned til `frgri`
- Inkluder issues med label `ikke starta` og issues uten label (aktive)
- **Utelat** issues med label `fremtidige` – disse er ikke aktuelle ennå (flyttes til `ikke starta` ca. én uke før de er relevante)
- Vis tittel og evt. forfallsdato

Slå sammen til én liste, sorter etter hastegrad. Merk kilde: `[Påminnelser]` / `[GitLab]`.

**Format:**
```
OPPGAVER & DEADLINES
- [OVERDUE][Påminnelser] Oppgavenavn — var [DATO]
- [I DAG][GitLab] Oppgavenavn — #issue-nummer
- [DENNE UKA][Påminnelser] Oppgavenavn — Frist [DATO]
```

Hvis ingen oppgaver: "Ingen oppgaver forfaller i dag."

### 4. Dagens møter
**Fra MCP kalender-integrasjon:**
- Møter bare for i dag
- Vis klokkeslett og deltagende (hvis tilgjengelig)
- Sorter etter tid (tidligst først)

**Format:**
```
DAGENS MØTER
- [TID] [MØTENAVN] med [DELTAKERE] (varighet: [MIN])
```

Hvis ingen møter: "Ingen møter i dag."

### 5. Dagens fokus
**Fra context/current-priorities.md:**
- Max 3 kilder (internkontroll, ERP, bærekraft)
- Én linje per
- Dette er deg sin personlige "nord" for dagen

**Format:**
```
DAGENS FOKUS (top 3)
1. [TEMA] — [EN-LINJE BESKRIVELSE]
2. [TEMA] — [EN-LINJE BESKRIVELSE]
3. [TEMA] — [EN-LINJE BESKRIVELSE]
```

### 6. Signoff
```
---
💡 Tip: Bruk time-blocking for dagens struktur. Anbefalt: Deep Work 08:00–09:30.
```

---

## Tone & Stil

✓ Kortfattet og strukturert
✓ Punkt-lister
✓ Formell, ingen utropstegn
✓ Deutsch når nødvendig (for Sigma2-kontekst)

---

## Eksempel-output

```
☕ MORNING BRIEFING – 11. mars 2026 (tirsdag)
Tidssone: GMT+1 (Trondheim)

EPOST (sist 24t)
- Calle Internkontroll RFI-tilbakemeldinger — SVAR
- Suzan Regnskap AP-bokslutning status — GJØRE
- Ledelse Møtebestilling — MØTE KOMMER

OPPGAVER & DEADLINES
- [I DAG] Gjennomgang internkontroll-prosess — Deadline kl. 15:00
- [DENNE UKA] Submit ERP-kravspesifikasjon — Frist 12. mars

DAGENS MØTER
- 10:30 Internkontroll workshop med Calle + Suzan (60 min)
- 14:00 ERP veivalgs-møte (45 min)

DAGENS FOKUS (top 2)
1. Internkontroll — Gjennomgang prosessdokumentasjon
2. ERP — Analyse av RFI-tilbakemeldinger

---
💡 Tip: Bruk time-blocking for dagens struktur. Anbefalt: Deep Work 08:00–09:30.
```

---

## Tekniske notat

- **MCP-integrasjoner brukt:** Epost (24t), Kalender (dagens møter), Påminnelser (che-ical-mcp), GitLab/Ecodream (prosjekt 1020, assigned til frgri)
- **GitLab-regel:** Label `fremtidige` ekskluderes alltid – disse flyttes til `ikke starta` ca. én uke før de er aktuelle
- **Fallback:** Hvis MCP ikke har data, rapportér "Data ikke tilgjengelig fra [kilde]."
- **Frekvens:** Kjør daglig 08:30 eller ved "morning briefing"-kommando.
- **Cache:** Cach resultater i sesjonen – refresh ved neste reset.