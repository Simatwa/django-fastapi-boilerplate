"""
Processes captcha validation using Cloudflare's Turnstile

Reference: https://developers.cloudflare.com/turnstile/get-started/server-side-validation/
"""

import re

import httpx
from fastapi import HTTPException, Request, status
from project.settings import env_setting

from ._types import TurnstileVerificationResponse
from .exceptions import InvalidSecretError

DEFAULT_TOKEN_KEY = "turnstile_token"
VERIFICATION_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

EXCLUDED_REMOTE_ADDR_PATTERN = re.compile(r"^(192\.168\.|10\.|127\.)")


class TurnstileToken:
    """Extracts turnstile token from request `json/form`"""

    def __init__(
        self, token_key: str = DEFAULT_TOKEN_KEY, auto_error: bool = True
    ):
        self.token_key = token_key
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> str | None:
        request_json: dict = await request.json()

        token = request_json.get(self.token_key)

        if token is None:
            # Try to extract from form data
            request_form: dict = await request.form()
            token = request_form.get(self.token_key)

        if not token:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=(f"Missing captcha token - {self.token_key}"),
                )
            else:
                return None

        return token


async def validate_turnstile_token(
    token: str, request: Request, auto_error: bool
) -> TurnstileVerificationResponse:
    assert env_setting.TURNSTILE_SECRET_KEY is not None, (
        "TURNSTILE_SECRET_KEY is empty. Declare its value in .env file"
    )
    payload = {"secret": env_setting.TURNSTILE_SECRET_KEY, "response": token}

    remote_ip = (
        request.headers.get("CF-Connecting-IP")
        or request.headers.get("X-Forwarded-For")
        or request.client.host
    )

    if not EXCLUDED_REMOTE_ADDR_PATTERN.match(remote_ip):
        payload["remote_ip"] = remote_ip

    async_client = httpx.AsyncClient()

    resp = await async_client.post(
        VERIFICATION_URL,
        data=payload,
    )

    if auto_error:
        if resp.status_code == status.HTTP_400_BAD_REQUEST:
            raise InvalidSecretError(
                resp.json(),
                (
                    f"Is your secret value '{env_setting.TURNSTILE_SECRET_KEY}'"
                    " really correct?"
                ),
            )

        resp.raise_for_status()

    return TurnstileVerificationResponse(**resp.json())


class CaptchaRequired:
    """Dependency that validates turnstile token

    #### Usage

    ```python
    @router.post("/new-post")
    async def new_post(
    token: TurnstileToken,
    captcha_info: Annotated[object, Depends(CaptchaRequired()],
    ) -> dict:
    ...
    """

    def __init__(
        self,
        token_key: str = DEFAULT_TOKEN_KEY,
        auto_error: bool = True,
        ensure_successful: bool = True,
    ):
        self.turnstile_token = TurnstileToken(
            token_key=token_key, auto_error=auto_error
        )
        self.ensure_successful = ensure_successful

    async def __call__(
        self, request: Request
    ) -> TurnstileVerificationResponse | None:
        token = await self.turnstile_token(request)

        if token is not None:
            verification = await validate_turnstile_token(
                token, request, self.ensure_successful
            )

            if self.ensure_successful:
                if not verification.success:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=(
                            f"Invalid or missing captcha token - "
                            f"{self.turnstile_token.token_key}"
                        ),
                    )

            return verification
