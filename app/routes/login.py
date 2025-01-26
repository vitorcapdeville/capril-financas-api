from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.core import security
from app.core.config import settings
from app.dependencies import CurrentUser, SessionDep
from app.models import Token, UserPublic

router = APIRouter(tags=["login"])


@router.post("/login/access-token", operation_id="login")
def login_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.authenticate(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos.")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo.")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(access_token=security.create_access_token(user.id, expires_delta=access_token_expires))


@router.post("/login/test-token", operation_id="get_current_user")
def test_token(current_user: CurrentUser) -> UserPublic:
    """
    Test access token
    """
    return current_user
