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
        {"name": "The Times Of India-Bangalore", "url": "https://timesofindia.indiatimes.com/rssfeeds/-2128833038.cms"},
        {"name": "The Times Of India-Most Read", "url": "https://timesofindia.indiatimes.com/rssfeedmostread.cms"},
    ],
    "Technology": [
        {"name": "WIRED", "url": "https://www.wired.com/feed/rss"},
        {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index"},
        {"name": "Times Of India - Tech", "url": "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms"},
        {"name": "Tech Crunch", "url": "https://techcrunch.com/feed/"},
        {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml"},
        {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/"},
    ],
    "AI & Innovations": [
        {"name": "WIRED AI", "url": "https://www.wired.com/feed/tag/ai/latest/rss"},
        {"name": "Quanta Magazine", "url": "https://api.quantamagazine.org/feed/"},
        {"name": "Mark Tech Post", "url": "https://www.marktechpost.com/feed/"},
        {"name": "arXiv cs.AI", "url": "https://arxiv.org/rss/cs.AI"},
    ],
    "Science & Mathematics": [
        {"name": "Quanta Magazine", "url": "https://api.quantamagazine.org/feed/"},
        {"name": "Khan Academy", "url": "https://blog.khanacademy.org/feed/"},
        {"name": "BBC Science", "url": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml"},
        {"name": "WIRED Science", "url": "https://www.wired.com/feed/category/science/latest/rss"},
    ],
    "Geopolitics & World": [
        {"name": "Foreign Affairs", "url": "https://www.foreignaffairs.com/rss.xml"},
        {"name": "Foreign Policy", "url": "https://foreignpolicy.com/feed/"},
        {"name": "War on the Rocks", "url": "https://warontherocks.com/feed/"},
        {"name": "The Times Of India-World", "url": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms"},
    ],
    "Economy & Stock Market": [
        {"name": "The Economic Times - India", "url": "https://economictimes.indiatimes.com/rssfeeds/13352306.cms"},
        {"name": "Seeking Alpha", "url": "https://seekingalpha.com/feed.xml"},
        {"name": "Freefincal", "url": "https://freefincal.com/feed/"},
    ],
    "Sports": [
        {"name": "BBC Sport", "url": "https://feeds.bbci.co.uk/sport/rss.xml"},
        {"name": "The Hindu - Sport", "url": "https://www.thehindu.com/sport/feeder/default.rss"},
        {"name": "Times Of India - Sports", "url": "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms"},
    ],
    "History, Legends & Heritage": [
        {"name": "Smithsonian", "url": "https://www.smithsonianmag.com/feed/"},
        {"name": "The Marginalian", "url": "https://www.themarginalian.org/feed/"},
    ],
    "Podblogs": [
        {"name": "Tim Ferriss", "url": "https://tim.blog/feed/"},
        {"name": "Lex Fridman", "url": "https://lexfridman.com/feed/podcast/"},
        {"name": "Astralcodex Ten", "url": "https://astralcodexten.substack.com/feed"},
    ],
    "Education": [
        {"name": "Khan Academy", "url": "https://blog.khanacademy.org/feed/"},
    ],
    "Agri Tech": [
        {"name": "The Better India", "url": "https://www.thebetterindia.com/feed/"},
        {"name": "AgFunderNews", "url": "https://agfundernews.com/feed/"},
    ],
    "Custom Scraped": [
        {"name": "MoneyLife", "url": "https://www.moneylife.in/"},
        {"name": "ESPN Cricinfo", "url": "https://www.espncricinfo.com/"},
        {"name": "PGurus", "url": "https://www.pgurus.com/"},
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