# demo/demo_twitter_scraper.py
import os, csv, argparse, requests
from datetime import datetime, timedelta

BASE = "https://api.twitter.com/2"

def headers():
    return {"Authorization": f"Bearer {os.getenv('TWITTER_BEARER_TOKEN')}"}

def get_user_id(username: str) -> str:
    r = requests.get(f"{BASE}/users/by/username/{username}", headers=headers())
    r.raise_for_status()
    return r.json()["data"]["id"]

def get_recent_tweets(user_id: str, days: int):
    start = (datetime.utcnow() - timedelta(days=days)).isoformat("T") + "Z"
    params = {"max_results": 100, "start_time": start, "tweet.fields":"created_at,public_metrics,lang"}
    r = requests.get(f"{BASE}/users/{user_id}/tweets", headers=headers(), params=params)
    r.raise_for_status()
    return r.json().get("data", [])

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--username", required=True)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--out", default="tweets.csv")
    args = ap.parse_args()

    uid = get_user_id(args.username)
    tweets = get_recent_tweets(uid, args.days)

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id","created_at","lang","likes","retweets","replies","quotes","text"])
        for t in tweets:
            m = t.get("public_metrics", {})
            w.writerow([t["id"], t["created_at"], t.get("lang"),
                        m.get("like_count",0), m.get("retweet_count",0),
                        m.get("reply_count",0), m.get("quote_count",0),
                        t.get("text","").replace("\n"," ")])
    print(f"Saved {len(tweets)} tweets → {args.out}")
