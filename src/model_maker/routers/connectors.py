from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class CreateConnectorPayload(BaseModel):
    name: str
    type: str
    host: str
    port: int
    username: str
    password: str
    database: str


@router.post("/connectors")
def create_connector(payload: CreateConnectorPayload):
    pass


@router.delete("/connectors/{connector_id}")
def delete_connector(connector_id: int):
    pass


@router.get("/connectors")
def list_connectors():
    pass
