import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# 1. MEMBACA DATA
# =========================

products = pd.read_csv("data/products.csv")


# =========================
# 2. MEMBUAT FITUR GABUNGAN
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
# 5. PRODUK YANG DICARI
# =========================

product_index = 0

query_product = products.iloc[product_index]["nama"]
query_category = products.iloc[product_index]["kategori"]


print("Produk yang dicari:", query_product)
print("Kategori produk:", query_category)


# =========================
# 6. FUNGSI REKOMENDASI
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
# 7. MEMBUAT REKOMENDASI
# =========================

recommendations = recommend_products(product_index)


print("\nRekomendasi:")

for index, score in recommendations:
    print(
        products.iloc[index]["nama"],
        "->",
        round(score, 3)
    )


# =========================
# 8. EVALUASI PRECISION@3
# =========================

relevant_count = 0

for index, score in recommendations:

    recommendation_category = products.iloc[index]["kategori"]

    print(
        "Cek:",
        products.iloc[index]["nama"],
        "| Kategori:",
        recommendation_category
    )

    if recommendation_category == query_category:
        relevant_count += 1


precision = relevant_count / len(recommendations)


# =========================
# 9. HASIL EVALUASI
# =========================

print("\nEvaluasi:")
print("Jumlah rekomendasi:", len(recommendations))
print("Jumlah produk relevan:", relevant_count)
print("Precision@3:", round(precision, 3))