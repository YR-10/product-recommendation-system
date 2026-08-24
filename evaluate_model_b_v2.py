import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from relevance import is_relevant


# =========================
# 1. BACA DATA
# =========================

products = pd.read_csv("data/products_v2.csv")


# =========================
# 2. MODEL B
# NAMA + DESKRIPSI + KATEGORI
# =========================

products["combined_features"] = (
    products["nama"] + " "
    + products["deskripsi"] + " "
    + products["kategori"]
)


# =========================
# 3. TF-IDF
# =========================

vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(
    products["combined_features"]
)


# =========================
# 4. COSINE SIMILARITY
# =========================

similarity = cosine_similarity(tfidf_matrix)


# =========================
# 5. FUNGSI REKOMENDASI
# =========================

def recommend_products(product_index, top_n=3):

    similarity_scores = list(
        enumerate(similarity[product_index])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = similarity_scores[
        1:top_n + 1
    ]

    return recommendations


# =========================
# 6. FUNGSI PRECISION@3
# =========================

def calculate_precision(product_index, top_n=3):

    recommendations = recommend_products(
        product_index,
        top_n
    )

    query_product = products.iloc[product_index]

    relevant_count = 0

    for index, score in recommendations:

        recommendation_product = products.iloc[index]

        if is_relevant(
            query_product,
            recommendation_product
        ):
            relevant_count += 1

    precision = (
        relevant_count
        / len(recommendations)
    )

    return precision


# =========================
# 7. EVALUASI SEMUA PRODUK
# =========================

precisions = []

print("Model B + Ground Truth V2")
print("\nPrecision@3 setiap produk:\n")

for product_index in range(len(products)):

    precision = calculate_precision(
        product_index
    )

    precisions.append(precision)

    print(
        products.iloc[product_index]["nama"],
        "->",
        round(precision, 3)
    )


# =========================
# 8. MEAN PRECISION@3
# =========================

mean_precision = (
    sum(precisions)
    / len(precisions)
)

print(
    "\nMean Precision@3 Model B V2:",
    round(mean_precision, 3)
)