from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.db import crud
from backend.app.services.youtube_ingest import ingest_youtube
from backend.app.services.instagram_ingest import ingest_instagram

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.post("/ingest/youtube")
async def ingest_youtube_data(user_id: int, db: Session = Depends(get_db)):
    accounts = crud.get_social_accounts(db, user_id)

    yt_accounts = [acc for acc in accounts if acc.platform.lower() == "youtube"]
    if not yt_accounts:
        raise HTTPException(status_code=404, detail="No connected YouTube accounts found")

    for acc in yt_accounts:
        await ingest_youtube(db=db, account=acc)

    return {"status": "completed", "platform": "youtube", "ingested_accounts": len(yt_accounts)}


@router.post("/ingest/instagram")
async def ingest_instagram_data(user_id: int, db: Session = Depends(get_db)):
    accounts = crud.get_social_accounts(db, user_id)

    ig_accounts = [acc for acc in accounts if acc.platform.lower() == "instagram"]
    if not ig_accounts:
        raise HTTPException(status_code=404, detail="No connected Instagram accounts found")

    for acc in ig_accounts:
        await ingest_instagram(db=db, account=acc)

    return {"status": "completed", "platform": "instagram", "ingested_accounts": len(ig_accounts)}

@router.post("/ingest/all")
async def ingest_all_platforms(user_id: int, db: Session = Depends(get_db)):
    accounts = crud.get_social_accounts(db, user_id)

    if not accounts:
        raise HTTPException(status_code=404, detail="No connected social accounts found")

    for acc in accounts:
        if acc.platform.lower() == "youtube":
            await ingest_youtube(db=db, account=acc)
        elif acc.platform.lower() == "instagram":
            await ingest_instagram(db=db, account=acc)

    return {"status": "completed", "platforms_synced": list(set([acc.platform for acc in accounts]))}


@router.get("/overview")
def analytics_overview(user_id: int, db: Session = Depends(get_db)):
    """
    Returns summary analytics for dashboard display
    """
    posts = crud.get_all_posts_with_analytics(db, user_id)

    if not posts:
        return {"message": "No analytics data available yet"}

    total_posts = len(posts)
    total_views = sum(p.views for p in posts)
    total_likes = sum(p.likes for p in posts)
    total_comments = sum(p.comments for p in posts)

    top_post = max(posts, key=lambda p: p.views)

    return {
        "total_posts": total_posts,
        "total_views": total_views,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "top_post": {
            "caption": top_post.caption,
            "views": top_post.views,
            "likes": top_post.likes,
            "posted_at": top_post.posted_at,
        }
    }

@router.get("/timeseries")
def engagement_timeseries(user_id: int, db: Session = Depends(get_db)):
    """
    Returns time-series data for charts
    """
    posts = crud.get_all_posts_with_analytics(db, user_id)

    if not posts:
        return {"message": "No analytics history available yet"}

    timeseries = [
        {
            "posted_at": p.posted_at,
            "views": p.views,
            "likes": p.likes,
            "comments": p.comments,
            "engagement_score": (p.likes + p.comments) / max(p.views, 1)
        }
        for p in sorted(posts, key=lambda x: x.posted_at)
    ]

    return {"timeline": timeseries}
