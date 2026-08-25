from src.recommender import ProductRecommender
from src.relevance import RelevanceEvaluator
from src.evaluation import RecommendationEvaluator


recommender = ProductRecommender(
    "data/products_v2.csv"
)


relevance_evaluator = RelevanceEvaluator(
    "data/products_v2.csv",
    threshold=2
)


evaluator = RecommendationEvaluator(
    recommender,
    relevance_evaluator
)


precision, recall = evaluator.evaluate_all(
    top_n=3
)


print(
    "Mean Precision@3:",
    round(precision, 3)
)


if recall is not None:

    print(
        "Mean Recall@3:",
        round(recall, 3)
    )