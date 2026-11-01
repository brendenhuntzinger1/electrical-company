# Volt Boys Electric: working agreements

Website for Volt Boys Electric, a full-service electrical contractor in Tampa Bay, Florida:
residential service, panels, new construction (rough-in to trim-out), remodels,
commercial, generators, EV chargers and the Volt Club membership.

## How the site is built

- Static HTML/CSS/JS, no framework yet.
- Page bodies live in `pages/*.html`. `build.py` wraps them in the shared header,
  footer, icons, phone number and license number. Run `python3 build.py` after any
  change and commit the generated `*.html` files too.
- Hosted on Vercel as a static site (no build step). Pushes to `main` deploy to production.
- `.preview/index.html` is a fragment copy of the homepage for the claude.ai preview (gitignored).
- Check every layout change at phone width (390px). Most visitors are on phones.

## Copy rules

- Plain, direct, confident. No invented numbers: no fake years in business, job
  counts, review counts, ratings or prices.
- Placeholders still to replace before launch: phone number, license number
  (`EC0000000`) and the Tampa Bay service area. Club and service prices are not shown
  until the owner sets them.
- No reviews on the site until they are real Google reviews. Never publish sample or
  made-up reviews.
- Photos in `images/` are free-license stock (Unsplash, Pexels). The people in them are
  not our crew; never caption them as "our team". Replace with real job photos when
  available.
- Claims the owner must confirm before launch: master electrician-led, fully insured
  (liability + workers' comp), workmanship guarantee, same-day service, 24/7 emergencies.
  Do not claim dealer status (e.g. Generac) until it is real.
- Florida contractor ads must show the license number. Keep it in the header and footer.
- "Led by master electricians" is only allowed if a master electrician actually leads
  the work. Florida's state license is the Certified Electrical Contractor (EC);
  "master electrician" is a county/city certificate. Confirm before launch.

## Not done yet

- The estimate form only shows a demo message. It needs to send to the owner's phone and email.
- Custom domain not connected yet (planned: voltboys.com).
