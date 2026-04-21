# Documentchecklists per Opdrachttype

> Laad dit bestand wanneer je controleert welke stukken nog ontbreken voor een opdracht.

## Checklist BTW-aangifte

**Altijd vereist:**
- [ ] Bankafschriften voor de aangifteperiode (of directe bankverbinding actief)
- [ ] Eventuele kassabonnen (indien kasboek bijgehouden)

**Controleer of al in systeem:**
- [ ] Verkoopfacturen alle perioden in het kwartaal ingeboekt?
- [ ] Inkoopfacturen alle perioden in het kwartaal ingeboekt?
- [ ] Creditnota's verwerkt?

**Bijzonder (vraag altijd):**
- [ ] Correcties vorige periodes? (vraag actief)
- [ ] Nieuwe investeringen in het kwartaal? (BTW te verrekenen)
- [ ] ICP-leveringen? (extra: ICP-opgave indienen)

---

## Checklist Jaarrekening

**Banken:**
- [ ] Jaaropgave bankrekening(en) per 31-12 (alle rekeningen)
- [ ] Eventuele spaarbankrekeningen per 31-12

**Onroerend goed (indien eigendom):**
- [ ] WOZ-beschikking bedrijfspand (gemeente stuurt dit toe)
- [ ] Hypotheekopgave per 31-12 (bank)
- [ ] Eigendomsakte of koopakte (eenmalig)

**Personeel:**
- [ ] Jaaropgave loonheffing december (of LH-aangifte dec)
- [ ] Pensioenopgave per 31-12
- [ ] UWV-opgave premies werknemersverzekeringen

**Financiering:**
- [ ] Leningsoverzicht per 31-12 (alle leningen in en uit)
- [ ] Aflossingsschema's

**Voorraden (indien van toepassing):**
- [ ] Inventarisatielijst per 31-12 (telling + waardering)
- [ ] Onderhanden werk per 31-12

**DGA:**
- [ ] Jaaropgave DGA-salaris
- [ ] Privé-gebruik auto (bijtelling of rittenregistratie)
- [ ] Opgave privéonttrekkingen (indien eenmanszaak/VOF)

**Deelnemingen:**
- [ ] Jaarrekeningen deelnemingen (indien meerderheidsbelang)

**Overig:**
- [ ] Verzekeringspolissen en -premies (controle)
- [ ] Lopende rechtszaken / claims (voor voorzieningen)

---

## Checklist Fiscaal (VPB-aangifte voorbereiding)

**Investeringen:**
- [ ] Investeringslijst boekjaar (nieuw aangeschafte activa)
- [ ] Desinvesteringslijst (verkochte/afgevoerde activa)
- [ ] Facturen nieuwe investeringen > €2.800 (voor KIA)

**DGA-positie:**
- [ ] DGA-salaris jaaropgave (voor gebruikelijk loon check)
- [ ] Stand R/C DGA per 31-12 (voor Wet excessief lenen check)
- [ ] Renteberekening R/C DGA (indien lening structuur)

**Verliesverrekening:**
- [ ] Verliescarry-forward vorige jaren (indien van toepassing)

**Bijzonder:**
- [ ] Deelnemingsvrijstelling (indien deelneming aanwezig)
- [ ] Innovatiebox (indien R&D activiteiten)
- [ ] Functionele valuta (indien relevant)

---

## Hoe te controleren wat al ontvangen is

### Via Exact Online Documents API
```sql
SELECT FileName, Category, Created, Description
FROM Documents.Documents
WHERE AccountID = '{klantGuid}'
AND Created >= datetime('{startperiode}')
ORDER BY Created DESC
```

### Als Documents API niet beschikbaar is
Vraag de accountant: "Welke van deze stukken zijn al ontvangen of liggen er al in het dossier?"

---

## E-mail Templates

### Template: Jaarrekening stukken opvragen

**Onderwerp:** Jaarrekening [jaar] — benodigde stukken

```
Beste [aanspreking] [achternaam],

Wij zijn gestart met de werkzaamheden voor uw jaarrekening [jaar]. 
Om deze tijdig af te kunnen ronden, ontvangen wij graag nog de volgende stukken:

[LIJST VAN ONTBREKENDE STUKKEN MET UITLEG]

Kunt u deze stukken voor [datum] aanleveren via [methode: e-mail/portaal]?

Heeft u vragen, neem dan gerust contact met ons op.

Met vriendelijke groet,
[naam]
[kantoor]
```

### Template: BTW stukken opvragen

**Onderwerp:** BTW-aangifte [kwartaal] [jaar] — ontbrekende informatie

```
Beste [aanspreking] [achternaam],

Voor het opstellen van uw BTW-aangifte over [kwartaal] [jaar] hebben wij nog 
de volgende informatie nodig:

[LIJST]

Kunt u dit zo spoedig mogelijk aanleveren? De uiterste aangiftedatum is [datum].

Met vriendelijke groet,
[naam]
```

### Aanspreking

Gebruik altijd "de heer" of "mevrouw" als je het geslacht weet, anders gebruik voornaam.
Bij twijfel: gebruik de volledige naam.
