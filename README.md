# Clarity Portal - Complete Version

Your personal authentic news aggregator with RSS + Custom Scraping.

## Features
- All your categories (Technology, AI, Science, Geopolitics, Economy, Sports, History, Podblogs, Education, Agri Tech)
- **Custom Scraped** tab for sites without RSS (MoneyLife, Cricinfo, PGurus)
- Clean modern UI
- Search across articles
- Easy to extend

## How to Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Deploy on Render (Free)

1. Push this folder to GitHub
2. Go to render.com → New Web Service
3. Connect your repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`
6. Deploy!

Your app will be live at `https://your-app.onrender.com`

## How to Add More Feeds

Edit `CATEGORIES` in `app.py`.

For new scraped sites, add to the `"Custom Scraped"` list.

Enjoy your clean personal news portal! 🚀
