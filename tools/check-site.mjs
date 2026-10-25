// Read-only validation of the static site in ./public: internal links, anchors, assets,
// SEO tags, sitemap and redirects. It never regenerates pages (tools/build.py is the legacy
// generator and would overwrite the modern pages, so it is not part of this check).
import fs from "node:fs";
import path from "node:path";

const root = path.resolve("public");
const ORIGIN = "https://trueframeathletics.com";
const RETIRED_COPY = ["Perform When It Gets Hard", "Launching with basketball"];
const errors = [];
const warnings = [];
const fail = (where, msg) => errors.push(`${where}: ${msg}`);
const warn = (where, msg) => warnings.push(`${where}: ${msg}`);

const isFile = (rel) => {
  const full = path.join(root, rel);
  return full.startsWith(root) && fs.existsSync(full) && fs.statSync(full).isFile();
};
const read = (rel) => fs.readFileSync(path.join(root, rel), "utf8");

// Map a URL path to a file in ./public the way Workers Static Assets serves it.
function resolvePath(pathname) {
  if (pathname === "/") return "index.html";
  let rel;
  try { rel = decodeURIComponent(pathname.slice(1)); } catch { return null; }
  if (isFile(rel)) return rel;
  if (isFile(rel + ".html")) return rel + ".html";
  return null;
}

const redirects = new Map();
if (isFile("_redirects")) {
  for (const line of read("_redirects").split(/\r?\n/)) {
    const [from, to] = line.trim().split(/\s+/);
    if (!from || from.startsWith("#")) continue;
    if (!to) { fail("_redirects", `malformed line "${line.trim()}"`); continue; }
    redirects.set(from, to);
    if (!resolvePath(new URL(to, ORIGIN).pathname)) fail("_redirects", `${from} -> ${to} does not resolve`);
  }
}

const pages = fs.readdirSync(root).filter((f) => f.endsWith(".html")).sort();
const ids = new Map(pages.map((p) => [p, new Set([...read(p).matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]))]));
const titles = new Map();
const descriptions = new Map();
const cssVersions = new Map();
const noindex = new Set();
const group = (map, key, page) => map.set(key, [...(map.get(key) ?? []), page]);
const attrOf = (tag, name) => tag.match(new RegExp(`\\b${name}="([^"]*)"`, "i"))?.[1];
const tagOf = (html, re) => html.match(re)?.[0] ?? "";

for (const page of pages) {
  const html = read(page);
  const slug = page.replace(/\.html$/, "");
  const base = page === "index.html" ? `${ORIGIN}/` : `${ORIGIN}/${slug}`;

  const css = html.match(/href="\/styles\.css(\?v=[^"]*)?"/);
  if (!css) fail(page, "no stylesheet link");
  else group(cssVersions, css[1] ?? "(none)", page);

  for (const [, kind, ref] of html.matchAll(/\b(href|src)="([^"]*)"/g)) {
    if (/^([a-z][a-z0-9+.-]*:|\/\/)/i.test(ref)) continue;
    const url = new URL(ref, base);
    const target = resolvePath(url.pathname);
    if (!target) {
      if (redirects.has(url.pathname)) warn(page, `${kind} ${ref} points at a redirected URL`);
      else fail(page, `broken ${kind} ${ref}`);
      continue;
    }
    const anchor = url.hash.slice(1);
    if (anchor && target.endsWith(".html") && !ids.get(target)?.has(decodeURIComponent(anchor)))
      fail(page, `missing anchor ${ref}`);
  }

  const title = html.match(/<title>([^<]*)<\/title>/i)?.[1].trim();
  const desc = attrOf(tagOf(html, /<meta[^>]*name="description"[^>]*>/i), "content")?.trim();
  const indexable = !/<meta[^>]*name="robots"[^>]*noindex/i.test(html);
  if (!indexable) noindex.add(page);
  if (!title) fail(page, "missing <title>");
  else { group(titles, title, page); if (title.length > 70) warn(page, `title is ${title.length} characters`); }
  if (!desc) { if (indexable) fail(page, "missing meta description"); }
  else { group(descriptions, desc, page); if (desc.length < 50 || desc.length > 170) warn(page, `description is ${desc.length} characters`); }

  if (indexable) {
    const canonical = attrOf(tagOf(html, /<link[^>]*rel="canonical"[^>]*>/i), "href");
    const ogUrl = attrOf(tagOf(html, /<meta[^>]*property="og:url"[^>]*>/i), "content");
    if (canonical !== base) fail(page, `canonical is ${canonical}, expected ${base}`);
    if (ogUrl !== base) warn(page, `og:url is ${ogUrl}, expected ${base}`);
  }

  const h1s = (html.match(/<h1[\s>]/gi) ?? []).length;
  if (h1s !== 1) warn(page, `${h1s} <h1> elements`);
  for (const img of html.matchAll(/<img\b[^>]*>/gi)) if (!/\balt=/i.test(img[0])) warn(page, "image without an alt attribute");
  for (const phrase of RETIRED_COPY) if (html.toLowerCase().includes(phrase.toLowerCase())) warn(page, `contains retired copy "${phrase}"`);
}

for (const [text, list] of titles) if (list.length > 1) warn(list.join(", "), `share the title "${text}"`);
for (const [text, list] of descriptions) if (list.length > 1) warn(list.join(", "), "share a meta description");
if (cssVersions.size > 1) warn("styles.css", `cache-busting version differs between pages: ${[...cssVersions].map(([v, p]) => `${v} (${p.join(", ")})`).join("; ")}`);

if (!isFile("sitemap.xml")) fail("sitemap.xml", "missing");
else {
  const listed = new Set();
  for (const [, loc] of read("sitemap.xml").matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)) {
    let url;
    try { url = new URL(loc); } catch { fail("sitemap.xml", `invalid URL ${loc}`); continue; }
    const target = url.origin === ORIGIN ? resolvePath(url.pathname) : null;
    if (!target) fail("sitemap.xml", `${loc} does not resolve to a page`);
    else listed.add(target);
  }
  for (const page of pages) if (!noindex.has(page) && !listed.has(page)) warn("sitemap.xml", `${page} is not listed`);
}

if (!isFile("robots.txt") || !read("robots.txt").includes(`Sitemap: ${ORIGIN}/sitemap.xml`)) warn("robots.txt", "does not point to the sitemap");

for (const w of warnings) console.warn("warning: " + w);
if (errors.length) {
  console.error(errors.map((e) => "error: " + e).join("\n"));
  process.exitCode = 1;
} else {
  console.log(`Checked ${pages.length} pages: links, anchors, assets, SEO tags, sitemap and redirects.`);
}
