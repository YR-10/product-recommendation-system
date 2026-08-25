from src.relevance import RelevanceEvaluator

evaluator = RelevanceEvaluator(
    "data/products_v2.csv",
    threshold=2
)

product_a = evaluator.products.iloc[0]
product_b = evaluator.products.iloc[1]

score = evaluator.calculate_score(
    product_a,
    product_b
)

relevant = evaluator.is_relevant(
    product_a,
    product_b
)

print("Produk A:", product_a["nama"])
print("Produk B:", product_b["nama"])
print("Skor relevansi:", score)
print("Relevan:", relevant)