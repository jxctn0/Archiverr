import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Optional


class Database:
    def __init__(self, db_path: str = "archiverr.db"):
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self._initialized = False

    def connect(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys = ON;")

            if not self._initialized:
                self._init_schema()
                self._initialized = True

        return self._conn

    def _init_schema(self):
        schema_path = Path(__file__).parent / "schema.sql"

        if not schema_path.exists():
            raise FileNotFoundError(f"Missing schema.sql at {schema_path}")

        with open(schema_path, "r") as f:
            self._conn.executescript(f.read())

    @contextmanager
    def session(self) -> Generator[sqlite3.Connection, None, None]:
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise