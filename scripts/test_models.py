from src.recommender import ProductRecommender

print("=== MODEL A ===")

model_a = ProductRecommender(
    feature_mode="description"
)

recommendations_a = model_a.recommend(
    0,
    3
)

print("Query", model_a.products.iloc[0]["nama"])

for index, score in recommendations_a:

    print(
        model_a.products.iloc[index]["nama"],
        "->",
        round(score, 3)
    )

model_a.close()

print("\n=== MODEL B ===")

model_b = ProductRecommender(
    feature_mode="combined"
)

recommendations_b = model_b.recommend(
    0,
    3
)

print("Query:", model_b.products.iloc[0]["nama"])

for index, score in recommendations_b:

    print(
        model_b.products.iloc[index]["nama"],
        "->",
        round(score, 3)
    )

model_b.close()