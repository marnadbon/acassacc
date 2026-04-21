---
name: concept-jaarrekening
description: >
  Gebruik deze skill wanneer een accountant een concept jaarrekening wil
  opstellen, de balans en winst-en-verliesrekening wil samenstellen, een
  cijferbeoordeling wil uitvoeren, wil vergelijken met vorig jaar, of vraagt
  om "de jaarrekening", "concept jaarrekening", "balans opmaken",
  "winst-en-verliesrekening", "cijferbeoordeling" of "hoe staan de cijfers"
  voor een klant en boekjaar. Werkt met Exact Online, Moneybird en AFAS.
model: opus
---

# Concept Jaarrekening

Je stelt een concept jaarrekening samen: balans, winst-en-verliesrekening, ratio-analyse en vergelijking met vorig jaar.

## Aanpak

**Stap 1 — Haal saldibalans op (huidig + vorig jaar)**

Exact Online:
```sql
SELECT GLAccountCode, GLAccountDescription, Amount, AmountDebit, AmountCredit,
       GLAccountClassification
FROM Financial.ReportingBalance
WHERE ReportingYear = {jaar}
ORDER BY GLAccountCode

-- En vorig jaar:
WHERE ReportingYear = {vorigJaar}
```

Grootboekclassificatie:
```sql
SELECT Code, Description, Type
FROM Financial.GLClassifications
```

Moneybird:
- `get_balance_sheet` — als beschikbaar
- Anders: exporteer via `list_ledger_accounts` en bouw zelf op

**Stap 2 — Rubriceer conform RJ-richtlijnen**

Groepeer rekeningen in de standaard jaarrekening-indeling:

BALANS ACTIVA:
- Vaste activa: 0xxx rekeningen
- Vlottende activa: debiteuren (1300), overige vorderingen (1400-1499), liquide middelen (1000-1099)

BALANS PASSIVA:
- Eigen vermogen: 0500-0599 (aandelenkapitaal, reserves, resultaat)
- Langlopende schulden: 1700-1799
- Kortlopende schulden: crediteuren (1600), BTW (1500), overige (1800-1899)

W&V REKENING:
- Omzet: 8xxx
- Inkoopwaarde: 7000-7099
- Brutowinst = Omzet − Inkoopwaarde
- Bedrijfskosten: 4xxx (personeel), 4xxx (huisvesting), 4xxx (auto), 4xxx (afschrijvingen)
- Bedrijfsresultaat
- Financiële baten/lasten: 8500-8599
- Resultaat voor belasting
- VPB (schatting indien BV)
- Nettoresultaat

Zie `references/rj-richtlijnen.md` voor gedetailleerde rubrieksindeling.

**Stap 3 — Voer cijferbeoordeling uit**

Vergelijking huidig vs. vorig jaar. Markeer afwijkingen:
- Omzetwijziging > 20%: ⚠️ toelichting vereist
- Brutomarge-afwijking > 5%-punt: ⚠️
- Personeelskostenratio-afwijking > 5%-punt: ⚠️

Ratio's berekenen:
```
Current ratio       = Vlottende activa ÷ Kortlopende schulden  (norm: > 1.0)
Solvabiliteit       = Eigen vermogen ÷ Totaal vermogen         (norm: > 25%)
Brutomarge          = (Omzet − Inkoopwaarde) ÷ Omzet
Personeelskostenratio = Personeelskosten ÷ Omzet
```

**Stap 4 — Controleer volledigheid**

Vereiste informatie voor een volledige jaarrekening (NV COS 4410):
- [ ] Alle bankrekeningen aangesloten
- [ ] Debiteuren specificatie ✓
- [ ] Crediteuren specificatie ✓
- [ ] BTW-saldo aangesloten met aangiftes
- [ ] Afschrijvingen verwerkt
- [ ] Overlopende posten verwerkt
- [ ] RC DGA toegelicht (indien aanwezig)
- [ ] Lonen aangesloten (indien personeel)

**Stap 5 — Presenteer concept**

```
CONCEPT JAARREKENING — [Klantnaam] — Boekjaar [Jaar]
(Samengesteld conform NV COS 4410)

BALANS per 31 december [jaar]

ACTIVA                          [jaar]      [vorig]
Vaste activa                  € 185.000   € 220.000
Vlottende activa
  Debiteuren                  €  38.500   €  32.000
  Overige vorderingen         €   5.200   €   4.800
  Liquide middelen            €  42.300   €  38.100
TOTAAL ACTIVA                 € 271.000   € 294.900

PASSIVA
Eigen vermogen                € 185.000   € 195.000
  Aandelenkapitaal            €  18.000   €  18.000
  Overige reserves            € 128.000   € 119.000
  Resultaat boekjaar          €  39.000   €  58.000
Langlopende schulden          €  45.000   €  58.000
Kortlopende schulden          €  41.000   €  41.900
TOTAAL PASSIVA                € 271.000   € 294.900

WINST-EN-VERLIESREKENING [jaar]
...

RATIO-ANALYSE
Current ratio: 2.1  ✅ (vorig jaar: 1.9)
Solvabiliteit: 68%  ✅ (vorig jaar: 66%)
Brutomarge:    42%  ✅ (vorig jaar: 44% — afwijking: -2%-punt, zie toelichting)

ACTIEPUNTEN VOOR DEFINITIEVE JAARREKENING:
□ Accountantsverklaring / samenstellingsverklaring toevoegen
□ Toelichting bij afwijkende posten schrijven
□ SBR-aanlevering via Nextens (buiten scope van dit systeem)
```

## Goedkeuringsmodel

- 🟢 **GROEN** — Cijfers ophalen, berekenen, presenteren (automatisch)
- 🟡 **ORANJE** — Correctieboekingen voorstellen voor gevonden onregelmatigheden
- 🔴 **ROOD** — Definitief indienen (SBR, KvK-deponering) — buiten scope, doorverwijzen

## Beperkingen

- SBR/XBRL-aanlevering en KvK-deponering gaan via Nextens of Exact Jaarrekening module — buiten scope van deze skill
- De samenstellingsverklaring (NV COS 4410) schrijft de accountant zelf
- Looncontrole: zie afzonderlijke check bij personeel (vraag of er lonen zijn)

## Referenties

Voor RJ-richtlijnen en balansindeling:
> Lees `references/rj-richtlijnen.md`
