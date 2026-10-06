#!/usr/bin/env python3
"""Builds the TrueFrame Athletics HTML pages into ../public.

Edit page content in this file, then run:  python3 tools/build.py
styles.css and the logo SVGs live in public/ and are edited directly.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(HERE, "..", "public")
EMAIL = "info@trueframeathletics.com"
SITE = "https://trueframeathletics.com"

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("schools-teams.html", "Teams & Schools"),
    ("athletes-parents.html", "Athletes & Parents"),
    ("contact.html", "Contact"),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Space+Grotesk:wght@500;700&display=swap">')

def header(active):
    """Renders the site header with nav. active = filename of current page."""
    nav_links = "".join(
        f'<li><a href="/{link.replace(".html", "") if link != "index.html" else ""}"'
        f'{' aria-current="page"' if link == active else ""}>{label}</a></li>'
        for link, label in NAV
    )
    return f"""<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="/" aria-label="TrueFrame Athletics home"><img src="/logo-mark.svg" alt="" width="46" height="39"><span class="brand-text"><span class="brand-name">TrueFrame</span><span class="brand-sub">Athletics</span></span></a>
    <button class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="nav-menu">Menu</button>
    <nav class="nav-menu" id="nav-menu" aria-label="Main">
      <ul class="nav-links">{nav_links}</ul>
      <a class="btn btn-primary nav-cta" href="/contact">Get Started</a>
    </nav>
  </div>
</header>"""

def footer():
    """Renders the site footer."""
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="/" aria-label="TrueFrame Athletics home"><img src="/logo-mark-dark.svg" alt="" width="46" height="39"><span class="brand-text"><span class="brand-name">TrueFrame</span><span class="brand-sub">Athletics</span></span></a>
        <p class="foot-tag">Mental Performance & Adversity Response. Helping athletes across sports reset, refocus, and respond.</p>
      </div>
      <div class="foot-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="/about">About</a></li>
          <li><a href="/services">Services</a></li>
          <li><a href="/schools-teams">Teams & Schools</a></li>
          <li><a href="/athletes-parents">Athletes & Parents</a></li>
        </ul>
      </div>
      <div class="foot-col">
        <h4>Get started</h4>
        <ul>
          <li><a href="/contact">Get Started</a></li>
          <li><span>{EMAIL}</span></li>
        </ul>
      </div>
    </div>
  </div>
</footer>"""

