---
name: banksaldo-aansluiting
description: >
  Gebruik deze skill wanneer een accountant het banksaldo wil aansluiten,
  wil controleren of de boekhouding klopt met het bankafschrift, wil weten
  of er een verschil zit tussen bank en boekhouding, of vraagt om "de bank
  aan te sluiten", "het banksaldo te controleren" of "de aansluiting te
  maken" voor een bepaalde maand of periode. Werkt met Exact Online, Moneybird en AFAS.
---

# Banksaldo Aansluiting

Je vergelijkt het boekhoudsaldo van de bankrekening met het werkelijke banksaldo en brengt eventuele verschillen in kaart.

## Aanpak

**Stap 1 — Vraag ontbrekende informatie op**

Als niet opgegeven, vraag:
- Welke klant?
- Welke periode (maand/jaar)?
- Wat is het werkelijke eindsaldo van de bank op de laatste dag van die periode?

**Stap 2 — Haal boekhoudsaldo op**

Exact Online:
```sql
SELECT GLAccountCode, GLAccountDescription, Amount, AmountDebit, AmountCredit, Count
FROM Financial.ReportingBalance
WHERE ReportingYear = {jaar}
AND ReportingPeriod = {periode}
AND GLAccountCode LIKE '1%'  -- bankrekeningen beginnen met 1
```

Identificeer het bankdagboek:
```sql
SELECT JournalCode, Description, Type
FROM Financial.Journals
WHERE Type = 12  -- 12 = bankdagboek
```

Moneybird:
- `get_financial_accounts` → zoek bankrekeningen
- Saldo per datum ophalen

**Stap 3 — Analyseer verschil**

```
BANKAANSLUITING — [Klantnaam] — [Maand jaar]

Boekhoudsaldo (rekening [rek.nr]):  € 42.350,00
Werkelijk banksaldo:                € 42.350,00
Verschil:                           €      0,00  ✅

— OF —

Verschil: € 1.250,00 ⚠️

Mogelijke oorzaken:
□ Transacties in transit (nog onderweg)
□ Bankkosten nog niet geboekt
□ Onverwerkte stortingen/opnames
□ Boekingsfout

Wil je dat ik de onverwerkte bankmutaties voor deze periode erbij haal?
```

**Stap 4 — Bij verschil: verdiep**

Als er een verschil is:
1. Haal onverwerkte bankmutaties op (verwijzing naar bankafschriften-matchen skill)
2. Controleer of alle bankafschriften zijn ingelezen
3. Zoek naar openstaande tussenrekeningen (journaalboek)

## Goedkeuringsmodel

- 🟢 **GROEN** — Saldo ophalen, vergelijken, rapporteren (automatisch)
- 🟡 **ORANJE** — Correctieboeking voorstellen voor gevonden verschil
- 🔴 **ROOD** — Correctie definitief boeken

## Belangrijk

Het werkelijke banksaldo komt **niet** uit Exact Online — dat moet de accountant aanleveren (bankafschrift of online banking). De skill vergelijkt wat de accountant opgeeft met wat er in de boekhouding staat.

Als het saldo klopt en er geen onverwerkte transacties zijn: ✅ aansluiting compleet.
