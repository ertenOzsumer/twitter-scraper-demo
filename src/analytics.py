from collections import Counter
from typing import List, Dict
import re

def extract_hashtags(t: Dict) -> List[str]:
    ents = t.get("entities", {})
    items = ents.get("hashtags", []) or []
    return [h.get("tag","").lower() for h in items if h.get("tag")]

def normalize(tweet: Dict) -> Dict:
    pm = tweet.get("public_metrics", {})
    ref = tweet.get("referenced_tweets", []) or []
    kinds = {x.get("type") for x in ref}
    return {
        "tweet_id": tweet["id"],
        "timestamp": tweet["created_at"],
        "text": tweet.get("text",""),
        "lang": tweet.get("lang"),
        "likes": pm.get("like_count",0),
        "retweets": pm.get("retweet_count",0),
        "replies": pm.get("reply_count",0),
        "quotes": pm.get("quote_count",0),
        "is_retweet": "retweeted" in kinds,
        "is_reply": "replied_to" in kinds,
        "is_quote": "quoted" in kinds,
        "hashtags": extract_hashtags(tweet)
    }

def summarize(rows: List[Dict]) -> Dict:
    metrics = {
        "posts": len(rows),
        "likes": sum(r["likes"] for r in rows),
        "retweets": sum(r["retweets"] for r in rows),
        "replies": sum(r["replies"] for r in rows),
        "quotes": sum(r["quotes"] for r in rows),
    }
    all_tags = [t for r in rows for t in r["hashtags"]]
    top_hashtags = [{"tag": t, "count": c} for t, c in Counter(all_tags).most_common(10)]
    # simple keywords = split by word chars, filter very short tokens
    words = []
    for r in rows:
        words += [w.lower() for w in re.findall(r"\w+", r["text"]) if len(w) > 3]
    top_keywords = [{"term": t, "count": c} for t, c in Counter(words).most_common(10)]
    return {"metrics": metrics, "top_hashtags": top_hashtags, "top_keywords": top_keywords}
