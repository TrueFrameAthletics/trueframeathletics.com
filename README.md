# TrueFrame Athletics — trueframeathletics.com

A static site served by Cloudflare Workers (Static Assets), plus a small Worker that handles the contact form.

```
public/          the website (HTML, CSS, logos, _headers, 404.html)
src/worker.js    handles POST /api/contact; everything else is served from public/
tools/build.py   generates the 6 HTML pages in public/ (edit page copy here)
wrangler.jsonc   Worker, assets, domain, and email config
```

## Editing
- **Page copy:** edit the corresponding file in `public/` directly. The current pages are hand-maintained. `tools/build.py` is an older generator and **will overwrite newer content** if run.\n- **Build safety:** `npm run build` runs `tools/check-site.mjs` to validate the public pages without rewriting them.
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
   - Build command: `npm run build` (validation only; never run the legacy Python generator)
   - Deploy command: `npx wrangler deploy`
4. **Domain:** `routes` in `wrangler.jsonc` attaches trueframeathletics.com and www as custom domains on deploy. The zone must be on the same Cloudflare account. Remove any existing DNS records for the apex/www that conflict.

Optional: create a KV namespace and uncomment `kv_namespaces` in `wrangler.jsonc` to keep a copy of every submission.

## Contact form behavior
- Validates name, email, role; hidden honeypot field drops bot submissions silently.
- Rejects cross-origin posts.
- On failure, the page tells the visitor to email directly.

## Production deployment troubleshooting (Oct 2026)
- In Cloudflare **Workers & Pages → trueframe-athletics → Settings → Build**, set the production branch to `main`, build command to `npm run build`, and **Deploy command** to `npx wrangler deploy` (not `npx wrangler preview`). The latter is for preview branches and can fail without dedicated `previews` bindings.
- Static website files are deployed from `./public` as declared in `wrangler.jsonc`. HTML routes `/how-it-works`, `/athletes`, `/teams`, `/about`, and `/contact` require matching files in `public`.
- After successful deploy, inspect the actual custom domain, reload on mobile, and verify `/styles.css`, `/how-it-works`, and `/contact` are served. The contact form also requires a verified Cloudflare Email Routing destination.
- Preview builds are optional. If enabled, create separate preview variables/bindings in `wrangler.jsonc` or disable preview builds. Do not use the production email address for test submissions.
