---
name: grootboek-specificeren
description: >
  Gebruik deze skill wanneer een accountant een balanspost wil specificeren,
  een specificatierapport wil maken, wil weten wat er op een bepaalde
  grootboekrekening staat, de debiteuren, crediteuren, bank, BTW of vaste
  activa balanspost wil onderbouwen, of vraagt om "specificeer de balans",
  "maak een specificatie van", "onderbouw de post" of "wat staat er op
  rekening" voor een klant. Werkt met Exact Online, Moneybird en AFAS.
model: opus
---

# Grootboek Specificeren

Je maakt een gedetailleerd specificatierapport voor één of meerdere balansposten. Dit is de kern van het samenstellingswerk.

## Aanpak

**Stap 1 — Bepaal welke balanspost**

Als niet opgegeven, vraag: welke balanspost? (bank, debiteuren, crediteuren, BTW, tussenrekeningen, RC DGA, vaste activa, of alle)

**Stap 2 — Haal data op per balanspost**

### BANK

```sql
SELECT GLAccountCode, GLAccountDescription, Amount
FROM Financial.ReportingBalance
WHERE ReportingYear = {jaar} AND ReportingPeriod = {periode}
AND GLAccountCode BETWEEN '1000' AND '1099'

SELECT Date, Description, Amount, EntryNumber
FROM FinancialTransaction.BankEntryLines
WHERE FinancialYear = {jaar} AND FinancialPeriod = {periode}
ORDER BY Date
```

### DEBITEUREN

```sql
SELECT AccountCode, AccountName, Amount, DueDate, EntryNumber, InvoiceDate
FROM Financial.ReceivablesList

SELECT Amount FROM Financial.ReportingBalance
WHERE GLAccountCode = '1300'  -- debiteurenrekening
```

Controleer: totaal ReceivablesList = saldo rekening 1300? Zo niet → verschilanalyse.

### CREDITEUREN

Zelfde patroon als debiteuren maar met `PayablesList` en rekening 1600.

### BTW

```sql
SELECT GLAccountCode, GLAccountDescription, Amount
FROM Financial.ReportingBalance
WHERE GLAccountCode BETWEEN '1500' AND '1599'  -- BTW-rekeningen
```

Vergelijk met ingediende BTW-aangiftes:
```sql
SELECT Year, Period, VATToPay, VATToReceive
FROM VAT.VATReturns
WHERE Year = {jaar}
```

### TUSSENREKENINGEN

```sql
SELECT GLAccountCode, GLAccountDescription, Amount
FROM Financial.ReportingBalance
WHERE ReportingYear = {jaar} AND ReportingPeriod = {periode}
AND GLAccountCode BETWEEN '1300' AND '1599'
AND ABS(Amount) > 0.01
```

Alle tussenrekeningen met saldo ≠ 0 vereisen toelichting in de jaarrekening.

### RC DGA

```sql
SELECT Amount, AmountDebit, AmountCredit, Count
FROM Financial.ReportingBalance
WHERE GLAccountCode = '{RC_DGA_rekening}'  -- meestal 1710 of 2410

SELECT Date, Description, Amount
FROM FinancialTransaction.TransactionLines
WHERE GLAccountCode = '{RC_DGA_rekening}'
AND FinancialYear = {jaar}
ORDER BY Date
```

Signaleer als stand boven €500.000 (Wet excessief lenen).

### VASTE ACTIVA

```sql
SELECT AssetCode, Description, StartDate, CostPrice, BookValue,
       DepreciationMethod, LifeTime, ResidualValue
FROM Assets.Assets
WHERE Status = 1  -- actief
```

**Stap 3 — Presenteer specificatierapport**

```
SPECIFICATIERAPPORT — [Klantnaam] — [Balanspost] — [Boekjaar]

SALDO PER [datum]: € [bedrag]

SAMENSTELLING:
[detaillijst per onderdeel]

AANSLUITING MET BALANS:
Saldo boekhouding:     € [bedrag]
Specificatie totaal:   € [bedrag]
Verschil:              €       0  ✅

BIJZONDERHEDEN:
[eventuele aandachtspunten]
```

**Stap 4 — Vaste activa: bereken afschrijvingen**

Als de post vaste activa is: activeer automatisch de afschrijvingen-berekenen skill voor de berekening.

## Referenties

Voor RJ-richtlijnen en classificatie-regels:
> Lees `references/rj-richtlijnen.md`
