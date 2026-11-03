"""
Project Sisyphus - Admissions of the Damned
Deliberately vulnerable Flask app for LOCAL, ISOLATED lab use only.

All records (prisoners, guards, staff) live in hades.db. Nothing sensitive
is embedded in the page or its source; the only way to read it is through
the vulnerable query.

The SQL is built by raw string concatenation on purpose, so that real tools
(sqlmap, Burp Suite, OWASP ZAP) can be pointed at it during an authorized,
controlled test. Do not deploy this anywhere reachable outside your own
test environment.

LAB_MODE controls difficulty:
  hard (default)  naive case-sensitive blocklist in front of the query, and
                  every failure returns the same generic "no records" page.
  easy            no filter, and raw SQLite errors are shown.

  Example:  LAB_MODE=easy python3 app.py
"""

import os
import sqlite3

from flask import Flask, render_template_string, request

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "hades.db")
MODE = os.environ.get("LAB_MODE", "hard").lower()
if MODE not in ("easy", "hard"):
    raise SystemExit("LAB_MODE must be 'easy' or 'hard'.")

# Naive literal-substring filter (hard mode only). It checks exact,
# case-sensitive phrases, a common real-world shortcut.
BLOCKED = ["union select", "or 1=1", "or 1 = 1", "or '1'='1"]

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ministry of Admissions - The Underworld</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>
  :root { --bg:#15120f; --bg2:#1d1812; --panel:#221c15; --bronze:#8a6a35;
          --bronze-light:#c9a35c; --parch:#e9ddc2; --dim:#b7ab8e;
          --oxide:#7a2b24; --oxide-light:#b84636; --rule:#3a3327;
          color-scheme: dark; }
  * { box-sizing:border-box; }
  body { margin:0; min-height:100vh; display:flex; justify-content:center;
         font-family:'EB Garamond', Georgia, serif; color:var(--parch);
         background: radial-gradient(ellipse at 50% -10%, #2a2015 0%, transparent 55%), var(--bg); }
  .page { width:100%; max-width:680px; padding:56px 24px 64px; }
  .crest { text-align:center; color:var(--bronze-light); font-family:'Cinzel', serif;
           font-size:13px; letter-spacing:.08em; }
  h1 { font-family:'Cinzel', serif; font-size:clamp(28px,5vw,40px); text-align:center; margin:6px 0 2px; }
  .subtitle { text-align:center; color:var(--dim); font-style:italic; font-size:17px; margin:0 0 36px; }
  .divider { height:1px; background:linear-gradient(90deg, transparent, var(--bronze), transparent); margin-bottom:36px; }
  .panel { background:var(--panel); border:1px solid var(--rule); padding:28px; box-shadow:0 20px 50px rgba(0,0,0,.4); }
  .label { font-family:'Cinzel', serif; font-size:14px; color:var(--bronze-light); margin-bottom:18px; }
  form { display:flex; flex-direction:column; gap:14px; }
  form label { font-size:15px; color:var(--dim); }
  .row { display:flex; gap:10px; }
  input[type=text] { flex:1; min-width:0; background:var(--bg2); border:1px solid var(--rule); color:var(--parch);
                     padding:12px 14px; font-family:inherit; font-size:17px; }
  input[type=text]:focus { outline:2px solid var(--bronze-light); outline-offset:1px; }
  button { background:var(--oxide); color:var(--parch); border:1px solid var(--oxide-light); padding:0 22px;
           font-family:'Cinzel', serif; font-size:14px; cursor:pointer; }
  button:hover { background:var(--oxide-light); }
  .results { margin-top:24px; }
  table { width:100%; border-collapse:collapse; font-size:16px; }
  th { text-align:left; font-family:'Cinzel', serif; font-weight:500; font-size:12px; color:var(--bronze-light);
       padding:8px 10px; border-bottom:1px solid var(--rule); }
  td { padding:9px 10px; border-bottom:1px solid var(--rule); }
  .empty { color:var(--dim); font-style:italic; padding:14px 2px; }
  .err { color:var(--oxide-light); font-family:ui-monospace, Menlo, monospace; font-size:14px;
         white-space:pre-wrap; padding:14px 2px; }
  footer { text-align:center; margin-top:36px; font-size:12px; color:var(--rule);
           font-family:'Cinzel', serif; letter-spacing:.04em; }
</style>
</head>
<body>
<!--
  guards_note.txt
  ----------------
  Guards, please remember your ranks and access codes.
  Thank you,
  Persephone
-->
<div class="page">
  <div class="crest">&#9765; ΑΔΗΣ · DIVISION OF RECORDS &#9765;</div>
  <h1>Ministry of Admissions</h1>
  <p class="subtitle">Search the registry of the condemned</p>
  <div class="divider"></div>
  <div class="panel">
    <div class="label">Registry Lookup</div>
    <form method="get" action="/search">
      <label for="name">Search by soul's recorded name</label>
      <div class="row">
        <input type="text" id="name" name="name" value="{{ q }}" autocomplete="off" placeholder="e.g. Sisyphus">
        <button type="submit">Search</button>
      </div>
    </form>
    <div class="results">
      {% if error %}
        <div class="err">{{ error }}</div>
      {% elif rows is none %}
        <div class="empty">No search performed yet.</div>
      {% elif not rows %}
        <div class="empty">No matching records found.</div>
      {% else %}
        <table>
          <tr>{% for col in columns %}<th>{{ col }}</th>{% endfor %}</tr>
          {% for row in rows %}<tr>{% for val in row %}<td>{{ val }}</td>{% endfor %}</tr>{% endfor %}
        </table>
      {% endif %}
    </div>
  </div>
  <footer>WE KNOW COMPUTERS AND STUFF</footer>
</div>
</body>
</html>
"""


def render(q="", rows=None, columns=(), error=None):
    return render_template_string(PAGE, q=q, rows=rows, columns=columns, error=error)


@app.route("/")
def index():
    return render()


@app.route("/search")
def search():
    name = request.args.get("name", "")

    if MODE == "hard" and any(phrase in name for phrase in BLOCKED):
        return render(q=name, rows=[])

    # VULNERABLE ON PURPOSE: raw string concatenation, no parameterization.
    query = "SELECT name, crime, sentence FROM prisoners WHERE name = '" + name + "'"

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(query)
        rows = cur.fetchall()
        columns = [d[0] for d in cur.description]
        return render(q=name, rows=rows, columns=columns)
    except sqlite3.Error as e:
        if MODE == "easy":
            return render(q=name, error=f"SQL error: {e}")
        # hard mode: failures look identical to a normal empty result
        return render(q=name, rows=[])
    finally:
        conn.close()


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        raise SystemExit("hades.db not found - run build_db.py first.")
    print(f"Running in {MODE.upper()} mode on http://127.0.0.1:5000")
    # debug=False on purpose: the vulnerability is the SQL query, not the
    # Flask debugger. Bind to localhost only.
    app.run(host="127.0.0.1", port=5000, debug=False)
