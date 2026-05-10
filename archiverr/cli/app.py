#================== archiverr/cli/app.py ==================
# This is the main entry point for the CLI application. It defines the commands and their associated functions.
#
# Usage:
#  archiverr import <path_to_library> - Imports the Apple Music library from the specified path.
#  archiverr analyze <path_to_library> - Analyzes the imported library and provides insights such as the distribution of tracks by year.
#  archiverr --help/-h - Displays the help message with available commands and their descriptions.
#  archiverr download - Downloads the music files based on the imported library (to be implemented).
#
# The CLI is built using the Typer library, which provides a simple and intuitive way to create command line interfaces in Python. Each command is decorated with @app.command() to register it with the Typer application. The functions associated with each command handle the logic for importing and analyzing the music library.


import typer

app = typer.Typer()


@app.command()
def ingest(
    path: str,
    verbose: bool = typer.Option(False, "--verbose", "-v")
):
    from archiverr.core.logging import setup_logging, log_event, Stage
    from archiverr.parser.apple_music import parse_library
    from archiverr.database.db import Database
    from archiverr.database.repositories import RawTrackRepository, BatchRepository

    logger = setup_logging(verbose)

    log_event(logger, Stage.INGEST, f"Loading {path}")

    library = parse_library(path)

    log_event(logger, Stage.PARSE, f"{len(library.tracks)} tracks found")

    db = Database()
    raw_repo = RawTrackRepository(db)
    batch_repo = BatchRepository(db)

    batch_id = "batch_" + path.split("/")[-1]

    log_event(logger, Stage.DB, f"Creating batch {batch_id}")
    batch_repo.create_batch(batch_id, path)

    for track in library.tracks.values():
        log_event(logger, Stage.RAW, f"{track.artist} - {track.title}")
        raw_repo.insert(track, batch_id)

    log_event(logger, Stage.DB, f"Batch complete ({len(library.tracks)})")