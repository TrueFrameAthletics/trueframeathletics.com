// Validate the committed static website; do not overwrite modern pages with the legacy generator.
import fs from "node:fs";
import path from "node:path";
const root = path.resolve("public");
const pages = ["index","how-it-works","athletes","teams","about","contact"];
let errors = [];
for (const name of pages) {
  const file = path.join(root, name + ".html");
  if (!fs.existsSync(file)) { errors.push("Missing " + file); continue; }
  const html=fs.readFileSync(file,"utf8");
  if (!html.includes('href="/styles.css')) errors.push(file + ": no stylesheet");
  for (const match of html.matchAll(/href="(\/[A-Za-z][A-Za-z0-9-]*)(?:#[^"]*)?"/g)) {
    const url=match[1];
    if (url==="/") continue;
    if (!fs.existsSync(path.join(root, url.slice(1)+".html")) && !fs.existsSync(path.join(root,url.slice(1))))
      errors.push(file + ": broken link " + url);
  }
}
if(!fs.existsSync(path.join(root,"styles.css"))) errors.push("Missing styles.css");
if(errors.length) { console.error(errors.join("\n")); process.exitCode=1; }
else console.log("Verified primary TrueFrame pages and linked assets. Existing published HTML unchanged.");
