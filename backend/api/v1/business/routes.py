from fastapi import APIRouter, Query, HTTPException, status
from fastapi.encoders import jsonable_encoder
from external.models import About, Message, FAQ, ServiceFeedback, Gallery, Document
from management.models import AppUtility

from api.v1.utils import send_email

from api.v1.models import ProcessFeedback
from api.v1.business.models import (
    BusinessAbout,
    NewVisitorMessage,
    BusinessGallery,
    FAQDetails,
    ShallowUserInfo,
    UserFeedback,
    DocumentInfo,
    AppUtilityInfo,
)
from typing import Annotated
import asyncio

router = APIRouter(prefix="/business", tags=["Business"])


@router.get("/about", name="Business information")
async def get_business_details() -> BusinessAbout:
    about = await About.objects.all().alast()
    if about is not None:
        return jsonable_encoder(about)
    raise HTTPException(status_code=404, detail="Business detail is not yet available.")


# GENERAL SITE DATA

# TODO: Implement routers for exposing the general site data


@router.post("/visitor-message", name="New visitor message")
async def new_visitor_message(message: NewVisitorMessage) -> ProcessFeedback:
    new_message = await Message.objects.acreate(**message.model_dump())
    await new_message.asave()
    await asyncio.to_thread(
        send_email,
        **dict(
            subject="Message Received Confirmation",
            recipient=new_message.email,
            template_name="email/message_received_confirmation",
            context=dict(message=new_message),
        ),
    )
    return ProcessFeedback(detail="Message received succesfully.")


@router.get("/galleries", name="Business galleries")
async def get_business_galleries() -> list[BusinessGallery]:
    return [
        jsonable_encoder(gallery)
        async for gallery in Gallery.objects.filter(show_in_index=True).all().order_by("-created_at")[:12]
    ]


@router.get("/feedbacks", name="Customers' feedback")
async def get_client_feedbacks() -> list[UserFeedback]:
    """Get customers' feedback"""
    feedbacks = ServiceFeedback.objects.filter(show_in_index=True).order_by("-created_at").all()[:6]
    feedback_list = []
    async for feedback in feedbacks:
        feedback_dict = jsonable_encoder(feedback)
        feedback_dict["user"] = ShallowUserInfo(**feedback.sender.model_dump())
        feedback_list.append(UserFeedback(**feedback_dict))
    return feedback_list


@router.get("/faqs", name="Frequently asked questions")
async def get_faqs() -> list[FAQDetails]:
    """Get frequently asked question"""
    return [
        FAQDetails(**jsonable_encoder(faq))
        async for faq in FAQ.objects.filter(is_shown=True).order_by("created_at").all()[:10]
    ]


@router.get("/document", name="Site document")
async def get_site_document(
    name: Annotated[Document.DocumentName, Query(description="Document name")],
) -> DocumentInfo:
    """Get site document such as Policy, ToS etc"""
    document = await Document.objects.filter(name=name.value).alast()
    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document has not yet been created.",
        )
    return document.model_dump()


@router.get("/app/utilities", name="App utilities")
async def get_app_utilities(
    name: Annotated[AppUtility.UtilityName, Query(description="Name filter")] = None,
) -> list[AppUtilityInfo]:
    """Get app utilities such as currency etc"""
    search_filter = dict()
    if name is not None:
        search_filter["name"] = name.value
    return [jsonable_encoder(utility) async for utility in AppUtility.objects.filter(**search_filter).all()]
