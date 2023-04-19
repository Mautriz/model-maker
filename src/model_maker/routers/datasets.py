from http import HTTPStatus
from io import BytesIO

import polars as pl
from fastapi import APIRouter, File, HTTPException, Response, UploadFile
from polars.exceptions import ComputeError
from pydantic import BaseModel

from model_maker.store import file_store

router = APIRouter()


class DatasetsSqlPayload(BaseModel):
    sql: str
    connector_id: str


class ListDatasetsResponse(BaseModel):
    datasets: list[str]


@router.post("/datasets")
async def create_upload_file(file: UploadFile = File(...)) -> Response:
    # check file extension
    if not file.filename:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "No filename provided")

    extension = _get_extension(file.filename)

    try:
        if extension == "csv":
            df = pl.read_csv(file.file)
        elif extension == "parquet":
            df = pl.read_parquet(file.file)
        elif extension == "avro":
            df = pl.read_avro(file.file)
        elif extension == "xlsx":
            bytesio = BytesIO(file.file.read())
            df = pl.read_excel(
                source=bytesio,
                sheet_id=1,
                sheet_name=None,
                read_csv_options=None,
                xlsx2csv_options=None,
            )
        else:
            raise HTTPException(HTTPStatus.BAD_REQUEST, "File extension not supported")
    except ComputeError as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, str(e))

    file_store.store_file(_replace_extension(file.filename), df)

    return Response(status_code=200)


@router.delete("/datasets/{dataset_id}")
def delete_dataset(dataset_id: str):
    file_store.delete_file(dataset_id)


@router.get("/datasets")
def list_datasets() -> ListDatasetsResponse:
    return ListDatasetsResponse(datasets=file_store.list_files())


@router.post("/datasets/sql")
def create_dataset_sql(payload: DatasetsSqlPayload):
    pass


@router.post("/datasets/fs")
def create_dataset_fs():
    pass


def _replace_extension(filename: str, new_extension=".parquet") -> str:
    return ".".join(filename.split(".")[:-1]) + new_extension


def _get_extension(filename: str) -> str:
    split_file = filename.split(".")

    # Handles the case where the file has no extension
    if len(split_file) == 1:
        return ""

    return split_file[-1]
