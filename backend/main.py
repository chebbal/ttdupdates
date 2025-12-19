from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from scraper import get_latest_updates
import os

app = FastAPI(title="TTD Updates Notifier")

class UpdateItem(BaseModel):
    id: Optional[int]
    message: Optional[str]
    cta: Optional[str]
    link: Optional[str]

@app.get("/")
def read_root():
    return {"message": "Welcome to TTD Updates Notifier API. Use /updates to fetch latest info."}

@app.get("/updates", response_model=List[UpdateItem])
def get_updates():
    """Trigger the scraper and return latest updates."""
    updates = get_latest_updates()
    if updates is None:
        raise HTTPException(status_code=500, detail="Failed to fetch updates")
    return updates

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
