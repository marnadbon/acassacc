# Exact Online MCP — Queries & Endpoints

> Laad dit bestand wanneer je Exact Online-specifieke queries nodig hebt voor bank, transacties of debiteuren/crediteuren.

## Verbinding

Exact Online MCP gebruikt CData SQL-interface. Alle tabellen zijn via `run_query` benaderbaar.

Basis: `SELECT * FROM [ServiceGroep].[Tabel] WHERE [filter]`

Divisienummer is automatisch meegenomen in de verbinding (per administratie).

## Bankmutaties

```sql
-- Alle onverwerkte bankmutaties
SELECT EntryID, Date, Amount, Description, BankAccount, Status
FROM FinancialTransaction.BankEntryLines
WHERE Status = 0
ORDER BY Date DESC

-- Bankmutaties voor specifieke periode
SELECT EntryID, Date, Amount, Description, BankAccount
FROM FinancialTransaction.BankEntryLines
WHERE FinancialYear = 2026
AND FinancialPeriod = 3  -- periode 3 = maart
ORDER BY Date

-- Bankdagboeken identificeren
SELECT JournalCode, Description, Type, BankAccount
FROM Financial.Journals
WHERE Type = 12  -- 12 = bankdagboek
```

## Debiteuren en Crediteuren

```sql
-- Openstaande debiteuren
SELECT AccountCode, AccountName, Amount, DueDate, EntryNumber,
       InvoiceDate, Description, CurrencyCode
FROM Financial.ReceivablesList
ORDER BY DueDate ASC

-- Openstaande crediteuren
SELECT AccountCode, AccountName, Amount, DueDate, EntryNumber,
       InvoiceDate, Description
FROM Financial.PayablesList
ORDER BY DueDate ASC

-- Specifieke relatie debiteuren
SELECT AccountName, Amount, DueDate, EntryNumber
FROM Financial.ReceivablesList
WHERE AccountName LIKE '%Jansen%'
```

## Grootboek en Saldibalans

```sql
-- Saldibalans voor periode
SELECT GLAccountCode, GLAccountDescription, Amount, AmountDebit, AmountCredit, Count
FROM Financial.ReportingBalance
WHERE ReportingYear = 2026
AND ReportingPeriod = 3

-- Specifieke rekening
SELECT GLAccountCode, GLAccountDescription, Amount
FROM Financial.ReportingBalance
WHERE ReportingYear = 2026
AND GLAccountCode = '1300'  -- debiteurenrekening

-- Alle rekeningen (rekeningschema)
SELECT Code, Description, Type, Classification
FROM Financial.GLAccounts
ORDER BY Code

-- Grootboekclassificaties
SELECT Code, Description, Type
FROM Financial.GLClassifications
```

## Transactielijnen

```sql
-- Alle transacties voor een periode
SELECT Date, GLAccountCode, Description, Amount, VATCode, Journal
FROM FinancialTransaction.TransactionLines
WHERE FinancialYear = 2026
AND FinancialPeriod BETWEEN 1 AND 3
ORDER BY Date

-- Transacties op specifieke rekening
SELECT Date, Description, Amount, AmountDC
FROM FinancialTransaction.TransactionLines
WHERE GLAccountCode = '1710'  -- RC DGA rekening
AND FinancialYear = 2026
ORDER BY Date
```

## BTW

```sql
-- BTW-transacties per periode
SELECT VATCode, VATAmountDC, VATBaseAmountDC, Date, Type
FROM VAT.VATTransactions
WHERE FinancialYear = 2026
AND FinancialPeriod BETWEEN 1 AND 3

-- BTW-codes
SELECT Code, Description, Type, VATPercentage
FROM VAT.VATCodes

-- Ingediende BTW-aangiftes
SELECT Year, Period, Status, VATToPay, VATToReceive, Created
FROM VAT.VATReturns
WHERE Year = 2025
ORDER BY Period DESC
```

## Activa

```sql
-- Activastaat
SELECT AssetCode, Description, StartDate, CostPrice, BookValue,
       ResidualValue, DepreciationMethod, LifeTime, DepreciationPercentage
FROM Assets.Assets
WHERE Status = 1  -- actief

-- Afschrijvingsmethoden
SELECT Code, Description
FROM Assets.DepreciationMethods
```

## Relaties

```sql
-- Klant/leverancier zoeken
SELECT ID, Code, Name, Email, Phone
FROM CRM.Accounts
WHERE Name LIKE '%Jansen%'

-- Contactpersoon
SELECT AccountName, FirstName, LastName, Email, Phone, IsMainContact
FROM CRM.Contacts
WHERE AccountID = '{guid}'
```

## Systeem

```sql
-- Alle divisies (administraties)
SELECT DivisionCode, Description, Status, Country
FROM System.Divisions
WHERE Status = 1

-- Financiële perioden
SELECT Year, Period, Status, StartDate, EndDate
FROM Financial.FinancialPeriods
WHERE Year = 2026
```

## Rate Limits

- 60 calls per minuut per company (divisie)
- 5.000 calls per dag per company
- Bij bulk: verwerk in batches, bouw 1 seconde pauze in tussen calls als je aan de limiet komt

## Let op: VATPercentages

VATCodes lijstcall geeft percentages leeg terug. Haal per code afzonderlijk op:
```sql
SELECT VATCodeID, Percentage, StartDate, EndDate
FROM VAT.VATPercentages
WHERE VATCodeID = '{guid}'
```
