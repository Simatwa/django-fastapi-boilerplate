"""Core routes"""

from typing import Annotated

from django.db.utils import IntegrityError
from external.models import ServiceFeedback
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Query,
    status,
)
from fastapi.encoders import jsonable_encoder
from management.models import (
    Concern,
    GroupMessage,
    MessageCategory,
    PersonalMessage,
)
from users.models import CustomUser

from api.v1.account.utils import get_user
from api.v1.core.models import (
    ConcernDetails,
    GroupMessageInfo,
    NewConcern,
    NewUserFeedback,
    PersonalMessageInfo,
    ShallowConcernDetails,
    UpdateConcern,
    UserFeedbackDetails,
)
from api.v1.models import ProcessFeedback
from api.v1.utils import get_value

router = APIRouter(prefix="/core", tags=["Core"])

# TODO: Implement your other routers here


@router.get("/personal/messages", name="Get personal messages")
async def get_personal_messages(
    user: Annotated[CustomUser, Depends(get_user)],
    is_read: Annotated[bool, Query(description="Is read filter")] = None,
    category: Annotated[
        MessageCategory, Query(description="Messages category")
    ] = None,
) -> list[PersonalMessageInfo]:
    """Messages that targets one user"""
    search_filter = dict(user=user)
    if is_read is not None:
        search_filter["is_read"] = is_read
    if category is not None:
        search_filter["category"] = category.value
    return [
        jsonable_encoder(message)
        async for message in PersonalMessage.objects.filter(**search_filter)
        .order_by("-created_at")
        .all()[:30]
    ]


@router.patch(
    "/personal/message/mark-read/{id}",
    name="Mark personal message as read",
)
async def mark_personal_message_read(
    id: Annotated[int, Path(description="Personal message ID")],
    user: Annotated[CustomUser, Depends(get_user)],
) -> ProcessFeedback:
    """Mark a personal message as read"""
    try:
        await PersonalMessage.objects.filter(id=id, user=user).aupdate(
            is_read=True
        )
        return ProcessFeedback(detail="Message marked as read successfully")
    except PersonalMessage.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with id {id} does not exist.",
        )


@router.get("/group/messages", name="Get group messages")
async def get_group_messages(
    user: Annotated[CustomUser, Depends(get_user)],
    is_read: Annotated[bool, Query(description="Is read filter")] = None,
    category: Annotated[
        MessageCategory, Query(description="Messages category")
    ] = None,
) -> list[GroupMessageInfo]:
    """Messages from unit group that user is a member"""
    message_list = []
    search_filter = dict(
        groups__in=[
            member_group async for member_group in user.member_groups.all()
        ]
    )
    if is_read is not None:
        if is_read:
            search_filter["read_by"] = user
        elif is_read is False:
            search_filter["read_by__isnull"] = True
    if category is not None:
        search_filter["category"] = category.value

    async for message in (
        GroupMessage.objects.prefetch_related("read_by")
        .filter(**search_filter)
        .order_by("-created_at")
        .all()[:30]
    ):
        message_dict = message.model_dump()
        message_dict["is_read"] = await message.read_by.acontains(user)
        message_list.append(message_dict)
    return message_list


@router.patch(
    "/group/message/mark-read/{id}", name="Mark group message as read"
)
async def mark_group_message_read(
    id: Annotated[int, Path(description="Group message ID")],
    user: Annotated[CustomUser, Depends(get_user)],
) -> ProcessFeedback:
    """Mark a particular group message as read"""
    try:
        target_message = await GroupMessage.objects.prefetch_related(
            "read_by"
        ).aget(
            id=id,
            groups__in=[
                member_group async for member_group in user.member_groups.all()
            ],
        )
        await target_message.read_by.aadd(user)
        return ProcessFeedback(detail="Message marked as read successfully.")
    except GroupMessage.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Community message with id {id} does not exist.",
        )


@router.get("/concerns", name="Get concerns")
async def get_concerns(
    user: Annotated[CustomUser, Depends(get_user)],
    status: Annotated[
        Concern.ConcernStatus, Query(description="Concern status")
    ] = None,
) -> list[ShallowConcernDetails]:
    """Get concerns ever sent"""
    search_filter = dict(user=user)
    if status is not None:
        search_filter["status"] = status.value
    return [
        jsonable_encoder(concern)
        async for concern in Concern.objects.filter(**search_filter)
        .order_by("-created_at")
        .all()[:30]
    ]


