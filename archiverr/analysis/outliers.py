def find_outliers(tracks):
    return [t for t in tracks if not t.year]
