#!/usr/bin/env python3
"""Builds the TrueFrame Athletics static site.

Outputs:
  dist/      deployable site (full HTML documents) for trueframeathletics.com
  preview/   same site, with index.html in artifact-page form for the Claude preview
"""
import os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
EMAIL = "info@trueframeathletics.com"   # TODO confirm real inbox
SITE = "https://trueframeathletics.com"

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("schools-teams.html", "Schools &amp; Teams"),
    ("athletes-parents.html", "Athletes &amp; Parents"),
    ("contact.html", "Contact"),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..900'
         '&family=Instrument+Sans:wght@400..700&family=IBM+Plex+Mono:wght@400;500&display=swap">')

BRAND = ('<a class="brand" href="index.html" aria-label="TrueFrame Athletics home">'
         '<img src="logo-mark.svg" alt="" width="46" height="39">'
         '<span class="brand-text"><span class="brand-name">TrueFrame</span>'
         '<span class="brand-sub">ATHLETICS</span></span></a>')

FOOT_BRAND = ('<a class="brand" href="index.html" aria-label="TrueFrame Athletics home">'
              '<img src="logo-mark-dark.svg" alt="" width="46" height="39">'
              '<span class="brand-text"><span class="brand-name">TrueFrame</span>'
              '<span class="brand-sub">ATHLETICS</span></span></a>')


def header(active):
    cur = ' aria-current="page"'
    links = "".join(
        f'<li><a href="{h}"{cur if h == active else ""}>{t}</a></li>' for h, t in NAV)
    return f'''<header class="site-header">
  <div class="wrap nav">
    {BRAND}
    <button class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="nav-menu">Menu</button>
    <nav class="nav-menu" id="nav-menu" aria-label="Main">
      <ul class="nav-links">{links}</ul>
      <a class="btn btn-primary nav-cta" href="contact.html">Schedule a Consultation</a>
    </nav>
  </div>
</header>'''


FOOTER = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        {FOOT_BRAND}
        <p class="foot-tag">Mental performance, film analysis, and athlete development for athletes who want to perform when it gets hard.</p>
      </div>
      <div class="foot-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="schools-teams.html">Schools &amp; Teams</a></li>
          <li><a href="athletes-parents.html">Athletes &amp; Parents</a></li>
        </ul>
      </div>
      <div class="foot-col">
        <h4>Get started</h4>
        <ul>
          <li><a href="contact.html">Schedule a consultation</a></li>
          <li><a href="contact.html">Team &amp; school inquiries</a></li>
          <li><span>{EMAIL}</span></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; <span id="yr">2026</span> TrueFrame Athletics. trueframeathletics.com</span>
      <span class="mono">See the complete player.</span>
    </div>
  </div>
</footer>
<script>
(function(){{
  var t=document.getElementById('nav-toggle'),m=document.getElementById('nav-menu');
  if(t&&m)t.addEventListener('click',function(){{var o=m.classList.toggle('open');t.setAttribute('aria-expanded',o);t.textContent=o?'Close':'Menu';}});
  var y=document.getElementById('yr'); if(y) y.textContent=new Date().getFullYear();
}})();
</script>'''


def cta_band(title="Ready to see the complete player?",
             text="Start with a free consultation. We&rsquo;ll talk through where the athlete or program is today, where things break down under pressure, and which path fits."):
    return f'''<section class="cta-band">
  <div class="wrap cta-inner">
    <div><h2>{title}</h2><p>{text}</p></div>
    <div class="btn-row">
      <a class="btn btn-dark" href="contact.html">Schedule a Consultation <span class="arr">&rarr;</span></a>
    </div>
  </div>
</section>'''


def page_hero(eyebrow, title, lede, extra=""):
    return f'''<section class="page-hero on-dark">
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p class="lede">{lede}</p>
    {extra}
    <div class="corner vf" aria-hidden="true"></div>
  </div>
