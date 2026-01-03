from uuid import uuid4
from typing import List

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError

from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select


router = APIRouter()


@router.post(
    '/',
    summary='Criar um novo Centro de Treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(db_session: DatabaseDependency, centro_in: CentroTreinamentoIn = Body(...)) -> CentroTreinamentoOut:
    try:
        centro_model = CentroTreinamentoModel(**centro_in.model_dump())
        db_session.add(centro_model)
        await db_session.commit()
        await db_session.refresh(centro_model)
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um centro de treinamento cadastrado com o nome: {centro_in.nome}"
        )
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir os dados no banco'
        )

    return CentroTreinamentoOut.model_validate(centro_model)


@router.get(
    '/',
    summary='Consultar todos os Centros de Treinamento',
    status_code=status.HTTP_200_OK,
    response_model=List[CentroTreinamentoOut],
)
async def query(db_session: DatabaseDependency) -> List[CentroTreinamentoOut]:
    centros: List[CentroTreinamentoModel] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return [CentroTreinamentoOut.model_validate(centro) for centro in centros]


@router.get(
    '/{id}',
    summary='Consultar um Centro de Treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro: CentroTreinamentoModel = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()

    if not centro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Centro de treinamento não encontrado no id: {id}')

    return CentroTreinamentoOut.model_validate(centro)