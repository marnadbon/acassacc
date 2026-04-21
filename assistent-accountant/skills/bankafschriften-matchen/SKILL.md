---
name: bankafschriften-matchen
description: >
  Gebruik deze skill wanneer een accountant onverwerkte banktransacties wil
  matchen, bankafschriften wil verwerken, wil weten welke betalingen nog niet
  zijn geboekt, matchingsuggesties wil voor transacties, of vraagt om "de bank
  bij te werken", "transacties te verwerken" of "de bankafschriften te doen"
  voor een klant. Werkt met Exact Online, Moneybird en AFAS.
---

# Bankafschriften Matchen

Je helpt de accountant om onverwerkte banktransacties te matchen aan openstaande facturen en de juiste grootboekrekeningen voor te stellen.

## Aanpak

**Stap 1 — Detecteer beschikbaar pakket**

Controleer welke MCP-tools beschikbaar zijn en gebruik de eerste die werkt:

| Pakket | Detectie | Tool voor bankmutaties |
|--------|----------|----------------------|
| Exact Online | `run_query` beschikbaar | `SELECT * FROM BankEntryLines WHERE FinancialYear = {jaar} AND FinancialPeriod = {periode} AND Status = 0` |
| Moneybird | `list_financial_mutations` beschikbaar | `list_financial_mutations(state: "unprocessed")` |
| AFAS | AFAS MCP beschikbaar | GetConnector BankTransactions met filter Status = open |

Als de klant niet is opgegeven, vraag dan welke klant en welke periode.

**Stap 2 — Haal onverwerkte transacties op**

Voor Exact Online:
```sql
SELECT EntryID, Date, Amount, Description, BankAccount
FROM FinancialTransaction.BankEntryLines
WHERE Status = 0
ORDER BY Date DESC
```

Combineer met openstaande posten:
```sql
SELECT AccountName, Amount, DueDate, EntryNumber, Description
FROM Financial.ReceivablesList
UNION ALL
SELECT AccountName, Amount, DueDate, EntryNumber, Description  
FROM Financial.PayablesList
```

**Stap 3 — Analyseer en stel matches voor**

Matchinglogica (in volgorde van zekerheid):
1. **Exacte match** (bedrag + relatie): 🟢 automatisch voorstellen
2. **Bedrag match** (zelfde bedrag, bekende relatie): 🟡 voorstel met toelichting
3. **Geen match**: 🟡 suggestie op basis van omschrijving, vraag bevestiging

**Stap 4 — Rapporteer**

Presenteer als overzicht:

```
BANKAFSCHRIFTEN — [Klantnaam] — [Periode]

Totaal onverwerkt: 47 transacties (€ 84.320)

🟢 Automatisch te matchen (32):  € 61.200 (68%)
🟡 Voorstel met toelichting (10): € 18.500 (21%)
🔴 Handmatige beoordeling (5):    €  4.620 (11%)

Wil je dat ik de 🟢 matches doorvoer?
```

## Goedkeuringsmodel

- 🟢 **GROEN** — Ophalen, analyseren, matchingsuggesties presenteren (automatisch)
- 🟡 **ORANJE** — Boekingsvoorstel klaarzetten als memoriaalpost (meld + wacht op "ja")
- 🔴 **ROOD** — Definitief boeken in het systeem (expliciete bevestiging verplicht)

Vraag nooit meer dan één keer om bevestiging. Groepeer alle voorstellen en vraag eenmalig.

## MCP-specifieke details

**Exact Online — let op:**
- `BankEntryLines` heeft veld `Status`: 0 = onverwerkt, 20 = verwerkt
- Relaties matchen via `Accounts?$filter=substringof('{naam}', Name)`
- Historische patronen ophalen via `TransactionLines?$filter=Journal eq guid'{bankdagboek}'`
- Schrijfactie (boeking): `GeneralJournalEntry/GeneralJournalEntries` POST → 🔴 ROOD

**Moneybird — let op:**
- `list_financial_mutations` geeft bank- en kassabonnen terug
- Filter `state: "unprocessed"` voor alleen onverwerkte
- Contacten matchen via `list_contacts`

**AFAS — let op:**
- Gebruik GetConnector `BankTransactions` met filter `<Filter><Field FieldId="Status" OperatorType="1"><Value>0</Value></Field></Filter>`
- UpdateConnector voor wegschrijven

## Referenties

Als je de beschikbare Exact Online queries nodig hebt:
> Lees `references/exact-queries.md`

Als je de Moneybird endpoints nodig hebt:
> Lees `references/moneybird-endpoints.md`
