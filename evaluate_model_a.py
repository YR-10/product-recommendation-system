import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


products = pd.read_csv("data/products.csv")

text_data = products["deskripsi"]


vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(
    text_data
)


similarity = cosine_similarity(tfidf_matrix)


def recommend_products(product_index, top_n=3):

    similarity_scores = list(
        enumerate(similarity[product_index])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = similarity_scores[1:top_n + 1]

    return recommendations


def calculate_precision(product_index, top_n=3):

    recommendations = recommend_products(
        product_index,
        top_n
    )

    query_category = products.iloc[
        product_index
    ]["kategori"]

    relevant_count = 0

    for index, score in recommendations:

        recommendation_category = products.iloc[
            index
        ]["kategori"]

        if recommendation_category == query_category:
            relevant_count += 1

    precision = relevant_count / len(recommendations)

    return precision


precisions = []

for product_index in range(len(products)):

    precision = calculate_precision(
        product_index
    )

    precisions.append(precision)


print("Model A: Deskripsi saja")

print(
    "Jumlah produk yang dievaluasi:",
    len(products)
)

print("\nPrecision setiap produk:")

for index, precision in enumerate(precisions):

    print(
        products.iloc[index]["nama"],
        "->",
        round(precision, 3)
    )


mean_precision = sum(precisions) / len(precisions)

print(
    "\nMean Precision@3 Model A:",
    round(mean_precision, 3)
)