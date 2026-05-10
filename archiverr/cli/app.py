import typer

from archiverr.parser.apple_music import parse_library
from archiverr.analysis.year_analysis import analyze_years


app = typer.Typer()


@app.command()
def ingest(path: str):
    tracks = parse_library(path)

    print(f"Loaded {len(tracks)} tracks")


@app.command()
def analyze(path: str):
    tracks = parse_library(path)

    years = analyze_years(tracks)

    print(years)


if __name__ == "__main__":
    app()