</section>'''


# ---------------------------------------------------------------- chart
def composure_chart():
    W, H = 560, 290
    x0, x1, y0, y1 = 70, 540, 44, 240     # plot box
    T = 32

    def X(t): return x0 + (x1 - x0) * t / T
    def Y(v): return y1 - (y1 - y0) * v / 100

    before = [(0, 72), (5, 71), (7, 30), (9, 34), (12, 48), (15, 60), (17, 24), (20, 30), (23, 40), (26, 46), (29, 33), (32, 37)]
    after = [(0, 72), (5, 72), (7, 50), (8.5, 64), (10, 73), (15, 74), (17, 56), (18.5, 70), (20, 76), (26, 75), (29, 64), (30.5, 74), (32, 78)]
    events = [(7, "Error"), (17, "Momentum swing"), (29, "Final 2:00")]

    def pts(s): return " ".join(f"{X(t):.1f},{Y(v):.1f}" for t, v in s)

    g = []
    for v in (25, 50, 75, 100):
        g.append(f'<line x1="{x0}" x2="{x1}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#2E2B36" stroke-width="1"/>')
    g.append(f'<line x1="{x0}" x2="{x1}" y1="{y1}" y2="{y1}" stroke="#4A4656" stroke-width="1"/>')
    for t, label in events:
        g.append(f'<line x1="{X(t):.1f}" x2="{X(t):.1f}" y1="{y0 - 6}" y2="{y1}" stroke="#7C3AED" stroke-width="1" stroke-dasharray="3 4" opacity=".8"/>')
        anchor = "end" if t > 26 else "middle"
        dx = 4 if anchor == "end" else 0
        g.append(f'<text x="{X(t) + dx:.1f}" y="{y0 - 14}" text-anchor="{anchor}" fill="#C9B6FB" font-family="IBM Plex Mono, monospace" font-size="10.5" letter-spacing="1">{label.upper()}</text>')
    for t in (0, 8, 16, 24, 32):
        g.append(f'<text x="{X(t):.1f}" y="{y1 + 20}" text-anchor="middle" fill="#8D899A" font-family="IBM Plex Mono, monospace" font-size="10">{t}&#8242;</text>')
    g.append(f'<text x="{x0 - 10}" y="{Y(88):.1f}" text-anchor="end" fill="#8D899A" font-family="IBM Plex Mono, monospace" font-size="10">COMPOSED</text>')
    g.append(f'<text x="{x0 - 10}" y="{Y(12):.1f}" text-anchor="end" fill="#8D899A" font-family="IBM Plex Mono, monospace" font-size="10">RATTLED</text>')
    g.append(f'<text x="{(x0 + x1) / 2:.0f}" y="{H - 4}" text-anchor="middle" fill="#6E6A7B" font-family="IBM Plex Mono, monospace" font-size="9.5" letter-spacing="1.5">GAME MINUTES</text>')
    g.append(f'<polyline points="{pts(before)}" fill="none" stroke="#8D899A" stroke-width="2" stroke-dasharray="5 5" stroke-linejoin="round" stroke-linecap="round"/>')
    area = f"{X(0):.1f},{y1} " + pts(after) + f" {X(T):.1f},{y1}"
    g.append(f'<polygon points="{area}" fill="#7C3AED" opacity=".14"/>')
    g.append(f'<polyline points="{pts(after)}" fill="none" stroke="#A98BF7" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>')
    lt, lv = after[-1]
    g.append(f'<circle cx="{X(lt):.1f}" cy="{Y(lv):.1f}" r="5" fill="#A98BF7" stroke="#19181E" stroke-width="2"/>')
    return (f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="chart-t chart-d">'
            f'<title id="chart-t">Composure through a game</title>'
            f'<desc id="chart-d">Illustrative example. After an error, a momentum swing, and the final two minutes, an athlete without a reset routine stays rattled for minutes; with a trained reset routine, composure recovers within a play or two.</desc>'
            + "".join(g) + '</svg>')


# ---------------------------------------------------------------- pages
HOME = f'''
<section class="hero on-dark">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">Mental performance &middot; Film analysis &middot; Athlete development</span>
      <h1>Perform When It Gets <span class="framed-word vf">Hard.</span></h1>
      <p class="lede">TrueFrame Athletics trains the mental side of competition. We help athletes stay confident, composed, and focused through pressure, mistakes, and setbacks, then use game film to prove it&rsquo;s working.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="contact.html">Schedule a Consultation <span class="arr">&rarr;</span></a>
        <a class="btn btn-ghost" href="services.html">Explore Services</a>
      </div>
      <div class="hero-meta mono"><span>Athletes &amp; parents</span><span>Coaches</span><span>High schools &amp; colleges</span><span>Clubs &amp; programs</span></div>
    </div>
    <figure class="film" style="margin:0">
      <div class="film-bar"><span class="rec">Film review</span><span>2nd half &middot; Composure response</span></div>
      <div class="film-screen vf">{composure_chart()}</div>
      <figcaption>
        <div class="film-legend"><span><i></i>No reset routine</span><span><i class="solid"></i>Trained reset routine</span></div>
        <p class="film-note">Illustrative example &middot; how we chart an athlete&rsquo;s response to hard moments</p>
      </figcaption>
    </figure>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <div class="sec-head split">
      <div class="stack"><span class="eyebrow">The moments that decide games</span>
      <h2>Talent shows up in the easy moments. Training shows up in the hard ones.</h2></div>
      <p class="lede">Most athletes practice skills. Very few practice what to do in the thirty seconds after a mistake. That&rsquo;s where games, seasons, and recruiting looks are won or lost.</p>
    </div>
    <div class="moments">
      <div class="moment"><span class="mono">Pressure</span><p>Big games, close scores, crowds, and scouts in the stands.</p></div>
      <div class="moment"><span class="mono">Mistakes</span><p>The error that turns into two more because the reset never came.</p></div>
      <div class="moment"><span class="mono">Confidence drops</span><p>Hesitation, passing up open looks, playing not to lose.</p></div>
      <div class="moment"><span class="mono">Adversity</span><p>A bad call, a hostile environment, a run by the other team.</p></div>
      <div class="moment"><span class="mono">Setbacks</span><p>Injury, lost minutes, a slump, a cut, a rough season.</p></div>
      <div class="moment"><span class="mono">High-stakes play</span><p>Playoffs, showcases, tryouts, and the final two minutes.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">The TrueFrame system</span>
      <h2>Mental performance at the center. Film and development built around it.</h2>
      <p class="lede">Every athlete we work with gets the same three-part approach. We don&rsquo;t guess at what&rsquo;s happening between the ears. We watch for it, name it, and train it.</p>
    </div>
    <div class="system">
      <article class="pillar pillar-core vf">
        <span class="tag">Core &middot; Mental performance</span>
        <h3>Confidence and composure that hold up under pressure.</h3>
        <div class="pillar-body stack">
          <p>We build the mental skills that decide close games: how an athlete prepares, how they talk to themselves, and how fast they recover when something goes wrong.</p>
          <ul class="checks">
            <li>Confidence that doesn&rsquo;t depend on the last play</li>
            <li>Composure and emotional control in high-stress moments</li>
            <li>Focus and attention on the next action</li>
            <li>Reset routines for responding to mistakes</li>
            <li>Resilience through adversity and setbacks</li>
            <li>Pre-competition preparation</li>
          </ul>
        </div>
      </article>
      <article class="pillar">
        <span class="tag">Supports &middot; Film analysis</span>
        <h3>See what actually happens under pressure.</h3>
        <p>Game film shows what stats can&rsquo;t: decision-making, hesitation, body language after a mistake, and the habits that show up when the game speeds up.</p>
      </article>
      <article class="pillar">
        <span class="tag">Supports &middot; Athlete development</span>
        <h3>Turn what we find into measurable change.</h3>
        <p>Every finding becomes specific behaviors, drills, and routines, with clear goals we track from one game to the next.</p>
      </article>
    </div>
  </div>
