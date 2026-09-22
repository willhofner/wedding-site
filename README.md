# We're Getting Married 💍

A one-page spoof wedding site: a wall of photos drifting sideways forever, with a very large
announcement on top. Click any photo to blow it up; Esc / tap outside / × drops you back in.

## Files

- `public/index.html` – the whole site (HTML + CSS + JS in one file)
- `public/photos/` – resized photos (`*-grid.jpg` for the wall, `*-full.jpg` for the lightbox)
- `public/photos.json` – the photo list the page loads
- `scripts/prep_photos.py` – regenerates the two folders above from a folder of originals
- `Dockerfile` + `Caddyfile` – tiny static web server so Railway can run it

## Deploy on Railway (GitHub path)

1. Push this folder to a new GitHub repo (private is fine).
2. Railway → **New Project → Deploy from GitHub repo** → pick the repo. Railway sees the
   Dockerfile and builds it. Nothing else to configure.
3. Service → **Settings → Networking → Generate Domain** to get a `*.up.railway.app` URL and
   confirm it works.
4. Still under **Networking → Custom Domain**, add each of your three domains. Railway shows you
   a CNAME target for each one (something like `abc123.up.railway.app`).

## Point the Namecheap domains at it

For **each** domain, in Namecheap → Domain List → Manage → **Advanced DNS**, delete the parking
records Namecheap put there and add:

| Type          | Host | Value                                   | TTL       |
|---------------|------|-----------------------------------------|-----------|
| CNAME Record  | www  | *the target Railway gave you*           | Automatic |
| ALIAS Record  | @    | *the same target*                       | Automatic |

Namecheap supports ALIAS at the root, which is what makes `hofners.com` (no www) work.
In Railway, add both `hofners.com` and `www.hofners.com` as custom domains so either form
gets a certificate. Repeat for `willandrigetmarried.com` and `willandriley.com`.

DNS usually propagates in 5–30 minutes; Railway issues the HTTPS certs automatically once it
sees the records.

## Changing things

- **Headline / subline:** edit the `<h1>` and `#sub` text in `public/index.html`.
- **Colors:** the `:root` variables at the top of the `<style>` block.
- **Add or swap photos:** put originals in a folder (e.g. `originals/`), run
  `python3 scripts/prep_photos.py originals` (needs `pip install pillow`), commit, push.
  Railway redeploys on every push.
