import pandas as pd


products = pd.read_csv("data/products_v2.csv")


def calculate_relevance(product_a, product_b):

    score = 0

    if product_a["jenis"] == product_b["jenis"]:
        score += 1

    if product_a["kategori"] == product_b["kategori"]:
        score += 1

    if product_a["ram_gb"] == product_b["ram_gb"]:
        score += 1

    if product_a["storage_gb"] == product_b["storage_gb"]:
        score += 1

    return score


def is_relevant(product_a, product_b):

    score = calculate_relevance(
        product_a,
        product_b
    )

    return score >= 2