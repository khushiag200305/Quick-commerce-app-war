# Project Notes: Quick-Commerce App War

## Data collection (Step 1)
- Scrape date: 8th oct 12:14am(date you ran the full scrape)
- Window: last 60 days from scrape time (DAYS_BACK = 60)
- Source: Google Play Store reviews via google-play-scraper (lang="en", country="in")
- Apps and package IDs:
  - Blinkit: com.grofers.customerapp
  - Zepto: com.zeptoconsumerapp
  - Instamart: in.swiggy.android.instamart (standalone app)

## Decisions
- Collected by date window, not fixed count: 10,000 reviews covered only ~4 days for Blinkit vs ~50 for Zepto/Instamart, so comparisons wouldn't be fair.
- Used the standalone Instamart app, not the Swiggy app, so reviews are about grocery only.

## Limitations
- I used the standalone Instamart app, so my data does not include grocery complaints from users who order Instamart through the main Swiggy app.

## Headline ratings at time of scrape (for comparison)
- Blinkit: 4.58 (1,240,588 written reviews)
- Zepto: 4.66 (467,307 written reviews)
- Instamart: 4.62 (124,679 written reviews)

- Full run: 109,709 reviews (Blinkit 83,045 | Zepto 13,226 | Instamart 13,438)
- Actual coverage: 2026-08-09 00:15 to 2026-10-07 00:27 (~59 days, all three apps)
- Newest reviews lag scrape time by ~1 day. First and last days are partial.
- Verified: no scrape errors, all apps reached the 60-day cutoff.