from pydantic import BaseModel, Field, field_validator, Field, EmailStr, HttpUrl
from external.models import ServiceFeedback
from management.models import AppUtility
from typing import Optional
from datetime import date, datetime
from api.v1.utils import get_document_path


class BusinessAbout(BaseModel):
    name: str
    short_name: str
    details: str
    slogan: str
    address: str
    founded_in: date
    email: Optional[str] = None
    phone_number: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    tiktok: Optional[str] = None
    youtube: Optional[str] = None
    logo: Optional[str] = None
    wallpaper: Optional[str] = None

    @field_validator("logo", "wallpaper")
    def validate_cover_photo(value):
        return get_document_path(value)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Library Management System",
                "short_name": "Library MS",
                "details": "Welcome to our Library Management System. We are committed to providing seamless access to books and resources for our community.",
                "slogan": "Empowering knowledge, one book at a time.",
                "address": "456 Knowledge Lane, Nairobi - Kenya",
                "founded_in": "2023-01-01",
                "email": "admin@libraryms.com",
                "phone_number": "+254722222222",
                "facebook": "https://www.facebook.com/libraryms",
                "twitter": "https://www.x.com/libraryms",
                "linkedin": "https://www.linkedin.com/company/libraryms",
                "instagram": "https://www.instagram.com/libraryms",
                "tiktok": "https://www.tiktok.com/@libraryms",
                "youtube": "https://www.youtube.com/libraryms",
                "logo": "/media/default/library_logo.png",
                "wallpaper": "/media/default/library_wallpaper.jpg",
            }
        }


class NewVisitorMessage(BaseModel):
    sender: str
    email: EmailStr
    body: str

    class Config:
        json_schema_extra = {
            "example": {
                "sender": "Jane Doe",
                "email": "jane.doe@example.com",
                "body": "I would like to inquire about your rental services.",
            }
        }


class ShallowUserInfo(BaseModel):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "first_name": "John",
                "last_name": "Doe",
                "profile": "/media/custom_user/profile.jpg",
            }
        }


class UserFeedback(BaseModel):
    user: ShallowUserInfo
    sender_role: ServiceFeedback.SenderRole
    message: str
    rate: ServiceFeedback.FeedbackRate
    created_at: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "sender_role": "Member",
                "message": "Great service!",
                "rate": "Excellent",
                "created_at": "2023-01-01T00:00:00",
                "user": {
                    "username": "johndoe",
                    "first_name": "John",
                    "last_name": "Doe",
                    "profile": "/media/custom_user/profile.jpg",
                },
            }
        }


class BusinessGallery(BaseModel):
    title: str
    details: str
    location_name: str
    youtube_video_link: Optional[HttpUrl] = Field(
        None, description="Youtube video link"
    )
    picture: Optional[str] = None
    date: date

    @field_validator("picture")
    def validate_file(value):
        return get_document_path(value)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Library Tour",
                "details": "A virtual tour of our main library facility.",
                "location_name": "Main Library",
                "youtube_video_link": "https://www.youtube.com/watch?v=example123",
                "picture": "/media/gallery/main-library-tour.jpg",
                "date": "2024-01-01",
            }
        }


class FAQDetails(BaseModel):
    question: str
    answer: str

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Can I suggest new books for the library to add?",
                "answer": (
                    "Yes, you can submit book suggestions through the 'Suggest a Book' "
                    "feature available in your account dashboard.",
                ),
            }
        }


class DocumentInfo(BaseModel):
    name: str
    content: str
    updated_at: datetime


class AppUtilityInfo(BaseModel):
    name: AppUtility.UtilityName
    description: str
    value: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Currency",
                "description": "<p>Transaction Currency</p>",
                "value": "$",
            }
        }


# TODO: Further business Models
