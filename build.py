"""Builds every page from pages/*.html plus one shared header and footer.

Run: python3 build.py
- Edit page bodies in pages/*.html.
- Edit the header, footer, phone, license and page list here.
- Tokens available in page bodies: {PHONE} {TEL} {LICENSE} {CHECK} and {ICON:name}.
- Every page is a full HTML document. A fragment copy of the homepage goes to
  .preview/index.html for the claude.ai preview (gitignored).
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
PREVIEW = ROOT / ".preview"
PHONE = "(813) 555-0142"
TEL = "+18135550142"
LICENSE = "EC0000000"
FONTS = "https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap"

CHECK = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg>'

# Simple stroke icons, 24x24.
_I = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
ICONS = {
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
    "home": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
    "hardhat": '<path d="M3 17h18"/><path d="M5 17a7 7 0 0 1 14 0"/><path d="M10 10V6h4v4"/><path d="M4 17v2h16v-2"/>',
    "building": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2"/><path d="M10 21v-3h4v3"/>',
    "panel": '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h6M9 10.5h6M9 14h6M9 17.5h6"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4 2.5-2.5z"/>',
    "bulb": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
    "fan": '<circle cx="12" cy="12" r="1.5"/><path d="M12 10.5C12 6 13 3 16 3s3 4-4 7.5zM13.5 12c4.5 0 7.5 1 7.5 4s-4 3-7.5-4zM12 13.5c0 4.5-1 7.5-4 7.5s-3-4 4-7.5zM10.5 12C6 12 3 11 3 8s4-3 7.5 4z"/>',
    "plug": '<path d="M9 2v5M15 2v5"/><path d="M6 7h12v4a6 6 0 0 1-12 0V7z"/><path d="M12 17v5"/>',
    "shield": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3z"/><path d="m13 8-3 5h4l-3 5"/>',
    "generator": '<rect x="3" y="7" width="18" height="12" rx="1.5"/><path d="M7 7V5h10v2"/><path d="m13 10-3 4h4l-3 4"/>',
    "car": '<path d="M5 16V11l2-5h10l2 5v5"/><path d="M3 16h18v2H3z"/><circle cx="7.5" cy="13" r="1"/><circle cx="16.5" cy="13" r="1"/>',
    "wave": '<path d="M3 15c2 0 2-2 4.5-2S10 15 12 15s2-2 4.5-2S19 15 21 15"/><path d="M3 19c2 0 2-2 4.5-2S10 19 12 19s2-2 4.5-2S19 19 21 19"/><path d="M8 11V4M16 11V4M8 7h8"/>',
    "wire": '<path d="M3 12h4l2-4 3 8 2-4h7"/>',
    "ruler": '<path d="M3 17 17 3l4 4L7 21z"/><path d="m7 13 2 2M10 10l2 2M13 7l2 2"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "camera": '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    "badge": '<circle cx="12" cy="9" r="6"/><path d="m9 14-1 7 4-2 4 2-1-7"/>',
    "broom": '<path d="M19 3 11 11"/><path d="M11 11c-3 0-6 2-7 6l-1 4 4-1c4-1 6-4 6-7z"/><path d="m7 15 2 2"/>',
    "phone": '<path d="M5 3h4l2 5-3 2a12 12 0 0 0 6 6l2-3 5 2v4a2 2 0 0 1-2 2A18 18 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="1.5"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
}

def icon(name):
    return _I.format(ICONS[name])

NAV = [
    ("residential.html", "Residential", "residential"),
    ("construction.html", "New construction", "construction"),
    ("commercial.html", "Commercial", "commercial"),
    ("generators.html", "Generators", "generators"),
    ("club.html", "Volt Club", "club"),
]

LOGO = """<a class="logo" href="index.html" aria-label="Volt Boys Electric home">
      <span class="logo-mark"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 2 5 13.5h6L9.5 22 19 9.5h-6.2L13.5 2Z" fill="currentColor"/></svg></span>
      <span class="logo-word">Volt Boys<small>ELECTRIC · LIC. {LICENSE}</small></span>
    </a>"""

HEADER = """<a class="skip" href="#main">Skip to content</a>
<div class="announce"><div class="wrap"><span><b>Led by master electricians</b> · Free estimates</span><span>Same-day service calls</span><span>24/7 emergencies</span></div></div>
<header class="top">
  <div class="wrap">
    """ + LOGO + """
    <nav class="links" id="mainNav" aria-label="Main">
{NAVLINKS}
      <a class="nav-contact" href="contact.html">Contact</a>
    </nav>
    <div class="top-cta">
      <a class="top-phone" href="tel:{TEL}">{PHONE}</a>
      <a class="btn btn-volt btn-sm" href="contact.html">Free estimate</a>
      <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="mainNav" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<main id="main">
