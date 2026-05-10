import logging
import sys
from typing import Optional


# =========================
# ANSI STYLING (kept, cleaned)
# =========================

FORMATTING = {
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "END": "\033[0m",
}

COLORS = {
    "LIGHT": {
        "BLACK": "\033[90m",
        "RED": "\033[91m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "BLUE": "\033[94m",
        "MAGENTA": "\033[95m",
        "CYAN": "\033[96m",
        "WHITE": "\033[97m",
    },
    "DARK": {
        "BLACK": "\033[30m",
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "YELLOW": "\033[33m",
        "BLUE": "\033[34m",
        "MAGENTA": "\033[35m",
        "CYAN": "\033[36m",
        "WHITE": "\033[37m",
    },
    "BACKGROUND": {
        "BLACK": "\033[40m",
        "RED": "\033[41m",
        "GREEN": "\033[42m",
        "YELLOW": "\033[43m",
        "BLUE": "\033[44m",
        "MAGENTA": "\033[45m",
        "CYAN": "\033[46m",
        "WHITE": "\033[47m",
    },
}


# =========================
# COLOR HELPERS (optional UI)
# =========================

def color_text(text: str, color: Optional[str]):
    if color is None:
        return text

    color = str(color).upper()

    if color in COLORS["LIGHT"]:
        return f"{COLORS['LIGHT'][color]}{text}{FORMATTING['END']}"

    try:
        code = int(color)
        if 0 <= code <= 255:
            return f"\033[38;5;{code}m{text}{FORMATTING['END']}"
    except ValueError:
        pass

    return text


def format_text(text: str, *formats):
    seq = "".join([FORMATTING.get(f.upper(), "") for f in formats])
    return f"{seq}{text}{FORMATTING['END']}"


# =========================
# LOGGING CORE
# =========================

LOGGER_NAME = "archiverr"


def setup_logger(verbose: bool = False) -> logging.Logger:
    """
    Central logging setup.

    verbose=True → DEBUG
    verbose=False → INFO
    """

    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    return logging.getLogger(LOGGER_NAME)


# =========================
# PIPELINE LOGGING (MAIN API)
# =========================

def log_event(logger: logging.Logger, stage: str, message: str):
    """
    Main structured logging format:

    [STAGE] message
    """
    logger.info(f"[{stage}] {message}")


def log_debug_event(logger: logging.Logger, stage: str, message: str):
    """
    Debug-level structured logs (only shown in -v mode)
    """
    logger.debug(f"[{stage}] {message}")


def log_track(logger: logging.Logger, stage: str, track, extra: str = ""):
    """
    Specialized helper for music pipeline logging.
    """
    msg = f"{track.artist} - {track.title}"
    if extra:
        msg += f" | {extra}"

    logger.info(f"[{stage}] {msg}")


def log_error(logger: logging.Logger, stage: str, message: str):
    logger.error(f"[{stage}] {message}")


# =========================
# PIPELINE STAGE CONSTANTS
# =========================

class Stage:
    INGEST = "INGEST"
    PARSE = "PARSE"
    DB = "DB"
    RAW = "RAW"
    CANONICAL = "CANONICAL"
    SPOTIFY = "SPOTIFY"
    MUSICBRAINZ = "MUSICBRAINZ"
    YOUTUBE = "YOUTUBE"
    DOWNLOAD = "DOWNLOAD"