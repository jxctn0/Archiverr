import argparse

from archiverr.parser.apple_music import parse_library
from archiverr.database.db import Database
from archiverr.database.repositories import RawTrackRepository, BatchRepository
from archiverr.core.logging import setup_logging, log_event, Stage
import uuid

from archiverr.core.hashing import hash_file


def ingest(path: str, verbose: bool):
    # Setup logging
    logger = setup_logging(verbose)

    # Create fresh database instance to avoid cached connections
    db_instance = Database()
    conn = db_instance.connect()

    # Calculate file hash to check for duplicates
    file_hash = hash_file(path)
    if verbose:
        log_event(logger, Stage.INGEST, f"Computed file hash: {file_hash}")

    # Check if this file has already been ingested

    existing = conn.execute(
        "SELECT batch_id FROM ingest_batches WHERE file_hash = ?",
        (file_hash,)
    ).fetchone()

    if existing:
        log_event(logger, Stage.INGEST, f"[SKIP] Library already imported (batch {existing['batch_id']})")
        return

    # Create new ingest batch
    batch_id = str(uuid.uuid4())

    if verbose:
        log_event(logger, Stage.INGEST, f"Starting new ingest batch {batch_id} for file {path}")

    # Insert batch record
    conn.execute(
        """
        INSERT INTO ingest_batches (batch_id, source_file, file_hash)
        VALUES (?, ?, ?)
        """,
        (batch_id, path, file_hash)
    )

    # Parse the library file
    library = parse_library(path) # returns Library Dataclass
    if verbose:
        log_event(logger, Stage.INGEST, f"Parsed library file with {len(library.tracks)} tracks, {len(library.playlists)} playlists")
    
    # Insert raw track data
    raw_repo = RawTrackRepository(db_instance)
    for track in library.tracks.values():
        raw_repo.insert(track, batch_id)
        if verbose:
            log_event(logger, Stage.INGEST, f"Inserted raw track: {track.title} by {track.artist}")

    # Insert batch metadata
    batch_repo = BatchRepository(db_instance)
    batch_repo.update_batch_metadata(batch_id, {
        "num_tracks": len(library.tracks),
        "num_playlists": len(library.playlists)
    })

    # Finalize batch
    conn.execute(
        """
        UPDATE ingest_batches
        SET status = 'completed'
        WHERE batch_id = ?
        """,
        (batch_id,)
    )

    if verbose:
        log_event(logger, Stage.INGEST, f"Completed ingest batch {batch_id}")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="archiverr",
        description="Music library ingestion + metadata resolution system"
    )

    parser.add_argument(
        "command",
        choices=["ingest"],
        help="Command to run"
    )

    parser.add_argument(
        "path",
        nargs="?",
        help="Path to Apple Music Library.xml"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    main_logger = setup_logging(args.verbose, not args.no_color)

    if args.verbose:
        log_event(main_logger, Stage.INIT, f"Starting Archiverr with command: {args.command}, path: {args.path}")
        

    if args.command == "ingest":
        if not args.path:
            parser.error("ingest requires a path to Library.xml")
        ingest(args.path, args.verbose)


if __name__ == "__main__":
    main()