</section>

<section class="section on-dark">
  <div class="wrap">
    <div class="sec-head">
      <span class="eyebrow">How it works</span>
      <h2>From first film to measurable improvement.</h2>
    </div>
    <div class="steps">
      <div class="step"><h3>Assess</h3><p>We start with an athlete assessment: strengths, gaps, mindset habits, and how they currently respond to pressure.</p></div>
      <div class="step"><h3>Review film</h3><p>We break down game film to see decision-making, hesitation, body language, and pressure responses in real competition.</p></div>
      <div class="step"><h3>Build the plan</h3><p>Findings become a personal development plan with specific goals, routines, and mental-performance work.</p></div>
      <div class="step"><h3>Train &amp; measure</h3><p>Ongoing coaching and follow-up film show what&rsquo;s changing, so progress is visible to athletes, parents, and coaches.</p></div>
    </div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <div class="sec-head split">
      <div class="stack"><span class="eyebrow">Services</span><h2>Six ways to work with TrueFrame.</h2></div>
      <p class="lede">Start with one service or combine them into a full development plan. Every service connects back to mental performance.</p>
    </div>
    <div class="cards">
      <a class="card" href="services.html#mental-performance"><span class="mono">Core</span><h3>Mental Performance Coaching</h3><p>Confidence, focus, handling pressure, recovering from mistakes, adversity, and preparation.</p><span class="more">Learn more &rarr;</span></a>
      <a class="card" href="services.html#assessments"><span class="mono">Start here</span><h3>Athlete Assessments</h3><p>Identify strengths, weaknesses, mindset habits, and the areas that matter most right now.</p><span class="more">Learn more &rarr;</span></a>
      <a class="card" href="services.html#film-review"><span class="mono">Film</span><h3>Film Review &amp; Performance Analysis</h3><p>Game-film breakdowns with feedback on decision-making, performance, and areas to improve.</p><span class="more">Learn more &rarr;</span></a>
      <a class="card" href="services.html#development-plans"><span class="mono">Development</span><h3>Individual Development Plans</h3><p>Personalized goals and action plans built from assessment and film findings.</p><span class="more">Learn more &rarr;</span></a>
      <a class="card" href="services.html#team-programs"><span class="mono">Programs</span><h3>Team &amp; School Programs</h3><p>Mental-performance sessions and season-long programs for teams, coaches, and athletic departments.</p><span class="more">Learn more &rarr;</span></a>
      <a class="card" href="services.html#recruiting"><span class="mono">Next level</span><h3>Recruiting Support</h3><p>Highlight-film review, athlete profiles, and guidance on presenting yourself professionally to coaches.</p><span class="more">Learn more &rarr;</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Who we help</span><h2>Built for the athlete, and everyone invested in them.</h2></div>
    <div class="split2">
      <article class="aud aud-a">
        <div class="who"><span>Athletes</span><span>Parents</span></div>
        <h3>Athletes &amp; Parents</h3>
        <p>For the athlete who plays great in practice and tightens up in games, or who can&rsquo;t shake a bad play. Parents get a clear plan, honest feedback, and visible progress.</p>
        <a class="btn btn-ghost" href="athletes-parents.html">For athletes &amp; parents <span class="arr">&rarr;</span></a>
      </article>
      <article class="aud aud-b on-dark">
        <div class="who"><span>Coaches</span><span>Athletic directors</span><span>High schools</span><span>Colleges</span><span>Clubs</span></div>
        <h3>Schools, Teams &amp; Programs</h3>
        <p>Mental-performance sessions, coach workshops, and season-long programs that give your staff a shared language for pressure, mistakes, and composure.</p>
        <a class="btn btn-ghost" href="schools-teams.html">For schools &amp; teams <span class="arr">&rarr;</span></a>
      </article>
    </div>
  </div>
