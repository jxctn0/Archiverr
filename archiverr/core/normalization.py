# This module contains functions for generating canonical identifiers for tracks based on their metadata.
# The canonical ID is a unique identifier that can be used to track the same track across different

import re

def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r"\(.*?\)", "", text)   # remove brackets
    text = re.sub(r"[^a-z0-9 ]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()