import feedparser
import requests
import json
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

KEYWORDS = [
    "shopify custom calculator",
    "roi tool developer",
    "pricing calculator",
    "quote estimator",
    "web calculator",
    "javascript calculator",
    "calculator js",
    "shopify calculator",
    "photo editing",
    "adobe photoshop",
    "adobe illustrator",
    "label design",
    "calculator"
]

RSS_FEEDS = [
    "https://www.upwork.com/ab/feed/jobs/rss?q=shopify+calculator",
    "https://www.upwork.com/ab/feed/jobs/rss?q=roi+calculator",
    "https://www.upwork.com/ab/feed/jobs/rss?q=pricing+calculator",
    "https://www.upwork.com/ab/feed/jobs/rss?q=web+calculator",
    "https://www.upwork.com/ab/feed/jobs/rss?q=javascript+calculator",
    "https://www.upwork.com/ab/feed/jobs/rss?q=photoshop",
    "https://www.upwork.com/ab/feed/jobs/rss?q=photo+editing",
    "https://www.upwork.com/ab/feed/jobs/rss?q=illustrator",
    "https://www.upwork.com/ab/feed/jobs/rss?q=label+design"
]

SEEN_FILE = "seen_jobs.json"

def load_seen():
    try:
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def should_send(summary, title):
    content = (title + summary).lower()
    return any(keyword in content for keyword in KEYWORDS)

seen = load_seen()

for rss in RSS_FEEDS:
    feed = feedparser.parse(rss)

    for job in feed.entries:

        if job.link in seen:
            continue

        if should_send(job.summary, job.title):

            verified = "payment verified" in job.summary.lower()
            tag = "✅ Verified" if verified else "⚠️ Unverified"

            content = (job.title + job.summary).lower()

            # Category detection
            if "shopify" in content:
                category = "🛒 Shopify"
            elif "roi" in content or "calculator" in content:
                category = "🧮 Calculator"
            elif "photoshop" in content or "photo editing" in content:
                category = "🖼️ Photoshop"
            elif "illustrator" in content or "label design" in content:
                category = "🎨 Illustrator"
            else:
                category = "📌 General"

            message = f"""{category} | {tag}

Title: {job.title}

{job.link}
"""

            send(message)
            seen.add(job.link)

save_seen(seen)
