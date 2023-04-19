from typing import Annotated

from fastapi import Header


async def extract_user_id(
    user_id: Annotated[str, Header] = Header(default="mauro")
) -> str:
    return user_id
