# Voorbeeld: Bankafschriften matchen

## Invoerprompt
"Match de bankafschriften voor Kapsalon Bella, periode maart 2025"

## Verwachte output

```
BANKAFSCHRIFTEN MATCHING — Kapsalon Bella — Maart 2025
Onverwerkte transacties gevonden: 8

🟢 AUTOMATISCH MATCHEN (hoge zekerheid):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
03-03  -€ 2.340,00  "Betaling factuur 2025-018"  → Crediteur: Henco Supplies (factuur 2025-018) ✅
07-03  +€ 5.800,00  "SEPA L. Jansen"             → Debiteur: L. Jansen BV (factuur 2025-004) ✅
15-03  -€   450,00  "IDEAL Huur maart"           → Rekening 4620 (huurkosten) ✅

🟡 CONTROLEREN VOOR MATCHEN (twijfelgevallen):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
22-03  -€   189,00  "Betaling 189"               → Mogelijke match: Factuur €189,50 van Beautyline? (verschil: €0,50)
28-03  +€ 1.200,00  "Overboeking"                → Geen duidelijke match — privé-storting DGA?

❌ GEEN MATCH GEVONDEN:
━━━━━━━━━━━━━━━━━━━━━━
12-03  -€   75,00   "PIN 75,00 SPAR"             → Kassa-uitgave, handmatig te categoriseren
18-03  -€  340,00   "Automatische incasso"       → Incasso-partij onbekend — welke leverancier?
25-03  +€  500,00   "Spaarrekening"              → Eigen rekening? Bevestig rekening-nr

Samenvatting: 3 automatisch ✅ | 2 ter controle 🟡 | 3 handmatig ❌

Zal ik de 3 automatische matches doorzetten naar Exact Online? 🔴
```