"""

FOOTER = """</main>
<footer class="site">
  <div class="wrap">
    <div class="foot-brand">
      """ + LOGO + """
      <p>Master electrician-led. Licensed Florida electrical contractor for homes, builders and businesses across Tampa Bay.</p>
      <p class="foot-phone">{PHONE}</p>
    </div>
    <div class="foot-col">
      <h4>Residential</h4>
      <a href="residential.html">Service &amp; repair</a>
      <a href="panel-replacement.html">Panel replacement</a>
      <a href="generators.html">Generators</a>
      <a href="ev-chargers.html">EV chargers</a>
      <a href="residential.html#lighting">Lighting &amp; fans</a>
    </div>
    <div class="foot-col">
      <h4>Construction &amp; commercial</h4>
      <a href="construction.html">New construction</a>
      <a href="construction.html#remodels">Remodels &amp; additions</a>
      <a href="commercial.html">Commercial build-outs</a>
      <a href="commercial.html#service">Commercial service</a>
    </div>
    <div class="foot-col">
      <h4>Company</h4>
      <a href="club.html">Volt Club membership</a>
      <a href="contact.html">Contact &amp; service area</a>
      <a href="contact.html">Careers</a>
    </div>
  </div>
  <div class="wrap foot-legal">
    <span>© 2026 Volt Boys Electric LLC · Florida Certified Electrical Contractor Lic. #{LICENSE} · Licensed &amp; insured</span>
    <span>Concept · phone, license and prices are placeholders</span>
  </div>
</footer>
<div class="actionbar">
  <a class="btn btn-volt" href="tel:{TEL}">Call</a>
  <a class="btn btn-ink" href="sms:{TEL}">Text</a>
  <a class="btn btn-line" href="contact.html">Estimate</a>
</div>
<script src="site.js"></script>
"""

CTA = """
  <section class="cta-band">
    <div class="wrap">
      <div>
        <h2>{cta_title}</h2>
        <p class="lede">Call, text a photo, or send the details. You get a written price, fast.</p>
      </div>
      <div class="cta-row">
        <a class="btn btn-ink" href="tel:{TEL}">Call {PHONE}</a>
        <a class="btn btn-line" href="contact.html">Get a free estimate</a>
      </div>
    </div>
  </section>
"""

HEAD = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
"""
COMMON_HEAD = """<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="styles.css">
"""

PAGES = [
    # file, title, description, nav key, CTA band title (None = no band)
    ("index.html", "Volt Boys Electric",
     "Licensed Tampa Bay electricians for service calls, panels, generators, remodels, new construction and commercial work.",
     "home", None),
    ("residential.html", "Residential Electrician | Volt Boys Electric",
     "Home electrical service and repair in Tampa Bay: troubleshooting, panels, rewiring, lighting, fans, outlets, surge protection, pools.",
     "residential", "Something not working? We'll come fix it."),
    ("construction.html", "New Construction Electrical | Volt Boys Electric",
     "Rough-in to trim-out electrical for builders, GCs and homeowners: new homes, additions and remodels across Tampa Bay.",
     "construction", "Send us your plans. We'll send a bid."),
    ("commercial.html", "Commercial Electrician | Volt Boys Electric",
     "Commercial electrical in Tampa Bay: tenant build-outs, service and maintenance, lighting retrofits and backup power.",
     "commercial", "Keep your business running."),
    ("generators.html", "Standby Generators | Volt Boys Electric",
     "Whole-home standby generator installation in Tampa Bay. Sizing, permits, gas tie-in and yearly service.",
     "generators", "Get ready before June 1."),
    ("panel-replacement.html", "Panel Replacement | Volt Boys Electric",
     "Federal Pacific, Zinsco and fuse panel replacement for Florida insurance and home sales. Quotes in 24 hours.",
     "residential", "Closing soon? Send us the report."),
    ("ev-chargers.html", "EV Charger Installation | Volt Boys Electric",
     "Level 2 EV charger installation in Tampa Bay, with a panel load check on every job.",
     "residential", "Charge at home tonight, not next month."),
    ("club.html", "Volt Club | Volt Boys Electric",
     "Volt Club membership: yearly electrical safety check, generator service, priority scheduling and member pricing.",
     "club", "Be first in line when you need us."),
    ("contact.html", "Contact | Volt Boys Electric",
     "Call, text or send a photo for a free estimate. Serving Hillsborough, Pinellas and Pasco counties.",
     "contact", None),
]

def fill(text):
    text = re.sub(r"\{ICON:(\w+)\}", lambda m: icon(m.group(1)), text)
    return (text.replace("{CHECK}", CHECK).replace("{PHONE}", PHONE)
                .replace("{TEL}", TEL).replace("{LICENSE}", LICENSE).replace("{FONTS}", FONTS))

for file, title, description, key, cta_title in PAGES:
    current = ' aria-current="page"'
    navlinks = "\n".join(
        f'      <a href="{href}"{current if k == key else ""}>{label}</a>'
        for href, label, k in NAV)
    body = (ROOT / "pages" / file).read_text()
    head = COMMON_HEAD.replace("{title}", title).replace("{description}", description)
    shell = HEADER.replace("{NAVLINKS}", navlinks) + body
    if cta_title:
        shell += CTA.replace("{cta_title}", cta_title)
    shell += FOOTER
    html = ("<!doctype html>\n<html lang=\"en\">\n<head>\n" + HEAD + head + "</head>\n<body>\n"
            + shell + "</body>\n</html>\n")
    (ROOT / file).write_text(fill(html))
    if file == "index.html":
        # Fragment copy for the claude.ai preview, which wraps the page itself.
        PREVIEW.mkdir(exist_ok=True)
        (PREVIEW / "index.html").write_text(fill(head + '<meta name="claude:viewport-fit-sides" content="cover">\n' + shell))
    print("built", file)
