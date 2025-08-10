# Twitter/X Analytics Scraper (API-first, Python)

Production-ready starter to fetch **public metrics** from Twitter/X, compute analytics (hashtags, keywords, KPIs), and export to **CSV/XLSX/PDF**. Arabic & English supported.

> ⚠️ **Note:** Bookmarks count is not publicly available via API and is excluded.

## Features
- API-first architecture with **FastAPI**
- Accurate public metrics via **Twitter API v2**
- Arabic & English text analytics (UTF-8, basic normalization)
- Exports: **CSV**, **Excel (XLSX)**, **PDF**
- Ready for **Docker** deployment
- Minimal **demo script** included (`demo/demo_twitter_scraper.py`)

## Endpoints
- `POST /scrape` → `{ profile_url, period: { from, to } }`
- `GET  /report/{job_id}` → JSON analytics + links for CSV/XLSX/PDF

## Quickstart

```bash
git clone https://github.com/ertenOzsumer/twitter-scraper-demo.git
cd twitter-x-analytics-scraper
cp .env.example .env   # add your TWITTER_BEARER_TOKEN
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.app:app --reload
```

**Run demo:**
```bash
export TWITTER_BEARER_TOKEN="YOUR_TOKEN"
python demo/demo_twitter_scraper.py --username TwitterDev --days 7
```

## Tech Stack
- Python: FastAPI, httpx, pandas, pydantic
- PDF: WeasyPrint/ReportLab (you can choose one; WeasyPrint is used here)
- Optional: Playwright (fallback only), proxies, APScheduler

## Roadmap
- Queue & job store (RQ/Celery)
- TF-IDF keyword scoring
- Media URL extraction
- Dashboard auth hooks