</section>

<section class="section-tight on-white">
  <div class="wrap sports">
    <div class="stack">
      <span class="eyebrow">Multi-sport</span>
      <h2>One system. Every sport.</h2>
      <p class="lede">Pressure, mistakes, and confidence work the same way on every field, court, mat, and track. We&rsquo;re launching with basketball and building TrueFrame for athletes across sports.</p>
    </div>
    <div class="sport-list">
      <span class="sport first">Basketball <small>Launching first</small></span>
      <span class="sport">Football</span><span class="sport">Volleyball</span><span class="sport">Soccer</span>
      <span class="sport">Baseball</span><span class="sport">Softball</span><span class="sport">Wrestling</span>
      <span class="sport">Track &amp; Field</span><span class="sport">Hockey</span><span class="sport">Tennis</span><span class="sport">Golf</span>
    </div>
  </div>
</section>
{cta_band()}
'''

ABOUT = page_hero("About TrueFrame",
                  'We see the <span class="accent">complete</span> player.',
                  "Physical skill gets an athlete on the floor. How they handle pressure, mistakes, and setbacks decides what they do once they&rsquo;re there. TrueFrame exists to develop that second part on purpose.") + f'''
<section class="section on-white">
  <div class="wrap two-col">
    <div class="stack">
      <span class="eyebrow">Why we exist</span>
      <h2>Most development stops at the physical.</h2>
    </div>
    <div class="prose">
      <p>Athletes spend thousands of hours on shooting, speed, strength, and technique. Almost none of that time goes to what happens when a game gets hard: the missed free throw, the dropped pass, the bad call, the scout in the stands, the slump that won&rsquo;t end.</p>
      <p>That&rsquo;s where talented athletes lose ground. They hesitate. They stop taking the shot. One mistake becomes three. Coaches see it, parents feel it, and the athlete usually can&rsquo;t explain it.</p>
      <p>TrueFrame Athletics treats the mental side of performance as a trainable skill. We use game film to see exactly how an athlete responds under pressure, coach the mental skills that change that response, and turn it into routines they can use in real competition.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Our approach</span><h2>Mental performance first. Proven on film.</h2></div>
    <div class="system">
      <article class="pillar pillar-core vf">
        <span class="tag">01 &middot; Mental performance</span>
        <h3>The center of everything we do.</h3>
        <p class="pillar-body">Confidence, composure, resilience, focus, response to mistakes, and performing under pressure. These are skills, and skills can be coached, practiced, and measured.</p>
      </article>
      <article class="pillar"><span class="tag">02 &middot; Film analysis</span><h3>What the film shows</h3><p>Decision-making, hesitation, body language, pressure responses, and performance habits. Film keeps the work honest and specific.</p></article>
      <article class="pillar"><span class="tag">03 &middot; Athlete development</span><h3>What the athlete does next</h3><p>Specific behaviors, drills, routines, and goals, with measurable improvement from one game to the next.</p></article>
    </div>
  </div>
</section>

<section class="section on-dark">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">The mark</span><h2>What the frame stands for.</h2>
      <p class="lede">The TrueFrame mark is a T and F set inside a camera viewfinder. It describes the work: look closely, then build forward.</p></div>
    <div class="meaning">
      <div><h4>Frame &amp; focus</h4><p>A clearer lens on potential. We look at the whole athlete, on film and off.</p></div>
      <div><h4>T + F monogram</h4><p>TrueFrame Athletics. An honest picture of where an athlete is today.</p></div>
      <div><h4>Progress</h4><p>Forward motion. Every review ends with a next step the athlete can act on.</p></div>
      <div><h4>Complete player</h4><p>More than stats. Skill, mindset, habits, and character together.</p></div>
    </div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap two-col">
    <div class="stack"><span class="eyebrow">What we value</span><h2>Five commitments behind every session.</h2></div>
    <ul class="values">
      <li><strong>Develop players</strong><span>Growth over quick fixes. We build habits that last beyond one season.</span></li>
      <li><strong>Turn film into opportunity</strong><span>Every clip should lead to a specific improvement or a better way to present an athlete.</span></li>
      <li><strong>Bridge the gap to the next level</strong><span>Help athletes understand what the next level expects and how to get there.</span></li>
      <li><strong>Performance with purpose</strong><span>Clear goals, honest feedback, and progress you can see.</span></li>
      <li><strong>See the complete player</strong><span>Athletes are more than a stat line. We coach the person, not just the position.</span></li>
    </ul>
  </div>
