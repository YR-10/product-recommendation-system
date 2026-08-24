import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


products = pd.read_csv("data/products.csv")


products["combined_features"] = (
    products["nama"] + " "
    + products["deskripsi"] + " "
    + products["kategori"]
)


print("Produk 1:")
print(products.iloc[0]["combined_features"])

print("\nProduk 2:")
print(products.iloc[1]["combined_features"])


vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(
    products["combined_features"]
)


similarity = cosine_similarity(tfidf_matrix)


print("\nSimilarity ASUS vs Lenovo:")
print(similarity[0][1])

def recommend_products(product_name, top_n=3):

    if product_name not in products["nama"].values:
        print("Produk tidak ditemukan.")
        return []

    product_index = products.index[
        products["nama"] == product_name
    ][0]

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


recommendations = recommend_products("Laptop ASUS")

print("\nRekomendasi Model B:")

for index, score in recommendations:
    print(
        products.iloc[index]["nama"],
        "->",
        round(score, 3)
    )
    
def recommend_products(product_name, top_n=3):
    if product_name not in products["nama"].values:
        print("Produk tidak ditemukan,")
        return[]

    product_index = products.index[
        products["nama"] == product_name
    ][0]

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

    recommendations = recommend_products
    ("Laptop ASUS")

    print("\nRekomendasi Model B:")
    for index, score in recommendations:
        print(
            products.iloc[index]["nama"],
            "->",
            round(score, 3)
        )

