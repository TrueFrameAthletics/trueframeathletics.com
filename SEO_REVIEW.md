# Search visibility update — unpublished review

Prepared November 8, 2026. Based on `site-updates` at `60bbf79`, not the older `main` branch. The live homepage matches the source on this branch after normalizing line endings. No production deployment or merge is authorized by this review.

## Changes
- Added `/mental-toughness-coach-for-coaches`: coach education, practical scenario, FRAME steps, program choices, film limitations, FAQs, and consultation links.
- Added `/mental-performance-coach-omaha`: accurate location context, session arrangements, virtual options, and preparation for a consultation; no invented office address.
- Updated titles and descriptions for eight existing service/identity pages and the two new pages.
- Added Organization, WebSite, WebPage, and founder Person structured data using public business information. No fabricated review ratings or credentials.
- Added contextual links from Home, Programs, and Teams plus footer links; added both pages to the sitemap.
- Preserved permissive robots.txt and made OAI-SearchBot access explicit. This is documentation of intended access, not evidence that Cloudflare permits every crawler request.
- Replaced the homepage's absolute film-verification wording with observational wording.

## Validation
- `npm run build`: all 14 HTML pages pass the existing link, anchor, asset, metadata, sitemap, and redirect checks.
- All 13 indexable pages have parseable JSON-LD with distinct node identifiers within each graph.
- Robots rules allow Googlebot, Bingbot, and OAI-SearchBot on the homepage and new pages.
- `git diff --check` passed.
- Viewed both new pages in the local browser preview and tested a coach-page FAQ disclosure. The static preview uses `.html` URLs; production's existing Cloudflare configuration handles extensionless paths. Production routing and mobile viewport behavior still need deployment-stage verification.

## Account-dependent work still outstanding
- Verify the Cloudflare production source branch before merging or deploying. `main` is older than the live site. This draft targets `site-updates` only.
- Inspect Search Console property ownership, indexing coverage, and sitemap status. After approved publication, submit the updated sitemap/request indexing for the new URLs.
- Review Cloudflare bot/firewall settings for Googlebot and OpenAI's documented OAI-SearchBot access. Do not weaken general protections or disable unrelated crawler rules.
- Verify an eligible Google Business Profile, actual business details, and service area. No listing or reviews were created.
- Connect existing analytics/Search Console data to measure queries, organic inquiries, and ChatGPT referrals. No analytics identifiers or tracking accounts were guessed.
- Collect authentic, permissioned testimonials and real examples as they become available. Existing illustrative report remains labeled.

No ranking or AI recommendation is guaranteed. Draft changes cannot affect search visibility until approved publication and discovery.
