import hashlib

from archiverr.core.normalization import normalize_text



def build_canonical_id(track):
    payload = "|".join([
        normalize_text(track.artist),
        normalize_text(track.album or ""),
        normalize_text(track.title),
        str(track.duration_ms or ""),
    ])

    return hashlib.sha1(payload.encode()).hexdigest()
