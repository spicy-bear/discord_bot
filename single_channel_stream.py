import time
import feedparser
import discord

url_strings = [
    'https://www.cisa.gov/uscert/ncas/alerts.xml',
    'https://krebsonsecurity.com/feed/'
]

displayed_titles = []
all_items = []  # Initialize all_items here

TOKEN = "discord_token"
CHANNEL_ID = "channel_id"

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Connected to Discord!")
    while True:
        print("Loading RSS feeds... please wait")
        for url in url_strings:
            try:
                feed = feedparser.parse(url)
                items = feed.entries
                for item in items:
                    if 'published_parsed' not in item:
                        continue

                    pub_date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.mktime(item.published_parsed)))

                    if pub_date > time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time() - 12 * 3600)):
                        all_items.append({
                            'title': item.title,
                            'link': item.link,
                            'description': item.description,
                            'pub_date': pub_date
                        })
            except Exception:
                continue

        all_items.sort(key=lambda x: x['title'])

        counter = 1
        for item in all_items:
            title = item['title']
            link = item['link']
            description = item['description']
            pub_date = item['pub_date']

            if title in displayed_titles:
                continue

            message = (
                f"[{counter}] Title: {title}\n"
                f"Publish date: {pub_date}\n"
                f"Description: {description}\n"
                f"Source: {link}"
            )

            channel = client.get_channel(int(CHANNEL_ID))
            await channel.send(message)

            displayed_titles.append(title)
            counter += 1

            time.sleep(3)

        all_items.clear()  # Clear all_items after each iteration

client.run(TOKEN)
