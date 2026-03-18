import feedparser
import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

RSS_FEEDS = [
    "https://www.upwork.com/ab/feed/jobs/rss?q=shopify",
    "https://www.upwork.com/ab/feed/jobs/rss?q=javascript",
    "https://www.upwork.com/ab/feed/jobs/rss?q=photoshop",
    "https://www.upwork.com/ab/feed/jobs/rss?q=graphic+design"
]

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

for rss in RSS_FEEDS:
    feed = feedparser.parse(rss)

    for job in feed.entries:

        message = f"""🚀 TEST JOB ALERT

Title: {job.title}

{job.link}
"""

        send(message)