</section>
{cta_band()}
'''

def svc(id_, tag, title, desc, what, get, who):
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    return f'''<article class="svc" id="{id_}">
  <div class="svc-head"><span class="eyebrow">{tag}</span><h2 style="font-size:clamp(1.7rem,3vw,2.3rem)">{title}</h2><p>{desc}</p></div>
  <div class="svc-body">
    <div><h4>What we work on</h4><ul>{li(what)}</ul></div>
    <div><h4>What you get</h4><ul>{li(get)}</ul></div>
    <div style="grid-column:1/-1"><h4>Best for</h4><p style="color:var(--mute)">{who}</p></div>
  </div>
</article>'''

SERVICES = page_hero("Services",
                     'Six services. <span class="accent">One</span> goal.',
                     "Every TrueFrame service helps athletes perform better when competition gets hard. Start with one, or combine them into a complete development plan.",
                     '<nav class="jump" aria-label="Services on this page"><a href="#mental-performance">Mental Performance</a><a href="#assessments">Assessments</a><a href="#film-review">Film Review</a><a href="#development-plans">Development Plans</a><a href="#team-programs">Team &amp; School</a><a href="#recruiting">Recruiting</a></nav>') + '''
<section class="section on-white"><div class="wrap">''' + "".join([
    svc("mental-performance", "Core service", "Mental Performance Coaching",
        "One-on-one coaching on the mental skills that decide close games. This is the center of TrueFrame, and every other service connects back to it.",
        ["Confidence that holds after a bad play", "Focus and attention control", "Handling pressure and big moments", "Recovering from mistakes with a reset routine", "Responding to adversity and setbacks", "Pre-game and in-game preparation"],
        ["Regular one-on-one sessions", "Personal reset and pre-game routines", "Practice assignments between sessions", "Progress check-ins with the athlete (and parents, if applicable)"],
        "Athletes who play well in practice but tighten up in games, lose confidence after mistakes, or want an edge in high-pressure competition."),
    svc("assessments", "Start here", "Athlete Assessments",
        "A structured starting point. We identify where an athlete is strong, where they break down, and which habits are helping or hurting them.",
        ["Current strengths and performance gaps", "Mindset habits and self-talk", "Typical responses to pressure and mistakes", "Goals, motivation, and preparation habits"],
        ["Assessment conversation and questionnaire", "Written summary of findings", "Recommended focus areas and next steps"],
        "Any athlete starting with TrueFrame, and parents or coaches who want a clear, objective picture before committing to a plan."),
    svc("film-review", "Film", "Film Review &amp; Performance Analysis",
        "We break down real game film to see what happens when the game speeds up, and give clear feedback the athlete can act on.",
        ["Decision-making and reads", "Hesitation and passed-up opportunities", "Body language after mistakes and bad calls", "Pressure responses in key moments", "Recurring performance habits"],
        ["Time-stamped breakdown of key moments", "Clear feedback on what to keep, fix, and build", "Follow-up review to measure change"],
        "Athletes and teams who have game film and want to understand what it shows beyond the box score."),
    svc("development-plans", "Development", "Individual Athlete Development Plans",
        "We turn assessment and film findings into a personal plan with specific goals, behaviors, drills, and routines.",
        ["Mental-performance goals", "Behaviors to build and habits to replace", "Drills and routines tied to film findings", "How to measure progress game to game"],
        ["Written development plan", "Goal checkpoints through the season", "Plan updates as the athlete improves"],
        "Athletes who want a structured path for a season or off-season, and parents who want to see measurable progress."),
    svc("team-programs", "Programs", "Team &amp; School Programs",
        "Mental-performance sessions and programs for high schools, colleges, coaches, clubs, and athletic departments.",
        ["Team sessions on pressure, composure, and resilience", "Shared language for mistakes and resets", "Coach workshops on building mentally tough athletes", "Film-based team pressure reviews"],
        ["Single sessions or season-long programs", "Materials for athletes and staff", "Program summary for coaches and administrators"],
        "Coaches and athletic directors who want their whole roster better prepared for pressure. <a href=\"schools-teams.html\" style=\"color:var(--purple);font-weight:700\">See Schools &amp; Teams &rarr;</a>"),
    svc("recruiting", "Next level", "Recruiting Support",
        "Help presenting an athlete honestly and professionally to college coaches, backed by film and a clear profile.",
        ["Highlight-film review and clip selection", "Athlete profile and presentation", "Communicating with coaches professionally", "Showing composure and character on film"],
        ["Highlight-film feedback", "Athlete profile guidance", "Recruiting communication tips and next steps"],
        "High school and club athletes preparing to reach out to college programs, and parents navigating recruiting for the first time."),
]) + '''
  <div class="callout" style="margin-top:40px"><p><strong>Pricing:</strong> Packages depend on the athlete or program and the combination of services. We&rsquo;ll recommend a fit and share pricing during your free consultation.</p></div>
