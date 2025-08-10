import httpx
from typing import List, Dict
from urllib.parse import urlparse
from .settings import settings

BASE = "https://api.twitter.com/2"

def _headers():
    return {"Authorization": f"Bearer {settings.TWITTER_BEARER_TOKEN}"}

def handle_from_url(profile_url: str) -> str:
    # Accept https://x.com/<handle> or https://twitter.com/<handle>
    path = urlparse(profile_url).path.strip("/")
    return path.split("/")[0]

async def get_user_id(handle: str) -> str:
    url = f"{BASE}/users/by/username/{handle}"
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(url, headers=_headers())
        r.raise_for_status()
        return r.json()["data"]["id"]

async def get_tweets(user_id: str, start_iso: str, end_iso: str) -> List[Dict]:
    url = f"{BASE}/users/{user_id}/tweets"
    params = {
        "max_results": 100,
        "start_time": start_iso,
        "end_time": end_iso,
        "tweet.fields": "created_at,public_metrics,lang,referenced_tweets,entities"
    }
    tweets: List[Dict] = []
    async with httpx.AsyncClient(timeout=30) as client:
        while True:
            r = await client.get(url, headers=_headers(), params=params)
            r.raise_for_status()
            data = r.json()
            tweets.extend(data.get("data", []))
            meta = data.get("meta", {})
            if "next_token" not in meta:
                break
            params["pagination_token"] = meta["next_token"]
    return tweets
