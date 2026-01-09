from fastapi import APIRouter, HTTPException, status

from src.schemas.auth import LoginIn
from src.security import sign_jwt
from src.views.auth import LoginOut

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=LoginOut)
async def login(data: LoginIn):
    """Gera token JWT para autenticação (simulação simples por user_id)."""
    # Em produção, validar usuário/senha no banco
    if data.user_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID de usuário inválido")
    return sign_jwt(user_id=data.user_id)
