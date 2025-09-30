import re
from datetime import datetime

from finance._enums import TransactionMeans, TransactionType
from pydantic import BaseModel, ConfigDict, field_validator
from users._enums import UserGender


class TokenAuth(BaseModel):
    access_token: str
    token_type: str | None = "bearer"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "pms_27b9d79erc245r44b9rba2crd2273b5cbb71",
                "token_type": "bearer",
            }
        }
    )


class ResetPassword(BaseModel):
    username: str
    new_password: str
    token: str

    @field_validator("new_password")
    def validate_new_password(new_password):
        if not re.match(
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&_-])[A-Za-z\d@$!%*?&_-]{8,}$",
            new_password,
        ):
            raise ValueError(
                "Password must be at least 8 characters long, include an "
                "uppercase letter, "
                "a lowercase letter, a number, and a special character."
            )
        return new_password

    @field_validator("token")
    def validate_token(token):
        if not re.match(r"[A-Z\d]{6,}", token):
            raise ValueError("Invalid token")
        return token

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "Smartwa",
                "new_password": "_Cljsuw376j$",
                "token": "0IJ4826L",
            }
        }
    )


class EditablePersonalData(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    address: str | None = None
    phone_number: str | None = None
    email: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "address": "Doctor",
                "phone_number": "+1234567890",
                "email": "john.doe@example.com",
            }
        }
    )


class UserProfile(EditablePersonalData):
    username: str
    gender: UserGender
    account_balance: float
    profile: str | None = None
    is_staff: bool
    date_joined: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "gender": "M",
                "address": "123 Meru-Maua Rd, Meru - Kenya",
                "phone_number": "+1234567890",
                "email": "john.doe@example.com",
                "username": "johndoe",
                "account_balance": 1244,
                "profile": "/media/custom_user/profile.jpg",
                "is_staff": False,
                "date_joined": "2023-01-01T00:00:00",
            }
        }
    )


class TransactionInfo(BaseModel):
    type: TransactionType
    amount: float
    means: TransactionMeans
    reference: str
    notes: str | None = None
    created_at: datetime


class PaymentAccountDetails(BaseModel):
    name: str
    paybill_number: str
    account_number: str
    details: str | None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "M-PESA",
                "paybill_number": "123456",
                "account_number": "78901234",
                "details": "Main business account",
            }
        }
    )


class SendMPESAPopupTo(BaseModel):
    phone_number: str
    amount: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"phone_number": "+1234567890", "amount": 100.0}
        }
    )
