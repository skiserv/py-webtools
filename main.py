from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from pywebtools.routers import notes, lists
from pywebtools.templating import templates

app = FastAPI()
app.include_router(notes.router)
app.include_router(lists.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
