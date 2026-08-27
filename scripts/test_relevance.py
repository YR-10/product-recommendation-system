from src.recommender import ProductRecommender
from src.relevance import RelevanceEvaluator


recommender = ProductRecommender()

evaluator = RelevanceEvaluator(
    threshold=2
)


product_a = recommender.products.iloc[0]
product_b = recommender.products.iloc[1]


score = evaluator.calculate_score(
    product_a,
    product_b
)

relevant = evaluator.is_relevant(
    product_a,
    product_b
)

reasons = evaluator.get_reasons(
    product_a,
    product_b
)


print("Produk A:", product_a["nama"])
print("Produk B:", product_b["nama"])
print("Skor relevansi:", score)
print("Relevan:", relevant)

print("\nAlasan rekomendasi:")

for reason in reasons:
    print("-", reason)


recommender.close()