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
# 6. FUNGSI RECALL@3
# =========================

def calculate_recall(product_index, top_n=3):

    query_product = products.iloc[product_index]

    # Cari semua produk yang relevan
    relevant_products = []

    for index in range(len(products)):

        if index == product_index:
            continue

        candidate_product = products.iloc[index]

        if is_relevant(
            query_product,
            candidate_product
        ):
            relevant_products.append(index)

    # Tidak ada produk relevan lain
    if len(relevant_products) == 0:
        return None

    # Ambil rekomendasi Top-N
    recommendations = recommend_products(
        product_index,
        top_n
    )

    # Hitung berapa produk relevan yang berhasil ditemukan
    relevant_retrieved = 0

    for index, score in recommendations:

        if index in relevant_products:
            relevant_retrieved += 1

    recall = (
        relevant_retrieved
        / len(relevant_products)
    )

    return recall


# =========================
# 7. EVALUASI SEMUA PRODUK
# =========================

recalls = []

print("Model B + Ground Truth V2")
print("\nRecall@3 setiap produk:\n")

for product_index in range(len(products)):

    recall = calculate_recall(
        product_index
    )

    if recall is not None:

        recalls.append(recall)

        print(
            products.iloc[product_index]["nama"],
            "->",
            round(recall, 3)
        )

    else:

        print(
            products.iloc[product_index]["nama"],
            "-> Tidak dapat dihitung"
        )


# =========================
# 8. MEAN RECALL@3
# =========================

mean_recall = sum(recalls) / len(recalls)

print(
    "\nMean Recall@3 Model B V2:",
    round(mean_recall, 3)
)