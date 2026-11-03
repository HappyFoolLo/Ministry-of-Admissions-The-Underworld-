# Ministry of Admissions: The Underworld

A small, self-contained web challenge for practising **SQL injection** in a safe environment. The theme is Greek mythology: you're poking at the registry of the condemned, run by the Underworld's Division of Records.

> **This is a simulation.** There is no backend and no real database. All "queries" are interpreted by a few lines of client-side JavaScript, and every name, code, and credential in the data is fictional. Nothing here can touch a real system.

> **Want the real thing?** A companion project runs the same challenge against a genuine Flask + SQLite backend, so you can use tools like sqlmap, Burp Suite and OWASP ZAP. See the [Flask version](https://github.com/<your-username>/<flask-repo-name>).

## Run it

It's a single static file with no build step and no dependencies.

**Locally:** download the repo and open `Ministry of Admissions — The Underworld.html` in any modern browser.

**On GitHub Pages:**
1. Push this repo to GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, select `main` and `/ (root)`, then save.
4. GitHub Pages serves `index.html` at the root URL, so either rename the file to `index.html` first, or visit `https://<your-username>.github.io/<repo-name>/Ministry%20of%20Admissions%20%E2%80%94%20The%20Underworld.html`.

## The challenge

Search the registry by a soul's recorded name. Behind the scenes the input is treated as if it were dropped straight into a query like:

```sql
SELECT ... FROM prisoners WHERE name = '<your input>'
```

Your job is to work out how the application handles that input, and see what else the Ministry is keeping on file.

Some things worth knowing:

- Nothing about the underlying query is shown. You have to infer it, as you would against a real black-box app.
- Any failure (bad syntax, wrong column count, unknown table, filtered input) returns the same generic "No matching records found" message, so error messages won't help you.
- There's a naive filter in front of the query layer. Real-world filters like this are often weaker than they look.
- Read the page source. Real developers leave things lying around.

## Limitations

Because everything runs in the browser, the simulated records are stored in the page's own JavaScript. Anyone who opens View Source or developer tools can read them without solving anything. That makes this version best suited to learning the *concepts* (query structure, quote balancing, filter bypass, UNION column matching) rather than working as a tamper-proof challenge.

That limitation is also a lesson in itself: **secrets placed in front-end code are never secret.** Access control and sensitive data belong on the server.

If you want a challenge where the data can only be reached through the injection, use the [Flask version](https://github.com/<your-username>/<flask-repo-name>), where all records live in a real SQLite database.

## Skills practised

- Identifying injection points in a black-box application
- Reasoning about query structure without error feedback
- Quote balancing and comment-based truncation
- `UNION`-based data extraction and column-count matching
- Understanding why blocklist filtering is not a real defence
- Recognising why sensitive data must never ship in client-side code

## Defence notes

If this were a real application, the fix is not a better blocklist. Use **parameterised queries / prepared statements**, apply least-privilege database accounts, keep sensitive data on the server, and never store credentials in plaintext.

## Project structure

```
.
├── Ministry of Admissions — The Underworld.html   # the entire challenge (HTML, CSS, JS)
├── README.md
└── LICENSE
```

## Disclaimer

This project is for education and authorised practice only. Don't use the techniques it teaches against systems you don't own or have explicit permission to test.

## License

MIT. See [LICENSE](LICENSE).
