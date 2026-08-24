import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# 1. BACA DATA
# =========================

products = pd.read_csv("data/products.csv")


# =========================
# 2. COMBINED FEATURES
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

    recommendations = similarity_scores[1:top_n + 1]

    return recommendations


# =========================
# 6. FUNGSI PRECISION
# =========================

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


# =========================
# 7. EVALUASI SEMUA PRODUK
# =========================

precisions = []

for product_index in range(len(products)):

    precision = calculate_precision(
        product_index
    )

    precisions.append(precision)


# =========================
# 8. TAMPILKAN HASIL
# =========================

print("Jumlah produk yang dievaluasi:", len(products))

print("\nPrecision setiap produk:")

for index, precision in enumerate(precisions):

    print(
        products.iloc[index]["nama"],
        "->",
        round(precision, 3)
    )


# =========================
# 9. MEAN PRECISION@3
# =========================

mean_precision = sum(precisions) / len(precisions)

print(
    "\nMean Precision@3:",
    round(mean_precision, 3)
)