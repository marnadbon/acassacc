"""
BTW bulk status overzicht — geeft per klant de BTW-status voor een kwartaal.
Gebruik als basis voor de bulk-run loop in btw-bulk-verwerking skill.

Input: JSON-bestand met klantlijst (gegenereerd door Exact Online MCP)
Output: Statusoverzicht per klant
"""
import json
import sys
from datetime import datetime

STATUSSEN = {
    "ingediend":    ("✅", "Ingediend"),
    "concept":      ("🔄", "Concept klaar"),
    "data_ontbreekt": ("⚠️", "Data ontbreekt"),
    "fout":         ("❌", "Fout gevonden"),
    "niet_gestart": ("⬜", "Niet gestart"),
}

def maak_overzicht(klanten: list, kwartaal: str, jaar: int) -> str:
    regels = [f"\nBTW BULK STATUS — {kwartaal} {jaar}",
              f"Gegenereerd: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n",
              f"{'Klant':<35} {'Status':<25} {'Opmerking'}",
              "-" * 80]

    for k in klanten:
        icoon, label = STATUSSEN.get(k.get("status", "niet_gestart"), ("?", "Onbekend"))
        regels.append(f"{k['naam']:<35} {icoon} {label:<20} {k.get('opmerking', '')}")

    ingediend = sum(1 for k in klanten if k.get("status") == "ingediend")
    regels.append(f"\nTotaal: {len(klanten)} klanten | ✅ {ingediend} ingediend | "
                  f"⬜ {len(klanten) - ingediend} nog te doen")
    return "\n".join(regels)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Gebruik: python bulk-status.py <klanten.json> [kwartaal] [jaar]")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        klanten = json.load(f)

    kwartaal = sys.argv[2] if len(sys.argv) > 2 else "Q?"
    jaar = int(sys.argv[3]) if len(sys.argv) > 3 else datetime.now().year
    print(maak_overzicht(klanten, kwartaal, jaar))
