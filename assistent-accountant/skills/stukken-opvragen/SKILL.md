---
name: stukken-opvragen
description: >
  Gebruik deze skill wanneer een accountant wil weten welke stukken er nog
  missen, een e-mail wil sturen om documenten op te vragen, wil controleren
  welke documenten al ontvangen zijn, of vraagt om "welke stukken missen er",
  "stuur een e-mail voor de ontbrekende stukken", "wat moet ik nog opvragen"
  of "klant heeft nog niet aangeleverd" voor een specifieke klant.
  Werkt met Exact Online. E-mail versturen vereist e-mail MCP verbinding.
---

# Stukken Opvragen

Je identificeert welke documenten ontbreken voor een specifieke opdracht (BTW, jaarrekening of fiscaal) en stelt een e-mail op om deze bij de klant op te vragen.

## Aanpak

**Stap 1 — Bepaal type en klant**

Vraag als niet opgegeven:
- Welke klant?
- Type opdracht: BTW / jaarrekening / fiscaal?
- Welk jaar/kwartaal?

**Stap 2 — Check wat er al is**

Exact Online — controleer documenten in het dossier:
```sql
SELECT FileName, Category, Created, Modified
FROM Documents.Documents
WHERE Account = guid'{klantID}'
AND Created >= datetime('{startperiode}')
ORDER BY Created DESC
```

Haal ook contactgegevens op:
```sql
SELECT Name, Email, Phone
FROM CRM.Contacts
WHERE Account = guid'{klantID}'
AND IsMainContact = true
```

**Stap 3 — Vergelijk met checklist**

Gebruik de checklists uit `references/document-checklists.md`.

Snel overzicht van wat er **altijd** nodig is:

**Voor BTW-aangifte:**
- Bankafschriften (of CAMT.053 of directe koppeling)
- Verkoopfacturen kwartaal (als niet al in systeem)
- Inkoopfacturen kwartaal (als niet al in systeem)

**Voor jaarrekening:**
- Jaaropgave bank(en) per 31-12
- WOZ-beschikking bedrijfspand (indien eigen pand)
- Inventarislijst per 31-12 (indien voorraad)
- Leningsoverzicht per 31-12 (indien leningen)
- Pensioenopgave per 31-12 (indien pensioenregeling)
- Salarisstrook december + loonheffingsaangifte december

**Voor fiscaal:**
- Investeringslijst boekjaar (nieuw en desinvesteringen)
- DGA-salaris jaaropgave
- Privé-gebruik auto (indien auto in BV)

**Stap 4 — Presenteer ontbrekende stukken**

```
ONTBREKENDE STUKKEN — [Klantnaam] — [Opdracht] [Periode]

Gevonden in dossier:
✅ Bankafschriften Q1 2026 (ontvangen 5 april)
✅ Verkoopfacturen Q1 (al in systeem)

Ontbreekt nog:
□ Bankafschrift ING per 31-12-2025
□ WOZ-beschikking bedrijfspand
□ Inventarislijst per 31-12-2025

Wil je dat ik een e-mail opstel om deze stukken op te vragen?
```

**Stap 5 — E-mail opstellen** (🟡 ORANJE)

```
Onderwerp: Jaarrekening [jaar] — nog benodigde stukken

Beste [Aanspreking] [Achternaam],

Wij zijn gestart met de werkzaamheden voor uw jaarrekening [jaar].
Om deze af te kunnen ronden, ontvangen wij graag nog de volgende stukken:

1. Bankafschrift ING per 31-12-[jaar]
   → Downloaden via uw internetbankieren onder "Afschriften"

2. WOZ-beschikking bedrijfspand [adres]
   → U ontvangt deze van de gemeente

3. Inventarislijst per 31-12-[jaar]
   → Een overzicht van uw voorraad per jaareinde

Kunt u deze stukken voor [datum + 2 weken] aanleveren?

Met vriendelijke groet,
[Naam kantoor]
```

Toon de e-mail en vraag: "Wil je deze e-mail versturen?"

**Stap 6 — Versturen** (🔴 ROOD)

Als e-mail MCP beschikbaar is: verstuur via e-mail connector.
Als niet beschikbaar: kopieer het concept zodat de accountant het zelf kan versturen.

## Goedkeuringsmodel

- 🟢 **GROEN** — Checklist controleren, ontbrekende stukken identificeren (automatisch)
- 🟡 **ORANJE** — E-mail concept opstellen en tonen
- 🔴 **ROOD** — E-mail definitief versturen

## Referenties

Voor volledige documentchecklists per opdrachttype:
> Lees `references/document-checklists.md`
