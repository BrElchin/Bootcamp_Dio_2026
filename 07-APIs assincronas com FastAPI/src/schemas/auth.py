from pydantic import BaseModel, PositiveInt


class LoginIn(BaseModel):
    user_id: PositiveInt
