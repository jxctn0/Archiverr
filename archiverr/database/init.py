from pathlib import Path
from archiverr.database.db import Database


def init_db(db: Database, schema_path: str = None):
    if schema_path is None:
        schema_path = Path(__file__).parent / "schema.sql"

    schema_sql = Path(schema_path).read_text()

    with db.session() as conn:
        conn.executescript(schema_sql)