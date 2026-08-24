import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from relevance import is_relevant


# =========================
# 1. BACA DATA
# =========================

products = pd.read_csv("data/products_v2.csv")


# =========================
# 2. MODEL A
# HANYA DESKRIPSI
# =========================

text_data = products["deskripsi"]


# =========================
# 3. TF-IDF
# =========================

vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(
    text_data
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
# 7. FUNGSI RECALL@3
# =========================

def calculate_recall(product_index, top_n=3):

    query_product = products.iloc[product_index]

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

    if len(relevant_products) == 0:
        return None

    recommendations = recommend_products(
        product_index,
        top_n
    )

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
# 8. EVALUASI SEMUA PRODUK
# =========================

precisions = []
recalls = []

print("Model A + Ground Truth V2")
print("\nHasil setiap produk:\n")

for product_index in range(len(products)):

    precision = calculate_precision(
        product_index
    )

    recall = calculate_recall(
        product_index
    )

    precisions.append(precision)

    if recall is not None:
        recalls.append(recall)

    print(
        products.iloc[product_index]["nama"],
        "-> Precision:",
        round(precision, 3),
        "| Recall:",
        "Tidak dapat dihitung"
        if recall is None
        else round(recall, 3)
    )


# =========================
# 9. MEAN PRECISION
# =========================

mean_precision = (
    sum(precisions)
    / len(precisions)
)


# =========================
# 10. MEAN RECALL
# =========================

mean_recall = (
    sum(recalls)
    / len(recalls)
)


# =========================
# 11. HASIL AKHIR
# =========================

print(
    "\nMean Precision@3 Model A V2:",
    round(mean_precision, 3)
)

print(
    "Mean Recall@3 Model A V2:",
    round(mean_recall, 3)
)