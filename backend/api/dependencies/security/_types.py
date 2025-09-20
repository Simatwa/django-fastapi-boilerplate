from datetime import datetime

from pydantic import BaseModel, Field


class TurnstileVerificationResponse(BaseModel):
    class Metadata(BaseModel):
        ephemeral_id: str

    success: bool
    error_codes: list[str] = Field(alias="error-codes")
    challenge_ts: datetime | None = None
    action: str | None = None
    cdata: str | None = None
    metadata: Metadata | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "challenge_ts": "2022-02-28T15:14:30.096Z",
                "hostname": "example.com",
                "error-codes": [],
                "action": "login",
                "cdata": "sessionid-123456789",
                "metadata": {"ephemeral_id": "x:9f78e0ed210960d7693b167e"},
            }
        }


class TurnstileToken(BaseModel):
    turnstile_token: str
