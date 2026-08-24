from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# 1. DATA PRODUK
# =========================

products = [
    "Laptop ASUS Intel i5 RAM 16GB SSD 512GB",
    "Laptop Lenovo Intel i5 RAM 16GB SSD 512GB",
    "Laptop Acer Ryzen 5 RAM 8GB SSD 512GB",
    "iPhone smartphone RAM 8GB 256GB",
    "Headset gaming wireless bluetooth"
]


# =========================
# 2. TF-IDF
# =========================

vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(products)

print("Daftar kata:")
print(vectorizer.get_feature_names_out())

print("\nMatriks TF-IDF:")
print(tfidf_matrix.toarray())


# =========================
# 3. COSINE SIMILARITY
# =========================

similarity = cosine_similarity(tfidf_matrix)

print("\nCosine Similarity:")
print(similarity)


# =========================
# 4. FUNGSI REKOMENDASI
# =========================

def recommend_products(product_name, top_n=3):

    if product_name not in products:
        print("Produk tidak ditemukan.")
        return []

    product_index = products.index(product_name)

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
# 5. MEMBUAT REKOMENDASI
# =========================

recommendations = recommend_products(
    "Laptop ASUS Intel i5 RAM 16GB SSD 512GB"
)


# =========================
# 6. MENAMPILKAN REKOMENDASI
# =========================

print("\nRekomendasi:")

for index, score in recommendations:
    print(
        products[index],
        "->",
        round(score, 3)
    )