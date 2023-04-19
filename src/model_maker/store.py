import os
from pathlib import Path

import polars as pl

STORE_PATH = Path(os.getcwd()) / "tmp"


class Store:
    def store_file(self, file_id: str, df: pl.DataFrame) -> None:
        df.write_parquet(STORE_PATH / file_id)

    def get_file(self, file_id: str) -> pl.DataFrame:
        return pl.read_parquet(STORE_PATH / file_id)

    def list_files(self) -> list[str]:
        return [f.name for f in STORE_PATH.iterdir() if f.is_file()]

    def delete_file(self, file_id: str) -> None:
        (STORE_PATH / file_id).unlink()


file_store = Store()
