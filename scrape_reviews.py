"""
Step 1: Collect Google Play Store reviews for quick-commerce apps.
Project: Quick-Commerce App War (Blinkit vs Zepto vs Instamart)

Run:  python scrape_reviews.py
Output: data/raw/<app>_reviews.csv  and  data/raw/all_reviews.csv
"""

import os
import time
import pandas as pd
from google_play_scraper import reviews, Sort
from datetime import datetime, timedelta

DAYS_BACK = 60
CUTOFF = datetime.now() - timedelta(days=DAYS_BACK)
MAX_PER_APP = 300000   # safety cap so the loop can't run forever

# 1. Which apps to collect. The package ID is in the Play Store URL:
#    https://play.google.com/store/apps/details?id=THIS_PART
APPS = {
    "Blinkit": "com.grofers.customerapp",
    "Zepto": "com.zeptoconsumerapp",
    "Instamart": "in.swiggy.android.instamart",  
}

BATCH_SIZE = 200         # reviews per request
PAUSE_SECONDS = 2        # be polite: wait between requests

# Columns we keep. We deliberately DROP userName and userImage:
# we don't need personal info for analysis.
KEEP_COLUMNS = [
    "reviewId", "app", "score", "content", "thumbsUpCount",
    "reviewCreatedVersion", "at", "replyContent", "repliedAt",
]


def fetch_reviews(app_name, package_id, target):
    """Collect reviews newest-first until they are older than CUTOFF, or we hit the safety cap."""    """Collect reviews newest-first until they are older than CUTOFF, or we hit the safety cap."""
    all_reviews = []
    token = None  # tells Google where the previous batch ended

    while len(all_reviews) < target:
        try:
            batch, token = reviews(
                package_id,
                lang="en",
                country="in",
                sort=Sort.NEWEST,
                count=BATCH_SIZE,
                continuation_token=token,
            )
        except Exception as e:
            print(f"{app_name}: error -> {e}. Stopping this app.")
            break

        if not batch:          # no more reviews available
            break

        all_reviews.extend(batch)
        if batch[-1]["at"]<CUTOFF:
            break
        print(f"{app_name}: {len(all_reviews)} reviews collected")
        time.sleep(PAUSE_SECONDS)
    if not all_reviews:
        return pd.DataFrame()
    
    df = pd.DataFrame(all_reviews)
    df["app"] = app_name
    df = df[df["at"] >= CUTOFF]
    return df


def main():
    os.makedirs("data/raw", exist_ok=True)
    frames = []

    for app_name, package_id in APPS.items():
        if package_id.startswith("PASTE"):
            print(f"Skipping {app_name}: add its package ID first.")
            continue

        df = fetch_reviews(app_name, package_id,  MAX_PER_APP)
        if df.empty:
            continue

        df = df[[c for c in KEEP_COLUMNS if c in df.columns]]
        df.to_csv(f"data/raw/{app_name.lower()}_reviews.csv", index=False)
        frames.append(df)

    if frames:
        combined = pd.concat(frames, ignore_index=True)
        combined.to_csv("data/raw/all_reviews.csv", index=False)
        print(f"\nDone! {len(combined)} total reviews saved to data/raw/all_reviews.csv")
        print(combined.groupby("app")["score"].agg(["count", "mean"]).round(2))


if __name__ == "__main__":
    main()