</div></section>''' + cta_band("Not sure where to start?", "Most athletes begin with an assessment and a film review. Tell us about the athlete or program and we&rsquo;ll recommend a starting point.")

SCHOOLS = page_hero("Schools &amp; Teams",
                    'Build a roster that <span class="accent">holds up</span> under pressure.',
                    "Mental-performance programs for high schools, colleges, clubs, and athletic departments. Give your athletes and staff a shared approach to pressure, mistakes, and composure.",
                    '<div class="btn-row" style="margin-top:8px"><a class="btn btn-primary" href="contact.html">Request a program consultation <span class="arr">&rarr;</span></a></div>') + '''
<section class="section on-white">
  <div class="wrap two-col">
    <div class="stack"><span class="eyebrow">The problem</span><h2>Coaches see it every season.</h2></div>
    <div class="prose">
      <p>A team that executes in practice falls apart during a run by the opponent. A starter can&rsquo;t let go of a turnover. Players tighten up in the playoffs. Coaches have limited practice time and rarely have a system for training the mental side.</p>
      <p>TrueFrame gives your program that system: structured sessions, a common language for resets and composure, and film-based feedback that connects mental performance to what actually happens in games.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Programs</span><h2>Flexible formats for your program.</h2></div>
    <div class="tiles">
      <article class="tile"><span class="eyebrow">Team sessions</span><h3>Mental Performance Sessions</h3><p>Interactive team sessions on confidence, composure, focus, and responding to mistakes. Athletes leave with a reset routine they can use in the next game.</p><div class="meta"><span>Single or series</span><span>In-person or virtual</span></div></article>
      <article class="tile"><span class="eyebrow">Season-long</span><h3>Season Program</h3><p>A structured program through preseason, conference play, and postseason, with sessions timed to the pressure points of the schedule.</p><div class="meta"><span>Full season</span><span>Progress reporting</span></div></article>
      <article class="tile"><span class="eyebrow">Staff</span><h3>Coach Workshops</h3><p>Practical tools for coaches: how to talk to athletes after mistakes, build confidence during slumps, and create pressure in practice.</p><div class="meta"><span>Coaches &amp; staff</span><span>Department-wide</span></div></article>
      <article class="tile"><span class="eyebrow">Film</span><h3>Team Film &amp; Pressure Review</h3><p>We review team film for pressure moments: momentum swings, late-game decisions, and body language, then turn findings into team habits.</p><div class="meta"><span>Game film</span><span>Team &amp; individual clips</span></div></article>
    </div>
  </div>
</section>

<section class="section on-dark">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">How we work with programs</span><h2>Simple to start. Built around your season.</h2></div>
    <div class="steps">
      <div class="step"><h3>Consult</h3><p>We meet with the coach or athletic director to understand the roster, the season, and the goals.</p></div>
      <div class="step"><h3>Design</h3><p>We recommend a format: sessions, a season program, coach workshops, film review, or a mix.</p></div>
      <div class="step"><h3>Deliver</h3><p>Sessions and film reviews run on your schedule, in person or virtual.</p></div>
      <div class="step"><h3>Report</h3><p>Coaches and administrators get a clear summary of what was covered and what&rsquo;s changing.</p></div>
    </div>
  </div>
</section>

<section class="section on-white">
  <div class="wrap two-col">
    <div class="stack"><span class="eyebrow">Who it&rsquo;s for</span><h2>Any program, any sport.</h2><p class="lede">We&rsquo;re launching with basketball and work with programs across sports.</p></div>
    <ul class="values">
      <li><strong>High schools</strong><span>Varsity and JV teams, athletic departments, and multi-sport programs.</span></li>
      <li><strong>Colleges</strong><span>Teams and departments looking for mental-performance support alongside strength and sport coaching.</span></li>
      <li><strong>Clubs &amp; travel teams</strong><span>Club and AAU-style programs preparing athletes for showcases and tournaments.</span></li>
      <li><strong>Coaches &amp; organizations</strong><span>Coaching staffs, leagues, camps, and sports organizations.</span></li>
    </ul>
  </div>
</section>
''' + cta_band("Let&rsquo;s talk about your program.", "Tell us about your team, your season, and what you&rsquo;re seeing under pressure. We&rsquo;ll recommend a format that fits.")

PARENTS = page_hero("Athletes &amp; Parents",
                    'Play like you practice. <span class="accent">Especially</span> when it matters.',
                    "One-on-one mental performance coaching, film review, and development plans for athletes who want to be at their best when the game gets hard.") + '''
<section class="section on-dark" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Sound familiar?</span><h2>Signs an athlete could benefit.</h2></div>
    <ul class="signs">
      <li>Plays great in practice, then tightens up in games</li>
      <li>One mistake turns into several</li>
      <li>Hesitates or passes up opportunities they&rsquo;d normally take</li>
      <li>Body language changes after a bad play or call</li>
      <li>Confidence rises and falls with playing time or the last game</li>
      <li>Struggles with nerves before big games, tryouts, or showcases</li>
      <li>Is coming back from an injury, slump, or tough season</li>
      <li>Wants to play at the next level and needs a clearer path</li>
    </ul>
  </div>
</section>

