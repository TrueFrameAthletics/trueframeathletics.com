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
        <p class="foot-tag">Own the Moment. Mental Performance &amp; Adversity Response for athletes who want a repeatable response when competition gets hard.</p>
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
    <span class="eyebrow">Mental Performance &amp; Adversity Response</span>
    <h1>Own the Moment.</h1>
    <p class="lede">When pressure rises, mistakes happen, or confidence drops, athletes need more than motivation. TrueFrame builds repeatable responses athletes can use in real competition.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="/contact">Get Started</a>
      <a class="btn btn-ghost" href="/about">Learn More <span class="arr">→</span></a>
    </div>
    <div class="corner vf" aria-hidden="true"></div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <div class="prose">
      <span class="eyebrow">The TrueFrame Difference</span>
      <h2>What does it mean to Own the Moment?</h2>
      <p>It means having a trained response when the game gets difficult. TrueFrame helps athletes recognize the moment, reset after mistakes, refocus on what they can control, and execute the next play with purpose.</p>
      <p><strong>FRAME is the system. Own the Moment is the result.</strong></p>
    </div>
  </div>
</section>

<section class="section on-light">
  <div class="wrap">
    <h2>For Athletes &amp; Parents</h2>
    <p class="lede">One-on-one coaching that helps athletes own pressure, mistakes, confidence swings, role changes, and adversity.</p>
    <div class="btn-row">
      <a class="btn btn-dark" href="/athletes-parents">Explore Athlete Coaching <span class="arr">→</span></a>
    </div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <h2>For Schools &amp; Teams</h2>
    <p class="lede">Bring a shared mental-performance language and repeatable reset system to your entire program.</p>
    <div class="btn-row">
      <a class="btn btn-dark" href="/schools-teams">Explore Own the Moment for Teams <span class="arr">→</span></a>
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
            "Own the Moment with practical mental performance and adversity-response coaching for athletes, teams, schools, and families.",
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
      <h2>About Richard Cooks</h2>
      <p>Richard Cooks holds a degree in psychology and a master's degree in industrial-organizational psychology. His background combines coaching, athlete development, and performance leadership. Professionally, he works in performance leadership, where he coaches and develops employees, supports performance improvement, navigates complex situations, and helps people remain effective under pressure.</p>
      <p>Richard has also supported soldiers as they prepared for overseas assignments. That experience informs his interest in preparation, focus, and responses to uncertainty. Through TrueFrame, he helps athletes practice responses to mistakes, pressure, confidence loss, role changes, and adversity.</p>
    </div>
  </div>
</section>

<section class="section on-light">
  <div class="wrap">
    <div class="prose">
      <h2>Why “Own the Moment”</h2>
      <p>Competition creates pressure, mistakes, expectations, adversity, frustration, and uncertainty. Athletes cannot always control the moment, but they can train their response to it. That is the idea behind Own the Moment.</p>
      <p>TrueFrame uses practical coaching, the FRAME system, and competition film to help athletes recognize difficult moments, reset faster, refocus attention, and respond with purpose.</p>
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
    <h1>Train the Response. Own the Moment.</h1>
    <p class="lede">Practical mental-performance coaching, adversity-response training, and film analysis for athletes and teams.</p>
    <div class="corner vf" aria-hidden="true"></div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <div class="prose">
      <h2>Own the Moment — Individual Athlete Coaching</h2>
      <p>One-on-one coaching helps athletes build a repeatable response to mistakes, pressure, confidence loss, role changes, adversity, and high-stakes competition. The FRAME system gives athletes practical tools they can use in the moment instead of relying only on motivational messaging.</p>
      <p>Sessions include film review when footage is available to pair athlete perspective with objective observation.</p>
    </div>
  </div>
</section>

<section class="section on-light">
  <div class="wrap">
    <div class="prose">
      <h2>Own the Moment — Team &amp; School Programs</h2>
      <p>Build a shared mental-performance language across your program through workshops, coaching, and practical reset routines. Programs can be customized by sport, age group, and the competitive challenges your athletes face most often.</p>
    </div>
  </div>
</section>

<section class="section on-dark">
  <div class="wrap">
    <div class="prose">
      <h2>Film-to-Response Analysis</h2>
      <p>Competition film is used to identify pressure moments, mistakes, body-language changes, decision patterns, recovery speed, and response behaviors. The goal is not just to review what happened, but to train what the athlete does next.</p>
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
    <h1>Bring Own the Moment to Your Program</h1>
    <p class="lede">Give athletes a shared system for responding to pressure, mistakes, adversity, and high-stakes competition.</p>
    <div class="corner vf" aria-hidden="true"></div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <div class="prose">
      <p>Own the Moment gives coaches and athletes a common language for what happens when competition gets difficult. Instead of simply telling athletes to “be confident” or “move on,” TrueFrame teaches repeatable responses they can practice and use.</p>
      <p>Through the FRAME system, athletes learn how to reset after mistakes, regain focus, manage adversity, communicate under pressure, and execute the next opportunity.</p>
    </div>
  </div>
</section>

<section class="section on-light">
  <div class="wrap">
    <div class="prose">
      <h2>Own the Moment Team Program</h2>
      <ul style="margin-left: 20px;">
        <li><strong>Baseline athlete and coach assessment</strong> to identify current challenges and pressure points</li>
        <li><strong>Team mental-performance sessions</strong> focused on mistakes, pressure, confidence, controllables, and adversity</li>
        <li><strong>FRAME reset tools</strong> athletes can use during practice and competition</li>
        <li><strong>Film-to-response review</strong> when footage is available</li>
        <li><strong>Coach consultation</strong> to reinforce the language and tools after sessions</li>
        <li><strong>Post-program feedback</strong> to identify progress and next steps</li>
      </ul>
      <p style="margin-top: 24px;"><strong>Founding School Pilot:</strong> A focused entry program for schools that want to introduce the Own the Moment approach before expanding it across a season or athletic department.</p>
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
    <h1>Own the Moment When It Gets Hard</h1>
    <p class="lede">Train the response you want when pressure rises, mistakes happen, or confidence starts to slip.</p>
    <div class="corner vf" aria-hidden="true"></div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <div class="prose">
      <p>Every athlete faces moments that test them: mistakes, pressure, setbacks, confidence loss, role changes, bad calls, and unexpected adversity. TrueFrame helps athletes train what happens next through one-on-one coaching, competition film, and practical mental-performance tools.</p>
      <p>The goal is simple: <strong>recognize the moment, reset, refocus, and respond.</strong></p>
    </div>
  </div>
</section>

<section class="section on-light">
  <div class="wrap">
    <div class="prose">
      <h2>The FRAME System</h2>
      <p><strong>FRAME is the method athletes use to Own the Moment:</strong></p>
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
    <h1>Ready to Own the Moment?</h1>
    <p class="lede">Tell us what your athlete or team is facing, and we’ll talk through the next step.</p>
    <div class="corner vf" aria-hidden="true"></div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <div class="prose" style="max-width: 600px;">
      <h2>Contact Information</h2>
      <p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p><strong>Location:</strong> Available for individual and team coaching</p>
      <p style="margin-top: 32px;">Whether you're an athlete, parent, coach, or school administrator, tell us where performance tends to break down: mistakes, pressure, confidence, adversity, role changes, or another challenge. We’ll help you decide whether TrueFrame is a good fit.</p>
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
