from typing import Annotated
from pydantic import Field, UUID4

from workout_api.contrib.schemas import BaseSchema, OutMixin


class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=50)]


class CategoriaOut(CategoriaIn, OutMixin):
    pass