<section class="section on-white">
  <div class="wrap">
    <div class="sec-head"><span class="eyebrow">Getting started</span><h2>What the first few weeks look like.</h2></div>
    <div class="steps light">
      <div class="step"><h3>Free consultation</h3><p>A conversation with the athlete and parent about what&rsquo;s happening, goals, and whether TrueFrame is a fit.</p></div>
      <div class="step"><h3>Assessment</h3><p>We identify strengths, mindset habits, and how the athlete responds to pressure and mistakes.</p></div>
      <div class="step"><h3>Film review</h3><p>We watch real game film together and point out the moments that matter.</p></div>
      <div class="step"><h3>Plan &amp; coaching</h3><p>The athlete gets a development plan and regular coaching, with progress you can see.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap two-col">
    <div class="stack">
      <span class="eyebrow">For parents</span>
      <h2>You&rsquo;ll know what we&rsquo;re working on and why.</h2>
      <p class="lede">Parents are part of the process. You&rsquo;ll get a clear picture of the plan, the goals, and how your athlete is progressing, with honest feedback and no guesswork.</p>
    </div>
    <div class="faq">
      <details open><summary>Is this therapy or counseling?</summary><p>No. Mental performance coaching focuses on sport performance skills like confidence, focus, composure, and preparation. It isn&rsquo;t a substitute for mental health care. If concerns come up that are outside the scope of performance coaching, we&rsquo;ll recommend connecting with a licensed professional.</p></details>
      <details><summary>Does my athlete have to play basketball?</summary><p>No. We&rsquo;re launching with basketball, but the TrueFrame approach works across sports. Pressure, mistakes, and confidence work the same way in every sport.</p></details>
      <details><summary>Do we need game film?</summary><p>Film helps a lot, and most athletes have access to some through their team or a streaming service. If you don&rsquo;t have film, we can still start with an assessment and mental performance coaching.</p></details>
      <details><summary>Are sessions in person or virtual?</summary><p>Both options are available. Film review and coaching work well virtually, which makes it easier to fit around school and practice schedules.</p></details>
      <details><summary>How long until we see a difference?</summary><p>Every athlete is different. Many notice changes in how they handle mistakes within a few weeks of using a reset routine. We track progress on film so you can see it for yourself.</p></details>
      <details><summary>How much does it cost?</summary><p>It depends on the services and how often you meet. We&rsquo;ll recommend options and share pricing during the free consultation.</p></details>
    </div>
  </div>
</section>
''' + cta_band("Start with a free consultation.", "Tell us about your athlete, their sport, and what you&rsquo;re seeing in games. We&rsquo;ll follow up to schedule a time to talk.")

CONTACT = page_hero("Contact",
                    'Let&rsquo;s get <span class="accent">started.</span>',
                    "Schedule a free consultation or ask about team and school programs. Tell us a little about the athlete or program and we&rsquo;ll follow up within two business days.") + f'''
<section class="section">
  <div class="wrap contact-grid">
    <form class="form" id="contact-form" novalidate>
      <div class="form-row">
        <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="f-phone">Phone <span class="opt">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="field"><label for="f-role">I am a&hellip;</label>
          <select id="f-role" name="role" required>
            <option value="">Select one</option><option>Athlete</option><option>Parent / guardian</option><option>Coach</option>
            <option>Athletic director / administrator</option><option>Club or organization</option><option>Other</option>
          </select></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="f-sport">Sport</label><input id="f-sport" name="sport" placeholder="e.g. Basketball"></div>
        <div class="field"><label for="f-org">School, team, or organization <span class="opt">(optional)</span></label><input id="f-org" name="organization"></div>
      </div>
      <fieldset class="chips" id="f-services">
        <legend>Interested in</legend>
        <label><input type="checkbox" name="services" value="Mental Performance Coaching"> Mental performance</label>
        <label><input type="checkbox" name="services" value="Athlete Assessment"> Assessment</label>
        <label><input type="checkbox" name="services" value="Film Review"> Film review</label>
        <label><input type="checkbox" name="services" value="Development Plan"> Development plan</label>
        <label><input type="checkbox" name="services" value="Team/School Program"> Team / school program</label>
        <label><input type="checkbox" name="services" value="Recruiting Support"> Recruiting</label>
        <label><input type="checkbox" name="services" value="Not sure"> Not sure yet</label>
      </fieldset>
      <div class="field"><label for="f-msg">What&rsquo;s going on?</label><textarea id="f-msg" name="message" placeholder="What are you seeing in games? What would you like to improve?"></textarea></div>
      <div class="btn-row"><button class="btn btn-primary" type="submit" id="f-submit">Request Consultation <span class="arr">&rarr;</span></button></div>
      <div class="form-status" id="f-status" role="status" hidden></div>
    </form>
    <aside class="aside">
      <div class="aside-box"><h3>Free consultation</h3><p>A 20&ndash;30 minute conversation about the athlete or program, what&rsquo;s happening under pressure, and which services fit. No commitment.</p></div>
      <div class="aside-box"><h3>Email us directly</h3>
        <div class="copyline"><code id="email-text">{EMAIL}</code><button class="copy-btn" type="button" id="copy-email">Copy</button></div></div>
      <div class="aside-box"><h3>Schools &amp; programs</h3><p>Athletic directors and coaches: include your season dates and roster size and we&rsquo;ll come prepared with program options.</p></div>
    </aside>
  </div>
