---
name: btw-aangifte-voorbereiden
description: >
  Gebruik deze skill wanneer een accountant een BTW-aangifte wil voorbereiden,
  BTW-bedragen wil berekenen per rubriek, de BTW wil controleren voor een
  kwartaal of maand, wil vergelijken met vorige periode, of vraagt om
  "de BTW doen", "BTW aangifte voorbereiden", "BTW berekenen" of
  "BTW controleren" voor een specifieke klant en periode.
  Werkt met Exact Online, Moneybird en AFAS.
---

# BTW-Aangifte Voorbereiden

Je bereidt de BTW-aangifte voor door alle BTW-transacties te analyseren, te rubriceren en te vergelijken met de vorige periode.

## Aanpak

**Stap 1 — Zorg voor juiste parameters**

Benodigde info:
- Klant (welke administratie/divisie)
- Periode: Q1 (jan-mrt), Q2 (apr-jun), Q3 (jul-sep), Q4 (okt-dec), of specifieke maand
- Jaar

**Stap 2 — Haal BTW-transacties op**

Exact Online:
```sql
SELECT VATCode, VATPercentage, VATAmountDC, VATBaseAmountDC, Type, Date
FROM VAT.VATTransactions
WHERE FinancialYear = {jaar}
AND FinancialPeriod BETWEEN {startperiode} AND {eindperiode}
```

> Let op: VATPercentages komen leeg terug bij VATCodes lijstcall.
> Haal percentages per code op via individuele GET:
> `GET /api/v1/{div}/vat/VATPercentages?$filter=VATCodeID eq guid'{id}'`

Moneybird:
```
GET /api/v1/{admin_id}/tax_returns
list_sales_invoices → filter op perioden
list_purchase_invoices → filter op perioden
```

**Stap 3 — Rubriceer**

Wijs elke transactie toe aan een rubriek. Zie `references/btw-rubrieken.md` voor de volledige rubriekenkaart.

Kern:
- **1a** (hoog tarief 21%): binnenlandse verkopen 21%
- **1b** (laag tarief 9%): binnenlandse verkopen 9%
- **1c** (overige tarieven): 0% of vrijgesteld
- **2a** (verlegde BTW): diensten van buitenlandse ondernemer
- **4a** (EU-leveringen intracommunautair): ICP-omzet
- **5b** (voorbelasting): alle inkoop-BTW

**Stap 4 — Vergelijk met vorige periode**

```sql
SELECT VATCode, SUM(VATAmountDC) as BedragVorigJaar
FROM VAT.VATTransactions
WHERE FinancialYear = {vorigJaar}
AND FinancialPeriod BETWEEN {startperiode} AND {eindperiode}
GROUP BY VATCode
```

**Stap 5 — Presenteer aangifte**

```
BTW-AANGIFTE — [Klantnaam] — [Q1/Q2/Q3/Q4] [Jaar]

OMZET
Rubriek 1a (hoog 21%):    Omzet € 85.000  | BTW € 17.850
Rubriek 1b (laag  9%):    Omzet € 12.000  | BTW €  1.080
Rubriek 1c (vrijgesteld): Omzet €  5.000  | BTW €      0

BUITENLAND
Rubriek 4a (ICP):         Omzet €      0  | BTW €      0

VERSCHULDIGD
Rubriek 5a (te betalen):               BTW € 18.930

AFTREKBAAR
Rubriek 5b (voorbelasting):            BTW €  6.200

TE BETALEN / TE ONTVANGEN:             BTW € 12.730

Vergelijking [vorige periode]: +8% (seizoensinvloed verwacht ✅)
Afwijkingen: geen ✅

Wil je deze aangifte ter review klaarzetten?
```

## Referenties

Als je de volledige rubriekenkaart nodig hebt (1a t/m 5g):
> Lees `references/btw-rubrieken.md`
