"""Routes for account `/account`"""

from fastapi import (
    APIRouter,
    status,
    HTTPException,
    Depends,
    Query,
)
from fastapi.encoders import jsonable_encoder
from fastapi.security.oauth2 import OAuth2PasswordRequestFormStrict
from typing import Annotated

from users.models import CustomUser, AuthToken
from finance.models import Account, Transaction
from project.utils import get_expiry_datetime

from api.v1.utils import send_email, get_value
from api.v1.account.utils import get_user, generate_token, generate_password_reset_token

from api.v1.account.models import (
    TokenAuth,
    ResetPassword,
    UserProfile,
    EditablePersonalData,
    TransactionInfo,
    PaymentAccountDetails,
    SendMPESAPopupTo,
)
from api.v1.models import ProcessFeedback
from django.db.models import Q
import asyncio

router = APIRouter(
    prefix="/account",
    tags=["Account"],
)


@router.post("/token", name="User auth token")
async def fetch_token(
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()]
) -> TokenAuth:
    """
    Get user account token
    """
    try:
        user = await CustomUser.objects.aget(username=form_data.username)
        if await user.acheck_password(form_data.password):
            if user.token is None:
                user.token = generate_token()
                await user.asave()
            return TokenAuth(
                access_token=user.token,
                token_type="bearer",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
            )
    except CustomUser.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist.",
        )


@router.patch("/token", name="Generate new user token")
async def generate_new_token(
    user: Annotated[CustomUser, Depends(get_user)]
) -> TokenAuth:
    """Generate new token"""
    user.token = generate_token()
    await user.asave()
    return TokenAuth(access_token=user.token)


@router.get("/profile", name="Get user profile")
async def profile_information(
    user: Annotated[CustomUser, Depends(get_user)]
) -> UserProfile:
    return user.model_dump()


@router.patch("/profile", name="Update user profile")
async def update_personal_info(
    user: Annotated[CustomUser, Depends(get_user)],
    updated_personal_data: EditablePersonalData,
) -> EditablePersonalData:
    user.first_name = get_value(updated_personal_data.first_name, user.first_name)
    user.last_name = get_value(updated_personal_data.last_name, user.last_name)
    user.phone_number = get_value(updated_personal_data.phone_number, user.phone_number)
    user.email = get_value(updated_personal_data.email, user.email)
    user.address = get_value(updated_personal_data.address, user.address)
    await user.asave()
    return user.model_dump()


@router.get("/exists", name="Check if username exists")
async def check_if_username_exists(
    username: Annotated[str, Query(description="Username to check against")]
) -> ProcessFeedback:
    """Checks if account with a particular username exists
    - Useful when setting username at account creation
    """
    existance_status = (
        await CustomUser.objects.filter(username=username).afirst() is not None
    )
    return ProcessFeedback(detail=existance_status)


@router.get("/transactions", name="Financial transactions")
async def get_financial_transactions(
    user: Annotated[CustomUser, Depends(get_user)],
    means: Annotated[
        Transaction.TransactionMeans, Query(description="Transaction means")
    ] = None,
    type: Annotated[
        Transaction.TransactionType, Query(description="Transaction type")
    ] = None,
) -> list[TransactionInfo]:
    """Get complete financial transactions"""
    search_filter = dict(user=user)
    if means is not None:
        search_filter["means"] = means.value
    if type is not None:
        search_filter["type"] = type.value
    return [
        jsonable_encoder(transaction)
        async for transaction in Transaction.objects.filter(**search_filter)
        .order_by("-created_at")
        .all()[:15]
    ]


@router.get("/mpesa-payment-account-details", name="M-Pesa payment account details")
async def get_mpesa_payment_account_details(
    user: Annotated[CustomUser, Depends(get_user)]
) -> PaymentAccountDetails:
    """Get mpesa payment account details specifically for current user"""
    try:
        account = await Account.objects.filter(
            Q(name__icontains="m-pesa") | Q(name__icontains="mpesa")
        ).alast()
        return PaymentAccountDetails(
            name=account.name,
            paybill_number=account.paybill_number,
            account_number=account.account_number
            % dict(
                id=user.id,
                username=user.username,
                phone_number=user.phone_number,
                email=user.email,
            ),
            details=account.details,
        )
    except Account.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="M-PESA Payment account details is currently not available.",
        )


