from uuid import uuid4
from typing import List

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError

from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.categorias.models import CategoriaModel
from workout_api.contrib.dependencies import DatabaseDependency
from sqlalchemy.future import select


router = APIRouter()


@router.post(
    '/',
    summary='Criar uma nova Categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)) -> CategoriaOut:
    try:
        categoria_model = CategoriaModel(**categoria_in.model_dump())
        db_session.add(categoria_model)
        await db_session.commit()
        await db_session.refresh(categoria_model)
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe uma categoria cadastrada com o nome: {categoria_in.nome}"
        )
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir os dados no banco'
        )

    return CategoriaOut.model_validate(categoria_model)


@router.get(
    '/',
    summary='Consultar todas as Categorias',
    status_code=status.HTTP_200_OK,
    response_model=List[CategoriaOut],
)
async def query(db_session: DatabaseDependency) -> List[CategoriaOut]:
    categorias: List[CategoriaModel] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return [CategoriaOut.model_validate(categoria) for categoria in categorias]


@router.get(
    '/{id}',
    summary='Consultar uma Categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaModel = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()

    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Categoria não encontrada no id: {id}')

    return CategoriaOut.model_validate(categoria)