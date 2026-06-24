#!/usr/bin/env python3
"""
Clarity Portal - Final Improved Version
"""

from flask import Flask, render_template, jsonify, request
import feedparser
import time
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ==================== YOUR FULL CATEGORIES ====================
CATEGORIES = {
    "Top Stories & Events": [
        {"name": "Google News", "url": "https://news.google.com/rss"},
        {"name": "The Guardian - World", "url": "https://www.theguardian.com/world/rss"},
        {"name": "BBC World", "url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
        #{"name": "Al Jazeera", "url": "https://apnews.com/rss"},
        {"name": "The Times Of India-Bangalore", "url": "https://timesofindia.indiatimes.com/rssfeeds/-2128833038.cms"},
        {"name": "The Times Of India-Most Read", "url": "https://timesofindia.indiatimes.com/rssfeedmostread.cms"},        
        ],
    "Technology": [
        {"name": "WIRED", "url": "https://www.wired.com/feed/rss"},
        {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index"},
        #{"name": "TESLA", "url": "https://www.tesla.com/blog/feed"},
        {"name": "Times Of India - Tech", "url": "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms"},        
        {"name": "Tech Crunch", "url": "https://techcrunch.com/feed/"},
        {"name": "The Vege", "url": "https://www.theverge.com/rss/index.xml"},
        {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/"},
        {"name": "Nautilus Magazine", "url": "https://nautil.us/feed/"},
        {"name": "Popular Science - How It Works", "url": "https://www.popsci.com/rss/"},
        #{"name": "SpaceX", "url": "https://www.spacex.com/rss.xml"},
        #{"name": "Explain xkcd - How It Works", "url": "https://explainxkcd.com/feed/"},
        #{"name": "Explain xkcd - How It Works", "url": "https://explainxkcd.com/feed/"},
    ],
    "AI & Innovations": [
        {"name": "WIRED AI", "url": "https://www.wired.com/feed/tag/ai/latest/rss"},
        {"name": "Quanta Magazine", "url": "https://api.quantamagazine.org/feed/"},
        {"name": "Mark Tech Post", "url": "https://www.marktechpost.com/feed/"},
        #{"name": "The Batch", "url": "https://www.deeplearning.ai/the-batch/feed/"},
        {"name": "arXiv cs.AI (research)", "url": "https://arxiv.org/rss/cs.AI"}, 
    ],
    "Science & Mathematics": [
        {"name": "Quanta Magazine", "url": "https://api.quantamagazine.org/feed/"},
        {"name": "Khan Academy", "url": "https://blog.khanacademy.org/feed/"},
        #{"name": "Art of Problem Solving", "url": "https://artofproblemsolving.com/feed"},
        {"name": "BBC Science", "url": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"},
        {"name": "WIRED Science", "url": "https://www.wired.com/feed/category/science/latest/rss"},
        {"name": "Times Of India - Science", "url": "https://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms"},
    ],
    "Geopolitics & World": [
        {"name": "Foreign Affairs", "url": "https://www.foreignaffairs.com/rss.xml"},
        {"name": "Foreign Policy", "url": "https://foreignpolicy.com/feed/"},
        {"name": "War on the Rocks", "url": "https://warontherocks.com/feed/"},
        {"name": "Diplomat", "url": "https://thediplomat.com/feed/"},
        {"name": "The New Global Order", "url": "https://thenewglobalorder.com/feed/"},
        {"name": "The Times Of India-World", "url": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms"}, 
        {"name": "The Times Of Israel", "url": "https://www.timesofisrael.com/feed/"}, 
        {"name": "The Drive (War Zone)", "url": "https://www.thedrive.com/feed"}, 
        #{"name": "Defense News", "url": "https://www.defensenews.com/rss/"}, 
        {"name": "Breaking Defense", "url": "https://breakingdefense.com/feed/"}, 
        {"name": "Space.com", "url": "https://www.space.com/feeds/all"}, 
        {"name": "Popular Mechanics - Military", "url": "https://www.popularmechanics.com/rss/"},
    ],
    "Economy & Stock Market": [
        {"name": "The Economic Times - India", "url": "https://economictimes.indiatimes.com/rssfeeds/13352306.cms"},
        {"name": "Seeking Alpha", "url": "https://seekingalpha.com/feed.xml"},
        {"name": "Finshots", "url": "https://finshots.in/rss/"},
        {"name": "Times Of India - Business", "url": "https://timesofindia.indiatimes.com/rssfeeds/1898055.cms"},
        {"name": "Economic Times - Recent Stories", "url": "https://b2b.economictimes.indiatimes.com/rss/recentstories"},
        {"name": "Economic Times - Electronics", "url": "https://b2b.economictimes.indiatimes.com/rss/electronics"},
        {"name": "Economic Times - Entreprenuer", "url": "https://b2b.economictimes.indiatimes.com/rss/entrepreneur"},
        #{"name": "Subramoney", "url": "https://subramoney.com/feed/"},
        {"name": "Freefincal (Pattu)", "url": "https://freefincal.com/feed/"},
        #{"name": "Moneycontrol", "url": "https://www.moneycontrol.com/rss/"},
        {"name": "ValuePickr", "url": "https://valuepickr.com/feed/"},
    ],
    "Sports": [
         {"name": "BBC Sport", "url": "https://feeds.bbci.co.uk/sport/rss.xml"},
        #{"name": "ESPN Cricinfo", "url": "https://www.espncricinfo.com/rss/content/rss"},
        {"name": "BBC Sport", "url": "https://feeds.bbci.co.uk/sport/football/rss.xml"},
        {"name": "The Hindu - Sport", "url": "https://www.thehindu.com/sport/feeder/default.rss"},
        {"name": "Times Of India - Sports", "url": "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms"},
        {"name": "Times Of India - Cricket", "url": "https://timesofindia.indiatimes.com/rssfeeds/54829575.cms"},
    ],
    "History, Legends & Heritage": [
         {"name": "Human Journey", "url": "https://humanjourney.us/feed/"},
        #{"name": "Elon Musk", "url": "https://x.ai/blog/feed"},       
        {"name": "The Marginalian", "url": "https://www.themarginalian.org/feed/"},
        #{"name": "Collections of Indian History", "url": "https://rss.feedspot.com/indian_history_rss_feeds/"},
        {"name": "Indian History Collective", "url": "https://indianhistorycollective.com/feed/"},
        {"name": "The Story Of India", "url": "https://storytrails.in/feed/"},
    ],
    "Podblogs": [
            {"name": "Tim Ferriss Blog", "url": "https://tim.blog/feed/"},
            {"name": "Lex Fridman", "url": "https://lexfridman.com/feed/podcast/"},
            {"name": "Astralcodex Ten", "url": "https://astralcodexten.substack.com/feed"},
            {"name": "Naval Ravikant", "url": "https://nav.al/feed"},
            {"name": "Gwern Branwen", "url": "https://www.gwern.net/feed.rss"},
            {"name": "Paul Graham Essays", "url": "http://www.aaronsw.com/2002/feeds/pgessays.rss"},
            {"name": "Stratechery (Ben Thompson)", "url": "https://stratechery.com/feed/"},
            {"name": "Dan Wang", "url": "https://danwang.substack.com/feed/"},
            {"name": "Balaji Srinivasan", "url": "https://balajis.com/feed/"},
    ],
    "Education": [
        {"name": "Learn CBSE", "url": "https://www.learncbse.in/feed/"},
        #{"name": "freeCodeCamp", "url": "https://www.freecodecamp.org/news/feed/"},
        {"name": "DEV Community", "url": "https://dev.to/feed"},
        {"name": "Real Python", "url": "https://realpython.com/feed"},
            # Add education blogs, university news, learning resources RSS here
    ],
    "Agri Tech": [
        {"name": "The Better India - Agri", "url": "https://www.thebetterindia.com/feed/"},
        {"name": "Modern Farmer", "url": "https://modernfarmer.com/feed/"},
        {"name": "AgFunderNews", "url": "https://agfundernews.com/feed/"},
        {"name": "PrecisionAg", "url": "https://www.precisionag.com/feed/"},
    ],
    "Custom Scraped": [
         # Add agricultural technology, farming innovations, agri-research feeds here
        {"name": "Substack", "url": "https://nextplayso.substack.com/p/best-blogs-for-tech-people"},
        #{"name": "ESPN Cricinfo", "url": "https://www.espncricinfo.com/"},
        {"name": "PGurus", "url": "https://www.pgurus.com/"},
        #{"name": "PrecisionAg", "url": "https://www.precisionag.com/feed/"},
    ],
}

# ==================== IMPROVED SCRAPER ====================
def scrape_site(url, limit=8):
    articles = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try multiple common patterns
        selectors = [
            'article', 
            'div.article', 
            'div.post', 
            'div.story', 
            'div.news-item',
            'li',
            'div.card'
        ]

        found = []
        for sel in selectors:
            found.extend(soup.select(sel))

        for item in found[:limit * 4]:
            title_tag = item.find(['h1', 'h2', 'h3', 'h4', 'a'])
            if title_tag:
                title = title_tag.get_text().strip()
                link = title_tag.get('href') if title_tag.name == 'a' else None
                
                if not link:
                    link_tag = item.find('a', href=True)
                    link = link_tag['href'] if link_tag else url

                if not link.startswith('http'):
                    link = url.rstrip('/') + '/' + link.lstrip('/')

                if len(title) > 15:
                    articles.append({
                        'title': title[:130],
                        'link': link,
                        'summary': 'Click to read the full article',
                        'published': '',
                        'pub_ts': time.time(),
                        'source': url.split('//')[-1].split('/')[0],
                        'image': None
                    })
                    if len(articles) >= limit:
                        break

    except Exception as e:
        print(f"Scraping error for {url}: {e}")

    return articles

# ==================== ROUTES ====================
@app.route('/')
def index():
    return render_template('index.html', categories=list(CATEGORIES.keys()))

@app.route('/api/categories')
def api_categories():
    return jsonify(list(CATEGORIES.keys()))

@app.route('/api/news')
def api_news():
    category = request.args.get('category', list(CATEGORIES.keys())[0])

    if category == "Custom Scraped":
        all_articles = []
        for item in CATEGORIES["Custom Scraped"]:
            arts = scrape_site(item["url"], limit=8)
            for a in arts:
                a['source'] = item["name"]
                all_articles.append(a)
        all_articles.sort(key=lambda x: x.get('pub_ts', 0), reverse=True)
        return jsonify({'category': category, 'count': len(all_articles), 'articles': all_articles[:25]})

    if category not in CATEGORIES:
        return jsonify({'error': 'Invalid category'}), 400

    all_articles = []
    for feed_info in CATEGORIES[category]:
        try:
            feed = feedparser.parse(feed_info['url'])
            for entry in feed.entries[:8]:
                # Image extraction
                image_url = None
                if 'media_thumbnail' in entry and entry.media_thumbnail:
                    image_url = entry.media_thumbnail[0].get('url')
                elif 'enclosures' in entry and entry.enclosures:
                    for enc in entry.enclosures:
                        if 'image' in str(enc.get('type', '')):
                            image_url = enc.get('href') or enc.get('url')
                            break

                all_articles.append({
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', '#'),
                    'summary': entry.get('summary', '')[:280],
                    'published': entry.get('published', ''),
                    'pub_ts': time.mktime(entry.published_parsed) if entry.get('published_parsed') else 0,
                    'source': feed_info['name'],
                    'image': image_url
                })
        except:
            pass

    all_articles.sort(key=lambda x: x.get('pub_ts', 0), reverse=True)
    return jsonify({'category': category, 'count': len(all_articles), 'articles': all_articles[:25]})

if __name__ == '__main__':
    print("🚀 Starting Clarity Portal")
    app.run(host='127.0.0.1', port=5000, debug=True)