"""Utility functions for user fastapi-app"""

import random
import uuid
from string import ascii_lowercase
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from project.utils import generate_random_token
from users.models import CustomUser

token_id = "lms_"
"""First characters of every user auth-token"""

v1_auth_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/account/token",
    description="Generated API authentication token",
)


async def get_user(
    token: Annotated[str, Depends(v1_auth_scheme)],
) -> CustomUser:
    """Ensures token passed match the one set"""
    if token:
        try:
            if token.startswith(token_id):
                user = await CustomUser.objects.select_related("account").aget(
                    token=token
                )
                return user

        except CustomUser.DoesNotExist:
            pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing token",
        headers={"WWW-Authenticate": "Bearer"},
    )


def generate_token() -> str:
    """Generates api token"""
    return token_id + str(uuid.uuid4()).replace(
        "-", random.choice(ascii_lowercase)
    )


def generate_password_reset_token(length: int = 8) -> str:
    return generate_random_token(length)
