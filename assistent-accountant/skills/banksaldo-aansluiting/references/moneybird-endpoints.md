# Moneybird MCP — Endpoints Referentie

> Laad dit bestand wanneer je Moneybird-specifieke API calls nodig hebt.

## Verbinding

Moneybird MCP gebruikt REST API via `vanderheijden86/moneybird-mcp-server`.
Basis-URL: `https://moneybird.com/api/v2/{administration_id}/`

## Bankmutaties

```
list_financial_mutations
  Parameters:
    state: "unprocessed" | "processed" | "ignored"
    period: "this_month" | "last_month" | "this_year" | "last_year" | custom
  
  Retourneert: id, date, message, amount, account_id, sepa_fields

create_financial_mutation (om transactie te boeken)
  → 🔴 ROOD goedkeuring vereist
```

## Openstaande Posten

```
list_sales_invoices
  Parameters:
    filter[state]: "open" | "late" | "paid" | "all"
    filter[period]: "this_month" | "last_month" etc.
  
  Retourneert: id, invoice_id, contact_id, state, due_date, total_price_incl_tax

list_purchase_invoices  
  Parameters:
    filter[state]: "open" | "paid" | "all"
  
  Retourneert: id, contact_id, due_date, total_price_incl_tax_base
```

## BTW

```
get_tax_returns
  Retourneert BTW-aangiftes per periode
  Fields: year, period, status, omzet_hoog, omzet_laag, btw_hoog, btw_laag, voorbelasting

list_tax_rates
  Retourneert BTW-tarieven: name, percentage, tax_rate_type
```

## Relaties

```
list_contacts
  Parameters:
    query: "zoekterm"
  Retourneert: id, company_name, firstname, lastname, email, phone

get_contact
  Parameters: contact_id
```

## Boekhouding

```
list_ledger_accounts
  Retourneert rekeningschema: id, name, account_type, parent_id

create_journal_entry (memoriaalpost)
  → 🟡 ORANJE goedkeuring vereist
```

## Administraties

```
list_administrations
  Retourneert alle Moneybird-administraties waartoe je toegang hebt
  Fields: id, name, language, currency, time_zone
```

## Notities

- Moneybird gebruikt `administration_id` in elke URL (niet divisienummer zoals Exact)
- BTW-codes zijn anders dan Exact Online — gebruik `tax_rate_id` referenties
- Automatisch reconciliëren is beperkt — suggesties doen op basis van bedrag/omschrijving
