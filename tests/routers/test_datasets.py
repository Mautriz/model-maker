import pytest
from fastapi.testclient import TestClient

from model_maker.routers.datasets import _get_extension, _replace_extension
from model_maker.store import file_store
from tests.utils import TEST_PATH


@pytest.fixture(autouse=True)
def clear_files():
    yield
    for file_id in file_store.list_files():
        file_store.delete_file(file_id)


def test_create_from_parquet(client: TestClient) -> None:
    file_path = TEST_PATH / "routers" / "test.parquet"

    with file_path.open("rb") as file:
        response = client.post("/datasets", files={"file": file})
        assert response.status_code == 200


def test_create_from_xlxs(client: TestClient) -> None:
    file_path = TEST_PATH / "routers" / "test.xlsx"

    with file_path.open("rb") as file:
        response = client.post("/datasets", files={"file": file})
        assert response.status_code == 200


def test_create_from_avro(client: TestClient) -> None:
    file_path = TEST_PATH / "routers" / "test.avro"

    with file_path.open("rb") as file:
        response = client.post("/datasets", files={"file": file})
        assert response.status_code == 200


def test_create_from_csv(client: TestClient) -> None:
    file_path = TEST_PATH / "routers" / "test.csv"

    with file_path.open("rb") as file:
        response = client.post("/datasets", files={"file": file})
        assert response.status_code == 200


def test_broken_csv(client: TestClient) -> None:
    broken_csv_path = TEST_PATH / "routers" / "broken.csv"

    with broken_csv_path.open("rb") as file:
        response = client.post("/datasets", files={"file": file})
        assert response.json() == {"detail": "invalid utf-8 sequence in csv"}
        assert response.status_code == 400


def test_get_files(client: TestClient) -> None:
    response = client.get("/datasets")
    assert response.status_code == 200
    assert response.json()["datasets"] == []

    # upload file
    file_path = TEST_PATH / "routers" / "test.csv"

    with file_path.open("rb") as file:
        response = client.post("/datasets", files={"file": file})
        assert response.status_code == 200

    response = client.get("/datasets")
    assert response.status_code == 200
    assert response.json()["datasets"] == ["test.parquet"]


def test_delete_file(client: TestClient) -> None:
    # upload file
    file_path = TEST_PATH / "routers" / "test.csv"

    with file_path.open("rb") as file:
        response = client.post("/datasets", files={"file": file})
        assert response.status_code == 200

    response = client.get("/datasets")
    assert response.status_code == 200
    assert response.json()["datasets"] == ["test.parquet"]

    response = client.delete("/datasets/test.parquet")
    assert response.status_code == 200

    response = client.get("/datasets")
    assert response.status_code == 200
    assert response.json()["datasets"] == []


def test_replace_extension() -> None:
    assert _replace_extension("test.csv") == "test.parquet"
    assert _replace_extension("test.csv", ".csv") == "test.csv"
    assert _replace_extension("dacacac.scaccomatto", ".parquet") == "dacacac.parquet"


def test_get_extension() -> None:
    assert _get_extension("test.csv") == "csv"
    assert _get_extension("test.parquet") == "parquet"
    assert _get_extension("test.avro") == "avro"
    assert _get_extension("test.xlsx") == "xlsx"
    assert _get_extension("test") == ""
    assert _get_extension("test.") == ""
    assert _get_extension("test.csv.csv") == "csv"
    assert _get_extension("test.csv.parquet") == "parquet"
    assert _get_extension("test.csv.avro") == "avro"
    assert _get_extension("test.csv.xlsx") == "xlsx"
