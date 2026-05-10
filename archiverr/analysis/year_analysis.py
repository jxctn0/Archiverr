from collections import Counter



def analyze_years(tracks):
    years = [t.year for t in tracks if t.year]
    return Counter(years)
