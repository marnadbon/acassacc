---
name: afschrijvingen-berekenen
description: >
  Gebruik deze skill wanneer een accountant afschrijvingen wil berekenen,
  de activastaat wil controleren, wil weten hoeveel er afgeschreven moet
  worden, de investeringsaftrek wil berekenen, KIA wil toepassen, of vraagt
  om "afschrijvingen", "activastaat", "KIA berekenen", "nieuwe investeringen"
  of "bereken de afschrijvingen" voor een klant en boekjaar.
  Werkt met Exact Online.
---

# Afschrijvingen Berekenen

Je haalt de activastaat op, berekent de afschrijvingen voor het boekjaar en bepaalt de investeringsaftrek (KIA/EIA).

## Aanpak

**Stap 1 — Haal activastaat op**

Exact Online:
```sql
SELECT AssetCode, Description, StartDate, CostPrice, ResidualValue,
       BookValue, DepreciationMethod, LifeTime, DepreciationPercentage,
       AssetGroupDescription
FROM Assets.Assets
WHERE Status = 1  -- 1 = actief
ORDER BY AssetGroupDescription, StartDate
```

Afschrijvingsmethoden:
```sql
SELECT Code, Description
FROM Assets.DepreciationMethods
```

**Stap 2 — Bereken afschrijvingen**

### Lineaire afschrijving
```
Jaarlijkse afschrijving = (Aanschafwaarde − Restwaarde) ÷ Levensduur in jaren
Maandelijks = Jaarlijkse ÷ 12
```

### Degressief
```
Jaarlijkse afschrijving = Boekwaarde × Afschrijvingspercentage
Stop als boekwaarde ≤ restwaarde
```

### Overig
Exact Online slaat de methode op in het systeem — gebruik `DepreciationMethod` en `LifeTime` uit de API.

**Stap 3 — Nieuwe investeringen dit jaar**

```sql
SELECT AssetCode, Description, CostPrice, StartDate
FROM Assets.Assets
WHERE StartDate >= datetime('{startboekjaar}')
AND StartDate <= datetime('{eindboekjaar}')
```

**Stap 4 — KIA berekenen (Kleinschaligheidsinvesteringsaftrek)**

KIA-staffel 2025:
| Investering | Aftrek |
|-------------|--------|
| < € 2.800 | 0% |
| € 2.800 – € 69.764 | 28% |
| € 69.765 – € 129.194 | € 19.535 (vast bedrag) |
| € 129.195 – € 387.580 | € 19.535 − 7,56% × (investering − € 129.194) |
| > € 387.580 | 0% |

Bereken totale investeringen voor het jaar en pas de staffel toe.

**EIA/MIA/VAMIL**: Als er investeringen zijn in energiebesparende of milieuvriendelijke activa, meld dat controle nodig is (lijsten wijzigen jaarlijks — agent kan dit niet automatisch bepalen).

**Stap 5 — Rapporteer**

```
AFSCHRIJVINGSOVERZICHT — [Klantnaam] — [Boekjaar]

ACTIVASTAAT
| Code | Omschrijving  | Aanschaf  | BW begin | Afschrijving | BW einde |
|------|---------------|-----------|----------|--------------|----------|
| 001  | Laptop        | € 1.500   | € 750    | € 375        | € 375    |
| 002  | Auto          | € 35.000  | € 21.000 | € 7.000      | € 14.000 |
| ...  |               |           |          |              |          |
| TOTAAL              |           | € 185.000 | € 42.500 | € 142.500   |

NIEUWE INVESTERINGEN [Boekjaar]:
- [Asset]: € [bedrag] (aangeschaft [datum])
Totaal nieuw: € 28.000

KIA-BEREKENING:
Totale investeringen: € 28.000
KIA-aftrek (28%):     €  7.840

Wil je de journaalpost voor de afschrijvingen aanmaken?
```

## Moneybird / AFAS

Moneybird heeft geen uitgebreid activabeheer. Vraag de accountant om de activastaat als bestand te uploaden, of gebruik de gegevens uit de boekhouding zelf (grootboekrekeningen 0xxx).

## Referenties

### Reference bestanden
- **`references/exact-queries.md`** — SQL queries voor Assets.Assets en DepreciationMethods

### Scripts
- **`scripts/kia-berekening.py`** — KIA-staffel berekening 2025. Gebruik: `python kia-berekening.py <bedrag>`
  Geeft direct de KIA-aftrek terug op basis van de investering.

### Voorbeelden
- **`examples/voorbeeld-afschrijvingsoverzicht.md`** — Voorbeeld van een volledig afschrijvingsoverzicht met KIA-berekening

Gebruik `scripts/kia-berekening.py` voor precieze KIA-berekeningen; de staffel is complex en foutgevoelig als handmatig berekend.
