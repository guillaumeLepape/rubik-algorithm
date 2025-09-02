from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .models import COFP_ALGORITHMS

templates_dir = (Path(__file__).parents[1] / "templates").resolve()
templates = Jinja2Templates(directory=str(templates_dir))


def create_app() -> FastAPI:
    app = FastAPI(title="CFOP Algorithms", description="Learn CFOP speedcubing algorithms")

    static_files_dir = (Path(__file__).parents[1] / "static").resolve()
    app.mount("/static", StaticFiles(directory=static_files_dir), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def home(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(
            request=request, name="home.html", context={"cofp_algorithms": COFP_ALGORITHMS}
        )

    return app
