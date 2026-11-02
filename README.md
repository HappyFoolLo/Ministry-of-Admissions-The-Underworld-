# Ministry of Admissions: The Underworld

A small, self-contained web challenge for practising **SQL injection** in a safe environment. The theme is Greek mythology: you're poking at the registry of the condemned, run by the Underworld's Division of Records.

> **This is a simulation.** There is no backend and no real database. All "queries" are interpreted by a few lines of client-side JavaScript, and every name, code, and credential in the data is fictional. Nothing here can touch a real system.

## Run it

It's a single static file with no build step and no dependencies.

**Locally:** open `index.html` in any modern browser.

**On GitHub Pages:**
1. Push this repo to GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, select `main` and `/ (root)`, then save.
4. Your challenge will be live at `https://<your-username>.github.io/<repo-name>/`.

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

## Skills practised

- Identifying injection points in a black-box application
- Reasoning about query structure without error feedback
- Quote balancing and comment-based truncation
- `UNION`-based data extraction and column-count matching
- Understanding why blocklist filtering is not a real defence

## Defence notes

If this were a real application, the fix is not a better blocklist. Use **parameterised queries / prepared statements**, apply least-privilege database accounts, and never store credentials in plaintext.

## Project structure

```
.
├── index.html   # the entire challenge (HTML, CSS, JS)
├── README.md
└── LICENSE
```

## Disclaimer

This project is for education and authorised practice only. Don't use the techniques it teaches against systems you don't own or have explicit permission to test.

## License

MIT. See [LICENSE](LICENSE).
