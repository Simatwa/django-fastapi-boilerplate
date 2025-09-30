"""
API module. Uses FastAPI.
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
from django.core.handlers.asgi import ASGIHandler

django.setup()

# Setup django first before importing any module that will require
# any of its resource

from fastapi import (  # noqa: E402
    FastAPI,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.responses import JSONResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from project.settings import (  # noqa: E402
    FRONTEND_DIR,
    MEDIA_ROOT,
    MEDIA_URL,
    STATIC_ROOT,
    STATIC_URL,
    env_setting,
)

from api.common import api_description, api_version  # noqa: E402
from api.middleware import register_middlewares  # noqa: E402
from api.v1 import router as v1_router  # noqa: E402

fastapi = FastAPI(
    title=f"{env_setting.SITE_NAME}  - API",
    version=api_version,
    description=api_description,
    license_info={
        "name": f"{env_setting.LICENSE} License",
        "url": f"{env_setting.REPOSITORY_LINK}refs/heads/main/LICENSE",
    },
    docs_url=f"{env_setting.API_PREFIX}/docs",
    redoc_url=f"{env_setting.API_PREFIX}/redoc",
    openapi_url=f"{env_setting.API_PREFIX}/openapi.json",
)

app = register_middlewares(fastapi)

# Mount static & media files
app.mount(STATIC_URL[:-1], StaticFiles(directory=STATIC_ROOT), name="static")
app.mount(MEDIA_URL[:-1], StaticFiles(directory=MEDIA_ROOT), name="media")


# Include API router
app.include_router(v1_router, prefix=env_setting.API_PREFIX)

# Mount django for admin & account creation views ie. /d/admin & /d/user/* etc
app.mount(env_setting.DJANGO_PREFIX, app=ASGIHandler(), name="django")

if FRONTEND_DIR:
    index_file_content = (FRONTEND_DIR / "index.html").read_text()

    @app.exception_handler(status.HTTP_404_NOT_FOUND)
    async def custom_http_exception_handler(
        request: Request, exc: HTTPException
    ):
        if not request.url.path.startswith(env_setting.API_PREFIX):
            return Response(content=index_file_content, media_type="text/html")

        return JSONResponse(
            content={"detail": exc.detail},
            status_code=status.HTTP_404_NOT_FOUND,
            media_type="application/json",
        )

    app.mount(
        "/",
        StaticFiles(directory=FRONTEND_DIR, html=True),
        name="frontend",
    )
