import matplotlib.pyplot as plt

models = [
    "Model A",
    "Model B"
]

precision = [
    0.800,
    0.867
]

recall = [
    0.425,
    0.515
]

x = range(len(models))

plt.bar(
    [i - 0.2 for i in x],
    precision,
    width=0.4,
    label="Proecision@3"
)

plt.bar(
    [i + 0.2 for i in x],
    recall,
    width=0.4,
    label="recall@3"
)

plt.xticks(
    list(x),
    models
)

plt.ylabel("Score")

plt.xlabel("Model")

plt.title("Perbandingan Model A dan Model B")

plt.ylim(0.1)

plt.legend()

plt.show()

