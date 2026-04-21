---
name: openstaande-posten-bewaken
description: >
  Gebruik deze skill wanneer een accountant openstaande facturen wil zien,
  debiteuren of crediteuren wil controleren, wil weten welke facturen te laat
  zijn, een ouderdomsanalyse wil, of vraagt om "de debiteuren", "openstaande
  rekeningen", "wie heeft er nog niet betaald", "welke facturen staan open"
  of "crediteuren overzicht" voor een klant. Werkt met Exact Online, Moneybird en AFAS.
---

# Openstaande Posten Bewaken

Je haalt de openstaande debiteuren en crediteuren op en maakt een ouderdomsanalyse.

## Aanpak

**Stap 1 — Detecteer pakket en haal data op**

Exact Online — debiteuren:
```sql
SELECT AccountCode, AccountName, Amount, DueDate, EntryNumber, InvoiceDate, Description, CurrencyCode
FROM Financial.ReceivablesList
ORDER BY DueDate ASC
```

Exact Online — crediteuren:
```sql
SELECT AccountCode, AccountName, Amount, DueDate, EntryNumber, InvoiceDate, Description
FROM Financial.PayablesList
ORDER BY DueDate ASC
```

Moneybird:
- `list_sales_invoices(filter: {state: "open"})` — openstaande verkoopfacturen
- `list_purchase_invoices(filter: {state: "open"})` — openstaande inkoopfacturen

AFAS:
- GetConnector `Debtors` met filter openstaand
- GetConnector `Creditors` met filter openstaand

**Stap 2 — Bereken ouderdomsanalyse**

Categoriseer op basis van `DueDate` vs. vandaag:

| Categorie | Definitie |
|-----------|-----------|
| Nog niet vervallen | DueDate > vandaag |
| 0-30 dagen te laat | DueDate 0-30 dagen geleden |
| 30-60 dagen te laat | DueDate 31-60 dagen geleden |
| 60-90 dagen te laat | DueDate 61-90 dagen geleden |
| >90 dagen te laat | DueDate >90 dagen geleden |

**Stap 3 — Rapporteer**

```
OPENSTAANDE DEBITEUREN — [Klantnaam] — [datum]

Totaal openstaand: € 87.450

| Categorie       | Bedrag    | Aantal |
|-----------------|-----------|--------|
| Nog niet vervallen | € 45.200 | 12 |
| 0-30 dagen      | € 28.000 |  8 |
| 30-60 dagen     | € 10.500 |  3 |
| 60-90 dagen     | €  2.750 |  1 |
| >90 dagen       | €  1.000 |  1 ⚠️ |

Top 3 grootste posten:
1. Bakkerij Jansen — € 18.500 — vervallen 5 dagen geleden
2. De Groene Tuin  — € 12.000 — vervalt over 12 dagen
3. Kapsalon Bella  — €  8.200 — vervallen 25 dagen geleden

Wil je dat ik een betalingsherinnering opstel voor posten >30 dagen?
```

**Stap 4 — Vervolgacties**

Na het overzicht, bied aan:
- Betalingsherinnering opstellen voor specifieke klanten (via e-mail MCP of als concept)
- Gedetailleerde factuurlijst voor een specifieke relatie
- Export als overzicht

## Goedkeuringsmodel

- 🟢 **GROEN** — Ophalen, berekenen, rapporteren (automatisch)
- 🟡 **ORANJE** — Betalingsherinnering opstellen als concept (toon eerst, wacht op "versturen")
- 🔴 **ROOD** — Herinneringen definitief versturen via e-mail

## Notities

- Toon bedragen altijd in euro met 2 decimalen
- Als een factuur >90 dagen open staat: markeer altijd met ⚠️ en stel actie voor
- Debiteurenlijst en crediteurenlijst altijd apart presenteren, nooit samenvoegen

## Referenties

### Reference bestanden
- **`references/exact-queries.md`** — SQL queries voor ReceivablesList en PayablesList
- **`references/moneybird-endpoints.md`** — Moneybird endpoints voor sales/purchase invoices

### Voorbeelden
- **`examples/`** — Voorbeeldoutputs van ouderdomsanalyses

Laad `references/exact-queries.md` voor de exacte SQL-syntax van ReceivablesList en PayablesList.
