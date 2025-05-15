"""
API module. Uses FastAPI.
"""

import os
import time
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Setup django first before importing any module that will require any of its resource

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
import django

django.setup()

from api.v1 import router as v1_router
from project.settings import (
    STATIC_URL,
    MEDIA_URL,
    STATIC_ROOT,
    MEDIA_ROOT,
    FRONTEND_DIR,
    env_setting,
)

api_module_path = Path(__file__).parent

app = FastAPI(
    title=f"{env_setting.SITE_NAME}  - API",
    version=api_module_path.joinpath("VERSION").read_text().strip(),
    description=api_module_path.joinpath("README.md").read_text(),
    license_info={
        "name": f"{env_setting.LICENSE} License",
        "url": f"{env_setting.REPOSITORY_LINK}refs/heads/main/LICENSE",
    },
    docs_url=f"{env_setting.API_PREFIX}/docs",
    redoc_url=f"{env_setting.API_PREFIX}/redoc",
    openapi_url=f"{env_setting.API_PREFIX}/openapi.json",
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response: Response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Mount static & media files
app.mount(STATIC_URL[:-1], StaticFiles(directory=STATIC_ROOT), name="static")
app.mount(MEDIA_URL[:-1], StaticFiles(directory=MEDIA_ROOT), name="media")

from django.core.handlers.wsgi import WSGIHandler

from fastapi.middleware.wsgi import WSGIMiddleware

# Include API router
app.include_router(v1_router, prefix=env_setting.API_PREFIX)

# Mount django for admin & account creation views ie. /d/admin & /d/user/* etc
app.mount("/d", app=WSGIMiddleware(WSGIHandler()), name="django")

if FRONTEND_DIR:
    # TODO: Incase of using React, implement a unified approach of handling these requests
    # Such that when user refreshes the page it will not return 404
    def get_index_reponse():
        file_path = FRONTEND_DIR / "index.html"
        if file_path.exists():
            return Response(content=file_path.read_text(), media_type="text/html")
        return Response(content="index.html not found", status_code=404)

    @app.get("/{path}", name="React requests hit here", include_in_schema=False)
    def serve_react_app(path: str):
        return get_index_reponse()

    @app.get(
        "/dashboard/{path}", name="React requests hit here", include_in_schema=False
    )
    def serve_react_app_dashboard(path: str):
        return get_index_reponse()

    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