@router.get("/other-payment-account-details", name="Other payment account details")
async def get_payment_account_details(
    user: Annotated[CustomUser, Depends(get_user)]
) -> list[PaymentAccountDetails]:
    """Get other payment account details such as bank etc."""
    return [
        PaymentAccountDetails(
            name=account.name,
            paybill_number=account.paybill_number,
            account_number=account.account_number
            % dict(
                id=user.id,
                username=user.username,
                phone_number=user.phone_number,
                email=user.email,
            ),
            details=account.details,
        )
        async for account in Account.objects.filter(is_active=True)
        .exclude(Q(name__icontains="m-pesa") | Q(name__icontains="mpesa"))
        .all()
    ]


@router.post("/send-mpesa-payment-popup", name="Send mpesa payment popup")
async def send_mpesa_popup_to(
    user: Annotated[CustomUser, Depends(get_user)], popup_to: SendMPESAPopupTo
) -> ProcessFeedback:
    """Send mpesa payment pop-up to user"""

    async def send_popup(phone_number, amount):
        """TODO: Request payment using Daraja API"""
        mpesa_details = await Account.objects.filter(name__icontains="m-pesa").alast()
        assert mpesa_details is not None, "M-PESA account details not found"
        account_number = mpesa_details.account_number % dict(
            id=user.id,
            username=user.username,
            phone_number=user.phone_number,
            email=user.email,
        )
        # TODO: Add routers for handling mpesa callbacks
        """
        send_payment_push(
            phone_number=phone_number,
            amount=amount,
            account_reference=account_number,
        )
        """
        # Push send successfully let's SIMULATE account debitting
        # user.account.save()
        new_transaction = await Transaction.objects.acreate(
            user=user,
            type=Transaction.TransactionType.DEPOSIT.value,
            amount=amount,
            means=Transaction.TransactionMeans.MPESA.value,
        )
        await new_transaction.asave()

    await send_popup(popup_to.phone_number, popup_to.amount)
    return ProcessFeedback(detail="M-pesa popup sent successfully.")


@router.get("/password/send-password-reset-token", name="Send password reset token")
async def reset_password(
    identity: Annotated[str, Query(description="Username or email address")]
) -> ProcessFeedback:
    """Emails password reset token to user"""
    try:
        target_user = await CustomUser.objects.filter(
            Q(username=identity) | Q(email=identity)
        ).aget()
        auth_token = await AuthToken.objects.filter(user=target_user).afirst()
        if auth_token is not None:
            auth_token.token = generate_password_reset_token()
            auth_token.expiry_datetime = get_expiry_datetime()
        else:
            auth_token = await AuthToken.objects.acreate(
                user=target_user,
                token=generate_password_reset_token(),
            )
        await auth_token.asave()
        await asyncio.to_thread(
            send_email,
            **dict(
                subject="Password Reset Token",
                recipient=auth_token.user.email,
                template_name="email/password_reset_token",
                context=dict(auth_token=auth_token),
            )
        )

    except CustomUser.DoesNotExist:
        # Let's not diclose about this for security reasons
        pass
    finally:
        return ProcessFeedback(
            detail=(
                "If an account with the provided identity exists, "
                "a password reset token has been sent to the associated email address."
            )
        )


@router.post("/password/reset", name="Set new account password")
async def reset_password(info: ResetPassword) -> ProcessFeedback:
    """Resets user account password"""
    try:
        auth_token = await AuthToken.objects.select_related("user").aget(
            token=info.token
        )
        if auth_token.is_expired():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token has expired.",
            )
        user = auth_token.user
        if user.username == info.username:
            user.set_password(info.new_password)
            user.token = generate_token()
            await user.asave()
            await auth_token.adelete()
            return ProcessFeedback(detail="Password reset successfully.")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username"
            )

    except AuthToken.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token.",
        )
