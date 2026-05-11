import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Optional


class Database:
    def __init__(self, db_path: str = "test_archiverr.db"):
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
        self._initialized = False

    def connect(self) -> sqlite3.Connection:
        """
        Create (or reuse) a SQLite connection.
        Automatically initialises schema on first use.
        """

        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys = ON;")

            if not self._initialized:
                self._init_schema()
                self._initialized = True

        return self._conn

    def _init_schema(self):
        """
        Load schema.sql into database.
        """

        schema_path = Path(__file__).parent / "schema.sql"

        if not schema_path.exists():
            raise FileNotFoundError(
                f"Missing schema.sql at {schema_path}"
            )

        with open(schema_path, "r", encoding="utf-8") as f:
            self._conn.executescript(f.read())

    @contextmanager
    def session(self) -> Generator[sqlite3.Connection, None, None]:
        """
        Transaction-safe session wrapper.
        """

        conn = self.connect()

        try:
            yield conn
            conn.commit()

        except Exception:
            conn.rollback()
            raise

    def close(self):
        """
        Close database connection cleanly.
        """

        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def reset(self):
        """
        Destroy and recreate database file.
        Useful for testing/dev.
        """

        self.close()

        db_file = Path(self.db_path)

        if db_file.exists():
            db_file.unlink()

        self._initialized = False


# =========================================================
# MODULE-LEVEL SINGLETON
# =========================================================

_default_db = Database()


def connect() -> sqlite3.Connection:
    """
    Global DB connection accessor.
    """

    return _default_db.connect()


def session():
    """
    Global transactional session accessor.
    """

    return _default_db.session()


def reset_db():
    """
    Reset singleton database instance.
    """

    global _default_db

    _default_db.reset()
    _default_db = Database(_default_db.db_path)

    return _default_db
