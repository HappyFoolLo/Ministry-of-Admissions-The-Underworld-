# Project Sisyphus — Phase 2 Lab: Admissions of the Damned

A real, deliberately vulnerable local target for SQL injection tool
practice (sqlmap, Burp Suite, OWASP ZAP). This is a genuine SQLite
backend with a raw, unparameterized query — not a simulation.

## ⚠️ Run this only on your own machine, isolated from any network
Bind address is `127.0.0.1` (localhost) by default. Do not change
this to `0.0.0.0` or expose it beyond your own test environment.

## Setup

```bash
cd hades_lab
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 build_db.py             # creates hades.db
python3 app.py                  # starts the server on http://127.0.0.1:5000
```

## What's vulnerable

`GET /search?name=<value>` builds this query by string concatenation,
with no parameterization or escaping:

```python
query = "SELECT name, crime, sentence FROM prisoners WHERE name = '" + name + "'"
```

This supports classic techniques:

- **Error-based discovery** — a stray `'` triggers a visible SQLite
  error in the response, useful for confirming injection and mapping
  syntax.
- **Boolean/tautology bypass** — e.g. `' OR '1'='1` returns every
  prisoner record.
- **UNION-based extraction** — e.g.
  `' UNION SELECT username, password, null FROM staff --`
  pulls credentials out of the `staff` table, which the normal query
  never touches. `' UNION SELECT name, rank, access_code FROM guards --`
  does the same for `guards`.

## Schema

- `prisoners(id, name, crime, sentence)`
- `guards(id, name, rank, access_code)`
- `staff(id, name, username, password)` — includes Hades, Persephone,
  Thanatos, Hypnos, Minos

## Tool pointers

- **sqlmap**: `sqlmap -u "http://127.0.0.1:5000/search?name=Sisyphus" --dbms=sqlite --dump`
- **Burp Suite / OWASP ZAP**: proxy through the browser or `curl` and
  fuzz the `name` parameter directly.

## Resetting the data

Re-run `python3 build_db.py` at any time to wipe and reseed `hades.db`.
