# TrueFrame Athletics — trueframeathletics.com

A static site served by Cloudflare Workers (Static Assets), plus a small Worker that handles the contact form.

```
public/          the website (HTML, CSS, logos, _headers, 404.html)
src/worker.js    handles POST /api/contact; everything else is served from public/
tools/build.py   generates the 6 HTML pages in public/ (edit page copy here)
wrangler.jsonc   Worker, assets, domain, and email config
```

## Editing
- **Page copy:** edit `tools/build.py`, then run `python3 tools/build.py` (or `npm run build`) and commit the regenerated `public/*.html`.
- **Styles / logo:** edit `public/styles.css` and `public/logo-mark.svg` directly. (`logo-mark-dark.svg` is regenerated from `logo-mark.svg` by the build.)
- **Contact email shown on the site:** `EMAIL` at the top of `tools/build.py`.

## Local dev
```
npm install
npm run dev        # http://localhost:8787 — contact form emails are written to .wrangler/tmp as .eml files
```

## One-time Cloudflare setup
1. **Email Routing:** Dashboard → trueframeathletics.com → Email → Email Routing → enable, and add + verify the inbox that should receive form submissions as a destination address.
2. **Config:** in `wrangler.jsonc`, replace both `REPLACE_WITH_YOUR_INBOX@example.com` values with that verified address. `CONTACT_FROM` (`website@trueframeathletics.com`) needs no mailbox; it only has to be on the domain.
3. **Deploy from GitHub:** Workers & Pages → Create → Import a repository → pick this repo.
   - Build command: *(leave empty; the HTML is committed)*
   - Deploy command: `npx wrangler deploy`
4. **Domain:** `routes` in `wrangler.jsonc` attaches trueframeathletics.com and www as custom domains on deploy. The zone must be on the same Cloudflare account. Remove any existing DNS records for the apex/www that conflict.

Optional: create a KV namespace and uncomment `kv_namespaces` in `wrangler.jsonc` to keep a copy of every submission.

## Contact form behavior
- Validates name, email, role; hidden honeypot field drops bot submissions silently.
- Rejects cross-origin posts.
- On failure, the page tells the visitor to email directly.
