# Antzen & Irene — Okinawa Wedding Site

Two pages:

- **`index.html`** — public guest page. Schedule, packing checklist, weather, RSVP link. Safe for anyone to see.
- **`planner.html`** — private planning dashboard (budget, guest tracking, vendor decisions) for the two of you and your coordinators. Content is AES-encrypted inside the file itself and only decrypts in the browser with the right password.

## Important: what the password protection actually does

GitHub Pages sites are public URLs — there's no login wall a static site can put in front of a page. `planner.html` handles this by never storing the real content in the file as plain text: the budget/guest data is encrypted, and the password you type in the browser derives the decryption key on the spot.

That means anyone without the password sees an empty lock screen, not the data. But it's not bank-grade security — someone who really wanted to could try to brute-force the encrypted file offline. Don't put anything on this site you'd be in serious trouble over if someone determined eventually cracked it. For a family wedding site, this is a reasonable, real deterrent — just go in with eyes open about what it is and isn't.

## Folder layout

```
index.html              ← public guest page, deployed as-is
planner.html            ← private page, deployed as-is (content inside is encrypted)
planner-source/         ← NOT committed to git (see .gitignore) — the plaintext you edit
  panels.html           ← the actual dashboard content, in plain HTML
  shell_template.html   ← the page frame (header, nav, CSS, password-gate logic)
scripts/
  encrypt_planner.py    ← regenerates planner.html from planner-source/
```

`planner-source/` is gitignored on purpose — it's the only place the plaintext budget/guest data exists, and it should never reach GitHub. Keep a personal backup of that folder somewhere private (not a public repo) since it's your only editable copy going forward.

## First-time setup

1. Create a new repository on GitHub (public is fine — the private data never leaves your machine in plain text).
2. From this folder:
   ```bash
   git init
   git add index.html planner.html scripts README.md .gitignore
   git commit -m "Initial wedding site"
   git branch -M main
   git remote add origin https://github.com/achuyo/irene-antzen-wedding.git
   git push -u origin main
   ```
3. On GitHub: **Settings → Pages → Source → Deploy from a branch → `main` / `(root)`** → Save.
4. Your site goes live at `https://achuyo.github.io/irene-antzen-wedding/` (guest page) and `.../planner.html` (private page) within a minute or two.

## The planner password

The current password isn't stored in this repo (that would defeat the encryption). Check your own notes/password manager for it, or generate a new one — see below.

If you ever want to change it, run:

```bash
pip install cryptography   # once, if you don't already have it
python3 scripts/encrypt_planner.py
```

It'll prompt you for a new password (typed, not shown on screen), then rewrite `planner.html`. Commit and push just that one file:

```bash
git add planner.html
git commit -m "Rotate planner password"
git push
```

## Updating the content later

- **Guest page changes** (schedule, checklist, weather): edit `index.html` directly, commit, push.
- **Planner changes** (budget, guest list, decisions): edit `planner-source/panels.html` (plain HTML, not encrypted), then re-run `python3 scripts/encrypt_planner.py` to rebuild `planner.html`, then commit and push `planner.html` only. Never commit anything from `planner-source/`.

## Linking the two pages

`index.html` doesn't link to `planner.html` anywhere, on purpose — it's not indexed or advertised, just reachable if you know the URL. Bookmark `https://achuyo.github.io/irene-antzen-wedding/planner.html` for the two of you.
