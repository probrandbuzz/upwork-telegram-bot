import feedparser
import requests
import json
import os

# Telegram bot credentials (set as GitHub Secrets)
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# Keywords you want to track
KEYWORDS = [
    "calculator",
    "shopify price calculator",
    "photoshop",
    "photo editing",
    "logo design",
    "label design",
    "image editing"
]

# Upwork RSS feeds
RSS_FEEDS = [
    "https://www.upwork.com/ab/feed/jobs/rss?q=shopify+price+calculator",
    "https://www.upwork.com/ab/feed/jobs/rss?q=calculator",
    "https://www.upwork.com/ab/feed/jobs/rss?q=photoshop",
    "https://www.upwork.com/ab/feed/jobs/rss?q=photo+editing"
]

# File to store jobs already sent
SEEN_FILE = "seen_jobs.json"

# Load previously seen jobs
def load_seen():
    try:
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    except:
        return set()

# Save seen jobs
def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

# Send message to Telegram
def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# Check if job matches any keyword
def should_send(summary, title):
    content = (title + summary).lower()
    return any(k.lower() in content for k in KEYWORDS)

# Load seen jobs
seen = load_seen()

# Loop through RSS feeds
for rss in RSS_FEEDS:
    feed = feedparser.parse(rss)
    for job in feed.entries:
        if job.link in seen:
            continue

        if should_send(job.summary, job.title):
            # Check payment verification
            verified = "payment verified" in job.summary.lower()
            tag = "✅ Verified" if verified else "⚠️ Unverified"

            message = f"""
{tag} Upwork Job 🚀

Title: {job.title}

Link: {job.link}
"""

            send(message)
            seen.add(job.link)

# Save updated seen jobs
save_seen(seen)
send("✅ Telegram bot test message: Everything is working!")
