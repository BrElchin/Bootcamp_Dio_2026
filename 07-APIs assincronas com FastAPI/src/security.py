import time
from datetime import datetime, timedelta
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from src.config import settings


class AccessToken(BaseModel):
    iss: str
    sub: int
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str


class JWTToken(BaseModel):
    access_token: str


def sign_jwt(user_id: int) -> JWTToken:
    """Gera um token JWT com expiração configurável."""
    now = datetime.utcnow()
    payload = {
        "iss": "desafio-bank.com.br",
        "sub": user_id,
        "aud": "desafio-bank",
        "exp": now + timedelta(minutes=settings.jwt_expiration_minutes),
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return JWTToken(access_token=token)


async def decode_jwt(token: str) -> AccessToken | None:
    """Decodifica e valida o token JWT."""
    try:
        decoded = jwt.decode(
            token,
            settings.jwt_secret,
            audience="desafio-bank",
            algorithms=[settings.jwt_algorithm]
        )
        token_data = AccessToken(**decoded)
        if token_data.exp < time.time():
            return None
        return token_data
    except jwt.PyJWTError:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> AccessToken:
        credentials = await super().__call__(request)
        if not credentials or not credentials.credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autorização ausente ou inválido."
            )

        if credentials.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Esquema de autenticação inválido. Use 'Bearer'."
            )

        token_data = await decode_jwt(credentials.credentials)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado."
            )

        return token_data


async def get_current_user(token: Annotated[AccessToken, Depends(JWTBearer())]) -> dict[str, int]:
    """Dependency para obter o usuário autenticado."""
    return {"user_id": token.sub}


def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    """Dependency para rotas que exigem autenticação."""
    return current_user
