import feedparser
import requests
import json
import os

# Telegram credentials (GitHub Secrets)
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Optimized high-intent keywords
KEYWORDS = [
    "shopify custom calculator",
    "roi tool developer",
    "pricing calculator",
    "quote estimator",
    "web calculator",
    "calculator js",
    "javascript calculator",
    "calculator"
]

# Matching RSS feeds
RSS_FEEDS = [
    "https://www.upwork.com/ab/feed/jobs/rss?q=shopify+calculator",
    "https://www.upwork.com/ab/feed/jobs/rss?q=roi+calculator",
    "https://www.upwork.com/ab/feed/jobs/rss?q=pricing+calculator",
    "https://www.upwork.com/ab/feed/jobs/rss?q=quote+estimator",
    "https://www.upwork.com/ab/feed/jobs/rss?q=web+calculator",
    "https://www.upwork.com/ab/feed/jobs/rss?q=javascript+calculator"
]

SEEN_FILE = "seen_jobs.json"

# Load previously sent jobs
def load_seen():
    try:
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    except:
        return set()

# Save sent jobs
def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

# Send Telegram message
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

# Keyword matching
def should_send(summary, title):
    content = (title + summary).lower()
    return any(keyword in content for keyword in KEYWORDS)

# Load seen jobs
seen = load_seen()

# Parse feeds
for rss in RSS_FEEDS:
    feed = feedparser.parse(rss)

    for job in feed.entries:

        if job.link in seen:
            continue

        if should_send(job.summary, job.title):

            # Payment verification detection
            verified = "payment verified" in job.summary.lower()
            tag = "✅ Verified" if verified else "⚠️ Unverified"

            # Smart tagging
            content = (job.title + job.summary).lower()

            if "shopify" in content:
                category = "🛒 Shopify"
            elif "roi" in content:
                category = "📊 ROI Tool"
            elif "javascript" in content or "js" in content:
                category = "💻 JS Dev"
            else:
                category = "🧮 Calculator"

            message = f"""{category} | {tag}

Title: {job.title}

{job.link}
"""

            send(message)
            seen.add(job.link)

# Save updated jobs
save_seen(seen)
