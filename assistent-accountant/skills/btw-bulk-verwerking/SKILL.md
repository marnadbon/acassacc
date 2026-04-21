---
name: btw-bulk-verwerking
description: >
  Gebruik deze skill wanneer een accountant de BTW-aangifte voor meerdere
  klanten tegelijk wil voorbereiden, een bulk BTW-run wil draaien voor een
  kwartaal, een overzicht wil van alle BTW-statusen, of vraagt om "BTW voor
  alle klanten", "bulk BTW aangifte", "BTW kwartaal overzicht" of
  "welke BTW-aangiftes zijn al klaar". Werkt met Exact Online.
---

# BTW Bulk Verwerking

Je verwerkt de BTW-aangifte voor alle klant-administraties in één run en geeft een dashboard met de status per klant.

## Aanpak

**Stap 1 — Haal alle administraties op**

Exact Online:
```sql
SELECT DivisionCode, Description, CountryCode, Status
FROM System.Divisions
WHERE Status = 1  -- alleen actieve administraties
```

**Stap 2 — Controleer welke BTW-aangiftes al klaar zijn**

Per divisie:
```sql
SELECT Year, Period, Status, Created
FROM VAT.VATReturns
WHERE Year = {jaar}
ORDER BY Period DESC
LIMIT 1
```

Status codes Exact Online VATReturns:
- 0 = concept
- 10 = ter review
- 20 = goedgekeurd
- 30 = ingediend

**Stap 3 — Verwerk per administratie**

Loop over alle actieve divisies. Gebruik de btw-aangifte-voorbereiden logica per klant.

> Let op rate limits: 60 calls/minuut per company. Bij 200+ klanten: verwerk in batches van 50, wacht 60 seconden tussen batches. Informeer de accountant over de verwachte doorlooptijd.

**Stap 4 — Dashboard**

```
BTW BULK — [Q1/Q2/Q3/Q4] [Jaar]
Verwerkt: 47 van 52 administraties

STATUS OVERZICHT:
✅ Al ingediend (23):     Bakkerij Jansen, De Groene Tuin, ...
🔄 Klaar voor review (15): Kapsalon Bella, ...
⚠️ Actie vereist (6):     [reden per klant]
❌ Fout (3):              [foutmelding]

TOTAAL TE BETALEN: € 284.500 (schatting alle klanten)

Wil je de "klaar voor review" aangiftes één voor één doornemen?
```

**Stap 5 — Vervolgactie**

Na het dashboard:
- Bied aan om de aangiftes die klaar zijn één voor één te reviewen
- Markeer goedgekeurde aangiftes (🟡 ORANJE: markeren als "goedgekeurd")
- Indienen: altijd per klant afzonderlijk met expliciete goedkeuring (🔴 ROOD)

## Goedkeuringsmodel

- 🟢 **GROEN** — Dashboard genereren, status ophalen (automatisch)
- 🟡 **ORANJE** — Aangifte als "klaar voor review" markeren
- 🔴 **ROOD** — Indienen — ALTIJD per klant afzonderlijk, nooit bulk-indienen

## Beperking

BTW bulk werkt het beste met Exact Online (via System/Divisions om alle administraties op te halen). Voor Moneybird en AFAS: verwerk administraties één voor één of laat de accountant de klantlijst aanleveren.
