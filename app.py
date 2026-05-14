from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database.db import db
from config.config import Config
from api.jikan import jikan

app = FastAPI(title="ANIZONEFLIX")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Context processor for global variables
@app.middleware("http")
async def add_global_vars(request: Request, call_next):
    request.state.logo_url = Config.LOGO_URL
    request.state.site_name = "ANIZONEFLIX"
    response = await call_next(request)
    return response

@app.get("/")
async def index(request: Request):
    trending = await db.get_all_anime(limit=10)
    recent = await db.get_all_anime(limit=20)
    return templates.TemplateResponse(request=request, name="index.html", context={
        "trending": trending,
        "recent": recent,
        "logo_url": Config.LOGO_URL,
        "site_name": "ANIZONEFLIX"
    })

@app.get("/anime/{slug}")
async def anime_detail(request: Request, slug: str):
    anime = await db.get_anime_by_slug(slug)
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    return templates.TemplateResponse(request=request, name="details.html", context={
        "anime": anime,
        "logo_url": Config.LOGO_URL,
        "site_name": "ANIZONEFLIX"
    })

@app.get("/search")
async def search_web(request: Request, q: str = ""):
    results = await db.search_anime_db(q)
    return templates.TemplateResponse(request=request, name="search.html", context={
        "results": results,
        "query": q,
        "logo_url": Config.LOGO_URL,
        "site_name": "ANIZONEFLIX"
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
