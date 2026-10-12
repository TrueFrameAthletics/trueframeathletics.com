// TrueFrame Athletics — Cloudflare Worker
// Static pages are served from ./public by Workers Static Assets.
// This Worker only runs for /api/* (see run_worker_first in wrangler.jsonc).
import { EmailMessage } from "cloudflare:email";

const MAX = { name: 100, email: 200, phone: 40, role: 60, sport: 60, organization: 120, message: 4000 };

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/contact") {
      if (request.method !== "POST") return json({ ok: false, error: "Method not allowed" }, 405);
      return handleContact(request, env);
    }
    if (url.pathname.startsWith("/api/")) return json({ ok: false, error: "Not found" }, 404);

    return env.ASSETS.fetch(request);
  },
};

async function handleContact(request, env) {
  // Only accept same-site form posts
  const origin = request.headers.get("Origin");
  if (origin && new URL(origin).host !== new URL(request.url).host) {
    return json({ ok: false, error: "Forbidden" }, 403);
  }

  let data;
  try {
    data = await request.json();
  } catch {
    return json({ ok: false, error: "Invalid request" }, 400);
  }

  // Honeypot: bots fill the hidden field. Pretend success, send nothing.
  if (data.company_website) return json({ ok: true });

  const f = {};
  for (const [k, max] of Object.entries(MAX)) f[k] = clean(data[k], max);
  const services = Array.isArray(data.services) ? data.services.slice(0, 10).map((s) => clean(s, 60)).filter(Boolean) : [];

  if (!f.name || !f.role || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email)) {
    return json({ ok: false, error: "Name, a valid email, and role are required." }, 400);
  }

  const subject = `Consultation request: ${f.name} (${f.role}${f.sport ? ", " + f.sport : ""})`;
  const body = [
    `Name: ${f.name}`,
    `Email: ${f.email}`,
    `Phone: ${f.phone || "-"}`,
    `Role: ${f.role}`,
    `Sport: ${f.sport || "-"}`,
    `Organization: ${f.organization || "-"}`,
    `Interested in: ${services.length ? services.join(", ") : "-"}`,
    "",
    "Message:",
    f.message || "-",
    "",
    `Submitted: ${new Date().toISOString()}`,
    `IP country: ${request.cf?.country || "?"}`,
  ].join("\n");

  // Optional: keep a copy of every submission in KV (bind SUBMISSIONS to enable)
  if (env.SUBMISSIONS) {
    const key = `contact:${Date.now()}:${crypto.randomUUID().slice(0, 8)}`;
    await env.SUBMISSIONS.put(key, JSON.stringify({ ...f, services, at: new Date().toISOString() }));
  }

  try {
    const raw = buildMime({
      from: env.CONTACT_FROM,
      fromName: "TrueFrame Website",
      to: env.CONTACT_TO,
      replyTo: f.email,
      subject,
      text: body,
    });
    await env.SEND_EMAIL.send(new EmailMessage(env.CONTACT_FROM, env.CONTACT_TO, raw));
  } catch (err) {
    console.error("send_email failed:", err && err.message);
    // If KV captured it, the lead is not lost; still tell the visitor to email directly.
    return json({ ok: false, error: "Could not send" }, 502);
  }

  return json({ ok: true });
}

function clean(v, max) {
  if (typeof v !== "string") return "";
  return v.replace(/\u0000/g, "").trim().slice(0, max);
}

function header(v) {
  return String(v).replace(/[\r\n]+/g, " ");
}

function b64(str) {
  const bytes = new TextEncoder().encode(str);
  let bin = "";
  for (const b of bytes) bin += String.fromCharCode(b);
  return btoa(bin).replace(/.{1,76}/g, "$&\r\n");
}

function buildMime({ from, fromName, to, replyTo, subject, text }) {
  const encSubject = `=?UTF-8?B?${btoa(String.fromCharCode(...new TextEncoder().encode(header(subject))))}?=`;
  return [
    `From: "${fromName}" <${from}>`,
    `To: <${to}>`,
    `Reply-To: <${header(replyTo)}>`,
    `Subject: ${encSubject}`,
    `Message-ID: <${crypto.randomUUID()}@${from.split("@")[1]}>`,
    `Date: ${new Date().toUTCString()}`,
    "MIME-Version: 1.0",
    'Content-Type: text/plain; charset="UTF-8"',
    "Content-Transfer-Encoding: base64",
    "",
    b64(text),
  ].join("\r\n");
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });
}
