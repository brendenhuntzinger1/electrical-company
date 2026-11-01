"""Builds the inner pages from one shared header and footer.

Run: python3 build.py
Edit page content in pages/*.html; edit the shell here.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
PHONE = "(813) 555-0142"
TEL = "+18135550142"
LICENSE = "EC0000000"

CHECK = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg>'

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="top">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Seawall Electric home">
      <span class="logo-mark"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M13.5 2 5 13.5h6L9.5 22 19 9.5h-6.2L13.5 2Z" fill="#f5b800"/></svg></span>
      <span class="logo-word">Seawall Electric<small>LIC. {license}</small></span>
    </a>
    <nav class="links" aria-label="Main">
      <a href="generators.html"{cur_generators}>Generators</a>
      <a href="panel-replacement.html"{cur_panels}>Panel replacement</a>
      <a href="ev-chargers.html"{cur_ev}>EV chargers</a>
      <a href="index.html#plan">Storm-Ready Plan</a>
      <a href="contact.html"{cur_contact}>Contact</a>
    </nav>
    <a class="btn btn-volt" href="tel:{tel}" aria-label="Call {phone}">
      <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2Z"/></svg>
      <span class="top-phone-label">{phone}</span>
    </a>
  </div>
</header>
<main>
"""

CTA = """
  <section class="cta-band">
    <div class="wrap">
      <div>
        <h2>{cta_title}</h2>
        <p class="lede">Send a photo and get a flat quote within 24 hours.</p>
      </div>
      <div class="cta-row">
        <a class="btn btn-volt" href="tel:{tel}">Call {phone}</a>
        <a class="btn btn-line" href="contact.html?service={cta_service}">Get a quote</a>
      </div>
    </div>
  </section>
"""

FOOT = """</main>
<footer class="site">
  <div class="wrap">
    <span>© 2026 Seawall Electric LLC · Florida Certified Electrical Contractor Lic. #{license} · Licensed &amp; insured</span>
    <span>Concept · phone, license and prices are placeholders</span>
  </div>
</footer>
<div class="actionbar">
  <a class="btn btn-volt" href="tel:{tel}">Call</a>
  <a class="btn btn-ink" href="sms:{tel}">Text</a>
  <a class="btn btn-line" href="contact.html">Quote</a>
</div>
<script src="site.js"></script>
</body>
</html>
"""

PAGES = [
    # file, title, description, nav key, CTA title, CTA service (or None for no CTA band)
    ("generators.html", "Standby Generators | Seawall Electric",
     "Whole-home standby generator installation in Tampa Bay. Sizing, permits, gas tie-in and yearly service.",
     "generators", "Get ready before June 1.", "Standby generator"),
    ("panel-replacement.html", "Panel Replacement | Seawall Electric",
     "Federal Pacific, Zinsco and fuse panel replacement for Florida insurance and home sales. Quotes in 24 hours.",
     "panels", "Closing soon? Send us the report.", "Panel replacement or upgrade"),
    ("ev-chargers.html", "EV Charger Installation | Seawall Electric",
     "Level 2 EV charger installation in Tampa Bay, with a panel load check on every job.",
     "ev", "Charge at home tonight, not next month.", "EV charger"),
    ("contact.html", "Contact | Seawall Electric",
     "Call, text or send a photo for a flat quote within 24 hours. Serving Hillsborough, Pinellas and Pasco counties.",
     "contact", None, None),
]

for file, title, description, key, cta_title, cta_service in PAGES:
    cur = {f"cur_{k}": (' aria-current="page"' if k == key else "")
           for k in ("generators", "panels", "ev", "contact")}
    body = (ROOT / "pages" / file).read_text().replace("{CHECK}", CHECK).replace("{PHONE}", PHONE).replace("{TEL}", TEL)
    html = HEAD.format(title=title, description=description, license=LICENSE, tel=TEL, phone=PHONE, **cur)
    html += body
    if cta_title:
        html += CTA.format(cta_title=cta_title, cta_service=cta_service.replace(" ", "%20"), tel=TEL, phone=PHONE)
    html += FOOT.format(license=LICENSE, tel=TEL)
    (ROOT / file).write_text(html)
    print("built", file)
