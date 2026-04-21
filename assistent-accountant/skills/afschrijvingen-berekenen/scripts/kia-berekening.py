"""
KIA-staffel berekening 2025 (Kleinschaligheidsinvesteringsaftrek)
Gebruik: python kia-berekening.py <investeringsbedrag>
"""
import sys

KIA_STAFFEL_2025 = [
    (0,       2_800,    0.00,  None),
    (2_800,   69_765,   0.28,  None),
    (69_765,  129_194,  None,  19_535),   # vast bedrag
    (129_194, 193_885,  None,  "sliding"), # aflopend naar 0
    (193_885, 387_580,  None,  "sliding"),
    (387_580, float("inf"), 0.00, None),
]

def bereken_kia(investering: float) -> dict:
    if investering <= 2_800:
        return {"investering": investering, "kia": 0, "toelichting": "Onder drempel €2.800"}

    if investering <= 69_765:
        kia = round(investering * 0.28, 2)
        return {"investering": investering, "kia": kia, "toelichting": "28% van investering"}

    if investering <= 129_194:
        return {"investering": investering, "kia": 19_535, "toelichting": "Vast bedrag €19.535"}

    if investering <= 387_580:
        # Lineair aflopend van 19.535 bij 129.194 naar 0 bij 387.580
        bereik = 387_580 - 129_194
        positie = investering - 129_194
        kia = round(19_535 * (1 - positie / bereik), 2)
        return {"investering": investering, "kia": max(0, kia), "toelichting": "Glijdende schaal"}

    return {"investering": investering, "kia": 0, "toelichting": "Boven maximum €387.580"}


if __name__ == "__main__":
    bedrag = float(sys.argv[1].replace(",", ".").replace(".", "", 1)) if len(sys.argv) > 1 else 0
    resultaat = bereken_kia(bedrag)
    print(f"Investering:  € {resultaat['investering']:>12,.2f}")
    print(f"KIA-aftrek:   € {resultaat['kia']:>12,.2f}")
    print(f"Toelichting:  {resultaat['toelichting']}")
