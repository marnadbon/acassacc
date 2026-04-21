---
name: kwaliteitscheck-administratie
description: >
  Gebruik deze skill wanneer een accountant de administratie wil controleren
  op fouten, wil checken op dubbele boekingen, foute BTW-codes, verkeerde
  grootboekrekeningen of openstaande tussenrekeningen, of vraagt om een
  "kwaliteitscheck", "administratiecontrole", "check de boekhouding" of
  "zijn er fouten" voor een klant. Werkt met Exact Online, Moneybird en AFAS.
---

# Kwaliteitscheck Administratie

Je voert een gestructureerde controle uit op de meest voorkomende fouten in de administratie.

## Aanpak

**Stap 1 — Bepaal periode**

Als niet opgegeven: controleer het huidige boekjaar, huidige en vorige maand.

**Stap 2 — Voer 4 controles uit**

### Controle 1: Dubbele boekingen

Exact Online:
```sql
SELECT Amount, Date, AccountCode, Description, COUNT(*) as AantalKeer
FROM FinancialTransaction.TransactionLines
WHERE FinancialYear = {jaar}
GROUP BY Amount, Date, AccountCode, Description
HAVING COUNT(*) > 1
```

Signaleer als: zelfde bedrag + zelfde datum + zelfde relatie = waarschijnlijk dubbel.

### Controle 2: Foute BTW-codes

Haal BTW-transacties op en controleer:
```sql
SELECT tl.GLAccountCode, tl.VATCode, tl.Amount, gl.Description as Rekening
FROM FinancialTransaction.TransactionLines tl
JOIN Financial.GLAccounts gl ON tl.GLAccountCode = gl.Code
WHERE tl.FinancialYear = {jaar}
AND tl.VATCode IS NOT NULL
```

Bekende foute combinaties:
- BTW-code op salarisrekeningen (4000-4999) → fout
- BTW-code op bankrekeningen (1000-1099) → fout tenzij aankoop
- Hoog BTW-tarief (21%) op leveringen die 9% of 0% zouden moeten zijn

### Controle 3: Tussenrekeningen met openstaand saldo

```sql
SELECT GLAccountCode, GLAccountDescription, Amount
FROM Financial.ReportingBalance
WHERE ReportingYear = {jaar}
AND ReportingPeriod = {huidigePeriode}
AND GLAccountCode BETWEEN '1300' AND '1599'  -- tussenrekeningen
AND ABS(Amount) > 0.01
```

Tussenrekeningen horen saldo = 0 te hebben. Afwijking = probleem.

### Controle 4: Grote of afwijkende boekingen

Detecteer uitschieters (bedrag > gemiddelde + 3× standaarddeviatie) voor handmatige review.

**Stap 3 — Rapporteer**

```
KWALITEITSCHECK — [Klantnaam] — [Periode]

✅ Geen dubbele boekingen gevonden
⚠️ 3 foute BTW-codes gevonden:
   - Factuur #1234: BTW 21% op energiekosten (moet 9%)
   - ...
⚠️ Tussenrekening 1400 heeft saldo € 850 (verwacht: 0)
✅ Geen afwijkende grote boekingen

2 punten vereisen actie. Wil je correctievoorstellen?
```

**Stap 4 — Correctievoorstellen** (🟡 ORANJE)

Voor elke gevonden fout: stel een memoriaalpost voor als correctie. Presenteer alle voorstellen tegelijk, vraag eenmalig om goedkeuring.

## Moneybird

Moneybird heeft minder analysemogelijkheden. Controleer:
- `list_sales_invoices` + `list_purchase_invoices` op dubbele facturen (zelfde bedrag + datum + contact)
- Openstaande posten die ouder zijn dan 1 jaar (waarschijnlijk administratieve fout)

## Referenties

### Reference bestanden
- **`references/exact-queries.md`** — SQL queries voor kwaliteitschecks (TransactionLines, VATCodes, ReportingBalance)

### Voorbeelden
- **`examples/`** — Voorbeeldoutputs van kwaliteitschecks

Laad `references/exact-queries.md` voor de exacte queries bij het zoeken naar dubbele boekingen en foute BTW-codes.
