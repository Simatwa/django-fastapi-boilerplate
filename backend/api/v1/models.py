"""Models for v1"""

from typing import Any

from pydantic import BaseModel, Field


class ProcessFeedback(BaseModel):
    detail: Any = Field(description="Feedback in details")

    class Config:
        json_schema_extra = {
            "example": {"detail": "This is a detailed feedback message."}
        }
