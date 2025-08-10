from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict

class Period(BaseModel):
    from_: str  # ISO date
    to: str     # ISO date

class ScrapeRequest(BaseModel):
    profile_url: HttpUrl
    period: Period

class TweetItem(BaseModel):
    tweet_id: str
    timestamp: str
    text: str
    lang: Optional[str]
    likes: int
    retweets: int
    replies: int
    quotes: int
    is_retweet: bool
    is_reply: bool
    is_quote: bool
    hashtags: List[str] = []

class Report(BaseModel):
    profile: Dict
    period: Period
    metrics: Dict
    top_hashtags: List[Dict]
    top_keywords: List[Dict]
    tweets: List[TweetItem]
