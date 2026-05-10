import matplotlib.pyplot as plt



def generate_year_heatmap(counter):
    years = sorted(counter.keys())
    counts = [counter[y] for y in years]

    plt.figure(figsize=(14, 5))
    plt.bar(years, counts)
    plt.xlabel("Year")
    plt.ylabel("Tracks")
    plt.title("Library Distribution")
    plt.show()
