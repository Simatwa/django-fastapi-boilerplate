from pydantic import BaseModel, HttpUrl
from typing import Optional
from management.models import MessageCategory, Concern
from external.models import ServiceFeedback
from datetime import datetime


class GroupInfo(BaseModel):
    name: str
    description: str
    social_media_link: HttpUrl
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Tech Enthusiasts",
                "description": "A group for people passionate about technology and innovation.",
                "social_media_link": "https://www.linkedin.com/groups/123456/",
                "created_at": "2025-04-18T22:21:43.609831Z",
            },
        }


class PersonalMessageInfo(BaseModel):
    id: int
    category: MessageCategory
    subject: str
    content: str
    created_at: datetime
    is_read: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id": 26,
                "category": "General",
                "subject": "Welcome Package Update",
                "content": (
                    "We've updated our welcome package with new amenities and services."
                    " Please review the attached document."
                ),
                "created_at": "2025-04-18T22:21:43.609831Z",
                "is_read": False,
            },
        }


class GroupMessageInfo(PersonalMessageInfo):
    pass


class NewConcern(BaseModel):
    about: str
    details: str

    class Config:
        json_schema_extra = {
            "example": {
                "about": "Service Quality",
                "details": "The service was not up to the expected standards.",
            },
        }


class ShallowConcernDetails(BaseModel):
    id: int
    about: str
    status: Concern.ConcernStatus
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 101,
                "about": "Service Quality",
                "status": "Pending",
                "created_at": "2025-04-18T22:21:43.609831Z",
            },
        }


class ConcernDetails(ShallowConcernDetails):
    details: str
    response: Optional[str] = None
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "id": 101,
                "about": "Service Quality",
                "status": "Resolved",
                "created_at": "2025-04-18T22:21:43.609831Z",
                "details": "The service was not up to the expected standards.",
                "response": "We apologize for the inconvenience and have taken corrective measures.",
                "updated_at": "2025-04-20T10:15:30.123456Z",
            },
        }


class UpdateConcern(BaseModel):
    about: Optional[str] = None
    details: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "about": "Service Quality",
                "details": "The service was not up to the expected standards.",
            },
        }


class NewUserFeedback(BaseModel):
    message: str
    rate: ServiceFeedback.FeedbackRate

    class Config:
        json_schema_extra = {
            "example": {
                "message": "The service was excellent and exceeded expectations.",
                "rate": "Excellent",
            },
        }


class UserFeedbackDetails(NewUserFeedback):
    created_at: datetime
    updated_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "message": "The service was excellent and exceeded expectations.",
                "rate": 5,
                "created_at": "2025-04-18T22:21:43.609831Z",
                "updated_at": "2025-04-19T08:30:00.123456Z",
            },
        }
