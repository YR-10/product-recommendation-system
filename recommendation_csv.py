import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# 1. MEMBACA DATA PRODUK
# =========================

products = pd.read_csv("data/products.csv")

descriptions = products["deskripsi"]


# =========================
# 2. TF-IDF
# =========================

vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(descriptions)


# =========================
# 3. COSINE SIMILARITY
# =========================

similarity = cosine_similarity(tfidf_matrix)


# =========================
# 4. FUNGSI REKOMENDASI
# =========================

def recommend_products(product_name, top_n=3):

    # Cek apakah produk ada
    if product_name not in products["nama"].values:
        print("Produk tidak ditemukan.")
        return []

    # Cari index produk berdasarkan nama
    product_index = products.index[
        products["nama"] == product_name
    ][0]

    # Ambil similarity produk tersebut
    similarity_scores = list(
        enumerate(similarity[product_index])
    )

    # Urutkan dari similarity terbesar
    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Buang produk itu sendiri dan ambil Top-N
    recommendations = similarity_scores[1:top_n + 1]

    return recommendations


# =========================
# 5. INFORMASI DATA
# =========================

print("Ukuran matrix TF-IDF:")
print(tfidf_matrix.shape)

print("\nUkuran matrix similarity:")
print(similarity.shape)


# =========================
# 6. MENAMPILKAN REKOMENDASI
# =========================

product_name = "Laptop ASUS"

recommendations = recommend_products(product_name)

print("\nRekomendasi produk:", product_name)

for index, score in recommendations:
    print(
        products.iloc[index]["nama"],
        "->",
        round(score, 3)
    )