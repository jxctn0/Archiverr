from archiverr.database.db import Database


class BatchRepository:
    def __init__(self, db: Database):
        self.db = db

    def create_batch(self, batch_id: str, source_file: str):
        with self.db.session() as conn:
            conn.execute(
                """
                INSERT INTO ingest_batches (batch_id, source_file)
                VALUES (?, ?)
                """,
                (batch_id, source_file),
            )

    def update_count(self, batch_id: str, count: int):
        with self.db.session() as conn:
            conn.execute(
                """
                UPDATE ingest_batches
                SET total_tracks = ?
                WHERE batch_id = ?
                """,
                (count, batch_id),
            )

    def update_batch_metadata(self, batch_id: str, metadata: dict):
        fields = [f"{key} = ?" for key in metadata.keys()]
        params = list(metadata.values()) + [batch_id]

        with self.db.session() as conn:
            conn.execute(
                f"""
                UPDATE ingest_batches
                SET {', '.join(fields)}
                WHERE batch_id = ?
                """,
                params,
            )