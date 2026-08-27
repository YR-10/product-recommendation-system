from src.recommender import ProductRecommender
from src.relevance import RelevanceEvaluator
from src.evaluation import RecommendationEvaluator


# =====================================
# GROUND TRUTH
# =====================================

relevance_evaluator = RelevanceEvaluator(
    threshold=2
)


# =====================================
# MODEL A
# DESKRIPSI SAJA
# =====================================

model_a = ProductRecommender(
    feature_mode="description"
)

evaluator_a = RecommendationEvaluator(
    model_a,
    relevance_evaluator
)

precision_a, recall_a = evaluator_a.evaluate_all(
    top_n=3
)


# =====================================
# MODEL B
# NAMA + DESKRIPSI + KATEGORI
# =====================================

model_b = ProductRecommender(
    feature_mode="combined"
)

evaluator_b = RecommendationEvaluator(
    model_b,
    relevance_evaluator
)

precision_b, recall_b = evaluator_b.evaluate_all(
    top_n=3
)


# =====================================
# HASIL
# =====================================

print("=== FINAL EVALUATION ===")

print("\nModel A - Deskripsi saja")

print(
    "Precision@3:",
    round(precision_a, 3)
)

print(
    "Recall@3:",
    round(recall_a, 3)
)


print("\nModel B - Nama + Deskripsi + Kategori")

print(
    "Precision@3:",
    round(precision_b, 3)
)

print(
    "Recall@3:",
    round(recall_b, 3)
)


# =====================================
# CLEANUP
# =====================================

model_a.close()
model_b.close()