@router.post("/concern/new", name="Add new concern")
async def add_new_concern(
    concern: NewConcern, user: Annotated[CustomUser, Depends(get_user)]
) -> ConcernDetails:
    """Add new concern"""
    new_concern_dict = concern.model_dump()
    new_concern_dict["user"] = user
    new_concern = await Concern.objects.acreate(**new_concern_dict)
    # new_concern.refresh_from_db()
    return new_concern.model_dump()


@router.patch("/concern/{id}", name="Update existing concern")
async def update_existing_concern(
    id: Annotated[int, Path(description="Concern ID")],
    concern: UpdateConcern,
    user: Annotated[CustomUser, Depends(get_user)],
) -> ConcernDetails:
    """Update existing concern"""
    try:
        target_concern = await Concern.objects.aget(
            id=id,
            user=user,
            status__in=[
                Concern.ConcernStatus.OPEN.value,
                Concern.ConcernStatus.IN_PROGRESS.value,
            ],
        )
        target_concern.about = get_value(concern.about, target_concern.about)
        target_concern.details = get_value(
            concern.details, target_concern.details
        )
        await target_concern.asave()
        return target_concern.model_dump()
    except Concern.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Open or In-Progres concern with id {id} does not exist.",
        )


@router.get("/concern/{id}", name="Get concern details")
async def get_concern_details(
    id: Annotated[int, Path(description="Concern ID")],
    user: Annotated[CustomUser, Depends(get_user)],
) -> ConcernDetails:
    """Get particular concern details"""
    try:
        target_concern = await Concern.objects.aget(id=id, user=user)
        return target_concern.model_dump()
    except Concern.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Concern with id {id} does not exist.",
        )


@router.delete("/concern/{id}", name="Delete concern")
async def delete_concern_details(
    id: Annotated[int, Path(description="Concern ID")],
    user: Annotated[CustomUser, Depends(get_user)],
) -> ProcessFeedback:
    """Delete a particular concern"""
    try:
        target_concern = await Concern.objects.aget(id=id, user=user)
        await target_concern.adelete()
        return ProcessFeedback(detail="Concern deleted successfully.")
    except Concern.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Concern with id {id} does not exist.",
        )


@router.post("/feedback", name="New feedback")
async def add_new_feedback(
    user: Annotated[CustomUser, Depends(get_user)],
    feedback: NewUserFeedback,
) -> UserFeedbackDetails:
    try:
        new_feedback = await ServiceFeedback.objects.acreate(
            sender=user, message=feedback.message, rate=feedback.rate.value
        )
        return new_feedback.model_dump()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "You already have an existing feedback. Consider updating it "
                "instead."
            ),
        )


@router.patch("/feedback", name="Update feedback")
async def update_feedback(
    user: Annotated[CustomUser, Depends(get_user)],
    feedback: NewUserFeedback,
) -> UserFeedbackDetails:
    """Update user service-feedback"""
    try:
        target_feedback = await ServiceFeedback.objects.aget(sender=user)
        target_feedback.message = get_value(
            feedback.message, target_feedback.message
        )
        target_feedback.rate = get_value(
            feedback.rate.value, target_feedback.rate
        )
        await target_feedback.asave()
        return target_feedback.model_dump()
    except ServiceFeedback.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You have not send a feedback yet.",
        )


@router.get("/feedback", name="Get feedback details")
async def get_feedback_details(
    user: Annotated[CustomUser, Depends(get_user)],
) -> UserFeedbackDetails:
    """Get user service-feedback"""
    try:
        target_feedback = await ServiceFeedback.objects.aget(sender=user)
        return target_feedback.model_dump()
    except ServiceFeedback.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You have not send a feedback yet.",
        )


@router.delete("/feedback", name="Delete feedback")
async def delete_feedback(
    user: Annotated[CustomUser, Depends(get_user)],
) -> ProcessFeedback:
    """Delete user feedback"""
    try:
        target_feedback = await ServiceFeedback.objects.aget(sender=user)
        await target_feedback.adelete()
        return ProcessFeedback(detail="Feedback deleted successfully.")
    except ServiceFeedback.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You have not send a feedback yet.",
        )
