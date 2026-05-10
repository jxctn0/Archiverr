def parse_playlist(path):
    tracks = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            print(line.strip())

    return tracks
