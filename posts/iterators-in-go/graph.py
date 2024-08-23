import matplotlib.pyplot as plt

names = ["channel", "enclosure function", "structure", "native go 1.23"]
usage_time = [614234, 82593, 72821, 10622]
usage_memory = [161, 8, 32, 0]
colors = ["#F77373", "#66B2FF", "#99FF99", "#FFCC99"]

plt.figure(figsize=(12, 10))

plt.subplot(2, 1, 1)
bars = plt.bar(names, usage_time, color=colors)
plt.title("Time usage")
plt.ylabel("ns/op")
# plt.yscale('log')  # for large values

for i, v in enumerate(usage_time):
    plt.text(i, v, str(v), ha="center", va="bottom")

plt.subplot(2, 1, 2)
bars = plt.bar(names, usage_memory, color=colors)
plt.title("Memory usage")
plt.ylabel("B/op")

# Добавляем значения над столбцами
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2.0,
        height,
        f"{height}",
        ha="center",
        va="bottom",
    )

# sub-graphs placement
plt.tight_layout()

# common legend
# plt.figlegend(bars, names, loc='lower center', ncol=4, bbox_to_anchor=(0.5, 0))

# indenting the graph from the bottom
plt.subplots_adjust(bottom=0.15)

# graph file name
plt.savefig("colored_algorithm_comparison.png")
plt.show()
