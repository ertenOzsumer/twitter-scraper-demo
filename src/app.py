from fastapi import FastAPI, HTTPException
from .schemas import ScrapeRequest, Report
from .ingest import handle_from_url, get_user_id, get_tweets
from .analytics import normalize, summarize
from .export_utils import export_csv, export_xlsx, export_pdf
from pathlib import Path

app = FastAPI(title="Twitter/X Analytics Scraper")

@app.post("/scrape", response_model=Report)
async def scrape(req: ScrapeRequest):
    try:
        handle = handle_from_url(req.profile_url)
        user_id = await get_user_id(handle)
        raw = await get_tweets(user_id, req.period.from_, req.period.to)
        rows = [normalize(t) for t in raw]
        agg = summarize(rows)
        report = {
            "profile": {"handle": handle, "user_id": user_id, "verified": None},
            "period": {"from_": req.period.from_, "to": req.period.to},
            **agg,
            "tweets": rows
        }
        out = Path("out"); out.mkdir(exist_ok=True)
        export_csv(rows, out / "tweets.csv")
        export_xlsx(rows, out / "tweets.xlsx")
        export_pdf(report, out / "report.pdf")
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