</section>
<script>
(function(){{
  var f=document.getElementById('contact-form'), s=document.getElementById('f-status'), b=document.getElementById('f-submit');
  function show(cls,msg){{ s.className='form-status '+cls; s.innerHTML=msg; s.hidden=false; }}
  f.addEventListener('submit', function(e){{
    e.preventDefault();
    var el=f.elements, name=el['name'].value.trim(), email=el['email'].value.trim(), role=el['role'].value;
    if(!name||!/^\\S+@\\S+\\.\\S+$/.test(email)||!role){{ show('err','Please add your name, a valid email, and who you are so we know how to follow up.'); return; }}
    var data={{}}; new FormData(f).forEach(function(v,k){{ if(k==='services'){{ (data[k]=data[k]||[]).push(v); }} else data[k]=v; }});
    b.disabled=true;
    fetch('/api/contact',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(data)}})
      .then(function(r){{ if(!r.ok) throw 0; f.reset(); show('ok','<strong>Request received.</strong> We&rsquo;ll follow up within two business days.'); }})
      .catch(function(){{ show('err','We couldn&rsquo;t send your request. Please email us at <strong>{EMAIL}</strong>.'); }})
      .finally(function(){{ b.disabled=false; }});
  }});
  var c=document.getElementById('copy-email');
  c.addEventListener('click', function(){{
    var t=document.getElementById('email-text').textContent;
    try {{ navigator.clipboard.writeText(t).then(function(){{ c.textContent='Copied'; }}, sel); }} catch(_){{ sel(); }}
    function sel(){{ var r=document.createRange(); r.selectNodeContents(document.getElementById('email-text')); var w=getSelection(); w.removeAllRanges(); w.addRange(r); }}
  }});
}})();
</script>'''

PAGES = [
    ("index.html", "TrueFrame Athletics", "TrueFrame Athletics helps athletes perform when it gets hard: mental performance coaching, film analysis, and athlete development for athletes, parents, coaches, and schools.", HOME),
    ("about.html", "About | TrueFrame Athletics", "Why TrueFrame Athletics exists and how we develop the complete player: mental performance first, proven on film.", ABOUT),
    ("services.html", "Services | TrueFrame Athletics", "Mental performance coaching, athlete assessments, film review, development plans, team programs, and recruiting support.", SERVICES),
    ("schools-teams.html", "Schools & Teams | TrueFrame Athletics", "Mental performance programs for high schools, colleges, clubs, coaches, and athletic departments.", SCHOOLS),
    ("athletes-parents.html", "Athletes & Parents | TrueFrame Athletics", "One-on-one mental performance coaching, film review, and development plans for athletes and their parents.", PARENTS),
    ("contact.html", "Contact | TrueFrame Athletics", "Schedule a free consultation with TrueFrame Athletics.", CONTACT),
]


def head_bits(title, desc, path):
    url = SITE + "/" + ("" if path == "index.html" else path)
    return (f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
            f'<link rel="canonical" href="{url}">\n<meta property="og:title" content="{title}">\n'
            f'<meta property="og:description" content="{desc}">\n<meta property="og:url" content="{url}">\n'
            f'<meta name="theme-color" content="#111111">\n<link rel="icon" href="favicon.svg" type="image/svg+xml">\n'
            f'{FONTS}\n<link rel="stylesheet" href="styles.css">')


def full_doc(path, title, desc, body):
    return (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            f'{head_bits(title, desc, path)}\n</head>\n<body>\n{header(path)}\n<main>{body}</main>\n{FOOTER}\n</body>\n</html>\n')


def fragment_doc(path, title, desc, body):
    return f'{head_bits(title, desc, path)}\n{header(path)}\n<main>{body}</main>\n{FOOTER}\n'


def main():
    dark = open(os.path.join(HERE, "logo-mark.svg")).read().replace("#111111", "#F7F7F9")
    open(os.path.join(HERE, "logo-mark-dark.svg"), "w").write(dark)
    assets = ["styles.css", "logo-mark.svg", "logo-mark-dark.svg", "favicon.svg"]
    for out in ("dist", "preview"):
        d = os.path.join(HERE, out)
        shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        for a in assets: shutil.copy(os.path.join(HERE, a), d)
        for path, title, desc, body in PAGES:
            html = fragment_doc(path, title, desc, body) if (out == "preview" and path == "index.html") else full_doc(path, title, desc, body)
            open(os.path.join(d, path), "w").write(html)
    open(os.path.join(HERE, "dist", "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}/{'' if p == 'index.html' else p}</loc></url>" for p, *_ in PAGES)
    open(os.path.join(HERE, "dist", "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print("built")


if __name__ == "__main__":
    main()
