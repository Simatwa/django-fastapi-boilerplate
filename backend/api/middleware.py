import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from project.settings import env_setting


def register_middlewares(app: FastAPI) -> FastAPI:
    # Add your middlewares here

    app.add_middleware(
        CORSMiddleware,
        allow_origins=env_setting.cors_allowed_origins,
        allow_credentials=env_setting.CORS_ALLOW_CREDENTIALS,
        allow_methods=env_setting.CORS_ALLOW_METHODS,
        allow_headers=env_setting.CORS_ALLOW_HEADERS,
        allow_origin_regex=(
            env_setting.CORS_ALLOWED_ORIGIN_REGEXES[0]
            if env_setting.CORS_ALLOWED_ORIGIN_REGEXES
            else None
        ),  # TODO: Consider merging regexes
    )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    return app
