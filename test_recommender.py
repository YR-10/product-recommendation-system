from src.recommender import ProductRecommender


recommender = ProductRecommender(
    "data/products_v2.csv"
)


recommendations = recommender.recommend(
    0,
    3
)


print("Rekomendasi untuk:")
print(
    recommender.products.iloc[0]["nama"]
)


print("\nHasil rekomendasi:")

for index, score in recommendations:

    print(
        recommender.products.iloc[index]["nama"],
        "->",
        round(score, 3)
    )