def meta(title, description, url_path="/"):
    """Returns <head> metadata."""
    og_url = SITE + (url_path if url_path.startswith("/") else "/" + url_path)
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{og_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{og_url}">
<meta name="theme-color" content="#111111">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="/styles.css">"""

def page(title, description, active, url_path, body):
    """Wraps body in full HTML page structure."""
    return f"""<!doctype html>
<html lang="en">
<head>
{meta(title, description, url_path)}
</head>
<body>
{header(active)}
<main id="main-content">
{body}
</main>
{footer()}
<script src="/worker.js"></script>
</body>
</html>"""

def main():
    """Build all pages."""
    os.makedirs(PUBLIC, exist_ok=True)

    # HOME PAGE
    home_body = """<section class="page-hero on-dark">
  <div class="wrap">
    <span class="eyebrow">Mental Performance Coaching</span>
    <h1>Own the Moment.</h1>
    <p class="lede">Reset. Refocus. Respond. Help your athletes build mental resilience and execute under pressure.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="/contact">Get Started</a>
      <a class="btn btn-ghost" href="/about">Learn More <span class="arr">→</span></a>
    </div>
    <div class="corner vf" aria-hidden="true"></div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <h2>For Athletes & Parents</h2>
    <p class="lede">Build mental skills that transfer across sports and life.</p>
    <div class="btn-row">
      <a class="btn btn-dark" href="/athletes-parents">Explore <span class="arr">→</span></a>
    </div>
  </div>
</section>

<section class="section on-light">
  <div class="wrap">
    <h2>For Schools & Teams</h2>
    <p class="lede">Develop team-wide mental performance and resilience.</p>
    <div class="btn-row">
      <a class="btn btn-dark" href="/schools-teams">Learn More <span class="arr">→</span></a>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap cta-inner">
    <div><h2>Ready to own the moment?</h2><p>Start your mental performance journey today.</p></div>
    <div class="btn-row">
      <a class="btn btn-dark" href="/contact">Get Started <span class="arr">→</span></a>
    </div>
  </div>
</section>"""
    
    with open(os.path.join(PUBLIC, "index.html"), "w") as f:
        f.write(page(
            "TrueFrame Athletics | Mental Performance Coaching",
            "Mental performance coaching for athletes. Reset, refocus, and respond under pressure.",
            "index.html", "/", home_body
        ))
    print("✓ index.html")

    # ABOUT PAGE
    about_body = """<section class="page-hero on-dark">
  <div class="wrap">
    <span class="eyebrow">About TrueFrame</span>
    <h1>Meet Richard Cooks</h1>
    <p class="lede">Founder & Mental Performance Coach at TrueFrame Athletics</p>
    <div class="corner vf" aria-hidden="true"></div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <div class="prose">
      <h2>Richard Cooks — Founder &amp; Mental Performance Coach</h2>
      <p>Richard Cooks holds a degree in psychology and a master’s degree in industrial-organizational psychology. His background combines coaching, athlete development, and healthcare operations. In his role as a customer service supervisor, he coaches employees, supports performance improvement, handles complex situations, and helps people respond constructively under pressure.</p>
      <p>Richard has also supported soldiers as they prepared for overseas assignments. That experience informs his interest in preparation, focus, and responses to uncertainty. Through TrueFrame, he helps athletes practice responses to mistakes, pressure, confidence loss, role changes, and adversity.</p>
    </div>
  </div>
</section>

<section class="section on-light">
  <div class="wrap">
    <div class="prose">
      <h2>The TrueFrame Approach</h2>
      <p>Competition creates pressure, mistakes, expectations, adversity, frustration, and uncertainty. Those moments can affect even skilled athletes. TrueFrame helps athletes develop better responses to those moments through practical coaching and film analysis.</p>
      <p><strong>Note:</strong> TrueFrame Athletics provides performance coaching and athlete development; it does not provide therapy or clinical mental-health treatment.</p>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap cta-inner">
    <div><h2>Learn more about how TrueFrame helps athletes.</h2><p>Explore our services and approach.</p></div>
    <div class="btn-row">
      <a class="btn btn-dark" href="/services">Services <span class="arr">→</span></a>
    </div>
  </div>
</section>"""
    
    with open(os.path.join(PUBLIC, "about.html"), "w") as f:
        f.write(page(
            "About Richard Cooks | TrueFrame Athletics",
            "Meet Richard Cooks, founder of TrueFrame Athletics, bringing psychology education, leadership, and athlete-development experience to mental performance coaching.",
            "about.html", "/about", about_body
        ))
    print("✓ about.html")

    # SERVICES PAGE
    services_body = """<section class="page-hero on-dark">
  <div class="wrap">
    <span class="eyebrow">What We Offer</span>
    <h1>Mental Performance Services</h1>
    <p class="lede">Coaching, film analysis, and athlete development for individual athletes and teams.</p>
    <div class="corner vf" aria-hidden="true"></div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <div class="prose">
      <h2>Individual Athlete Coaching</h2>
      <p>One-on-one mental performance coaching using the FRAME system: recognizing competitive challenges, resetting with practical routines, refocusing attention, reflecting on responses, and executing the next opportunity.</p>
      <p>Sessions include film review when footage is available to pair athlete perspective with objective observation.</p>
    </div>
  </div>
</section>

<section class="section on-light">
  <div class="wrap">
    <div class="prose">
      <h2>Team & School Programs</h2>
      <p>Develop team-wide mental resilience and performance through workshops, coaching, and film analysis. Programs can be customized for sports, age groups, and specific competitive challenges.</p>
    </div>
  </div>
</section>

<section class="section on-dark">
  <div class="wrap">
    <div class="prose">
      <h2>Film Analysis & Review</h2>
      <p>Detailed competition film review that identifies key moments, decisions, and responses. Observations support coaching conversations and help athletes see their performance from a different angle.</p>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap cta-inner">
    <div><h2>Ready to get started?</h2><p>Contact us to discuss your mental performance goals.</p></div>
    <div class="btn-row">
      <a class="btn btn-dark" href="/contact">Get Started <span class="arr">→</span></a>
    </div>
  </div>
</section>"""
    
    with open(os.path.join(PUBLIC, "services.html"), "w") as f:
        f.write(page(
            "Services | TrueFrame Athletics",
            "Mental performance coaching, film analysis, and athlete development services for individual athletes and teams.",
            "services.html", "/services", services_body
        ))
    print("✓ services.html")

    # SCHOOLS & TEAMS PAGE
    teams_body = """<section class="page-hero on-dark">
  <div class="wrap">
    <span class="eyebrow">For Schools & Teams</span>
    <h1>Build Team Mental Resilience</h1>
    <p class="lede">Develop competitive mental performance across your team or program.</p>
    <div class="corner vf" aria-hidden="true"></div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <div class="prose">
      <p>Team mental performance creates competitive advantage. When athletes share language, strategies, and practices for handling pressure, mistakes, and adversity, your program becomes stronger.</p>
      <p>TrueFrame works with schools and teams to build team-wide mental performance culture and develop consistent reset and refocus routines.</p>
    </div>
  </div>
</section>

<section class="section on-light">
  <div class="wrap">
    <div class="prose">
      <h2>Programs Include</h2>
      <ul style="margin-left: 20px;">
        <li><strong>Team workshops</strong> on mental performance fundamentals</li>
        <li><strong>Individual athlete coaching</strong> for key players</li>
        <li><strong>Film analysis sessions</strong> to reinforce team concepts</li>
        <li><strong>Coaching staff consultation</strong> to integrate mental performance into team training</li>
      </ul>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap cta-inner">
    <div><h2>Interested in a team program?</h2><p>Let's discuss how TrueFrame can support your program.</p></div>
    <div class="btn-row">
      <a class="btn btn-dark" href="/contact">Contact Us <span class="arr">→</span></a>
    </div>
  </div>
</section>"""
    
    with open(os.path.join(PUBLIC, "schools-teams.html"), "w") as f:
        f.write(page(
            "Schools & Teams | TrueFrame Athletics",
            "Mental performance programs for school teams and sports programs. Build team-wide resilience and competitive advantage.",
            "schools-teams.html", "/schools-teams", teams_body
        ))
    print("✓ schools-teams.html")

    # ATHLETES & PARENTS PAGE
    athletes_body = """<section class="page-hero on-dark">
  <div class="wrap">
    <span class="eyebrow">For Athletes & Parents</span>
    <h1>Develop Mental Performance</h1>
    <p class="lede">Mental skills training for individual athletes ready to own the moment.</p>
    <div class="corner vf" aria-hidden="true"></div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <div class="prose">
      <p>Every athlete faces moments that test their mental strength: mistakes, pressure, setbacks, confidence loss, and unexpected changes. TrueFrame helps athletes build practical responses to those moments through one-on-one coaching, film analysis, and sport-specific strategies.</p>
    </div>
  </div>
</section>

<section class="section on-light">
  <div class="wrap">
    <div class="prose">
      <h2>How It Works</h2>
      <p><strong>The FRAME System:</strong></p>
      <ul style="margin-left: 20px;">
        <li><strong>F</strong>ocus — Recognize what is happening</li>
        <li><strong>R</strong>eset — Use practical routines to refocus</li>
        <li><strong>A</strong>ttention — Direct focus to the next opportunity</li>
        <li><strong>M</strong>anage — Apply sport-specific competitive strategies</li>
        <li><strong>E</strong>xecute — Trust your preparation and perform</li>
      </ul>
      <p style="margin-top: 24px;">Sessions include film review when available to pair your perspective with objective observation of your performance.</p>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap cta-inner">
    <div><h2>Ready to start?</h2><p>Get in touch to learn how TrueFrame can help your athlete.</p></div>
    <div class="btn-row">
      <a class="btn btn-dark" href="/contact">Get Started <span class="arr">→</span></a>
    </div>
  </div>
</section>"""
    
    with open(os.path.join(PUBLIC, "athletes-parents.html"), "w") as f:
        f.write(page(
            "Athletes & Parents | TrueFrame Athletics",
            "Mental performance coaching for individual athletes. Build mental resilience, reset under pressure, and execute with confidence.",
            "athletes-parents.html", "/athletes-parents", athletes_body
        ))
    print("✓ athletes-parents.html")

    # CONTACT PAGE
    contact_body = f"""<section class="page-hero on-dark">
  <div class="wrap">
    <span class="eyebrow">Get Started</span>
    <h1>Let's Connect</h1>
    <p class="lede">Interested in mental performance coaching? Reach out to discuss your goals.</p>
    <div class="corner vf" aria-hidden="true"></div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <div class="prose" style="max-width: 600px;">
      <h2>Contact Information</h2>
      <p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p><strong>Location:</strong> Available for individual and team coaching</p>
      <p style="margin-top: 32px;">Whether you're an athlete, parent, coach, or school administrator, we'd love to hear about your mental performance goals. Drop us a message and we'll get back to you soon.</p>
    </div>
  </div>
</section>

<section class="section on-light">
  <div class="wrap">
    <div class="prose">
      <h2>What to Expect</h2>
      <ul style="margin-left: 20px;">
        <li>We'll discuss your specific goals and challenges</li>
        <li>Learn about the FRAME system and coaching approach</li>
        <li>Explore how coaching can support your athlete or team</li>
        <li>Schedule an initial session if it's a good fit</li>
      </ul>
    </div>
  </div>
</section>"""
    
    with open(os.path.join(PUBLIC, "contact.html"), "w") as f:
        f.write(page(
            "Contact | TrueFrame Athletics",
            "Get in touch with TrueFrame Athletics. Email us about mental performance coaching for athletes or teams.",
            "contact.html", "/contact", contact_body
        ))
    print("✓ contact.html")

    # 404 PAGE
    not_found_body = """<section class="page-hero on-dark">
  <div class="wrap">
    <div class="corner vf" aria-hidden="true"></div>
    <span class="eyebrow">404 · Page Not Found</span>
    <h1>Out of Frame</h1>
    <p class="lede">The page you're looking for moved or doesn't exist. Let's get you back on track.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="/">Back to Home</a>
      <a class="btn btn-ghost" href="/contact">Contact Us <span class="arr">→</span></a>
    </div>
  </div>
</section>"""
    
    with open(os.path.join(PUBLIC, "404.html"), "w") as f:
        f.write(page(
            "Page Not Found | TrueFrame Athletics",
            "The page you're looking for doesn't exist. Return to TrueFrame Athletics home.",
            "404.html", "/404", not_found_body
        ))
    print("✓ 404.html")

    print("\n✓ All pages built successfully!")

if __name__ == "__main__":
    main()
