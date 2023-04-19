from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from model_maker.database.base import get_session
from model_maker.database.user import User

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> dict[str, int]:
    return {"item_id": item_id}


class CreateUserPayload(BaseModel):
    username: str
    email: str


class CreateUserResponse(BaseModel):
    id: str
    username: str
    email: str


@app.post("/users")
async def create_user(
    payload: CreateUserPayload, session: AsyncSession = Depends(get_session)
) -> CreateUserResponse:
    user = User(username=payload.username, email=payload.email)

    session.add(user)
    await session.flush()

    return CreateUserResponse(id=user.id, username=user.username, email=user.email)
