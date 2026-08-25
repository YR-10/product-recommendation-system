from src.recommender import ProductRecommender
from src.relevance import RelevanceEvaluator


class RecommendationEvaluator:

    def __init__(
        self,
        recommender,
        relevance_evaluator
    ):

        self.recommender = recommender
        self.relevance_evaluator = relevance_evaluator


    def calculate_precision(
        self,
        product_index,
        top_n=3
    ):

        recommendations = (
            self.recommender.recommend(
                product_index,
                top_n
            )
        )

        query_product = (
            self.recommender.products.iloc[
                product_index
            ]
        )

        relevant_count = 0

        for index, score in recommendations:

            recommendation_product = (
                self.recommender.products.iloc[index]
            )

            if self.relevance_evaluator.is_relevant(
                query_product,
                recommendation_product
            ):
                relevant_count += 1

        return (
            relevant_count
            / len(recommendations)
        )


    def calculate_recall(
        self,
        product_index,
        top_n=3
    ):

        query_product = (
            self.recommender.products.iloc[
                product_index
            ]
        )

        relevant_products = []

        for index in range(
            len(self.recommender.products)
        ):

            if index == product_index:
                continue

            candidate_product = (
                self.recommender.products.iloc[index]
            )

            if self.relevance_evaluator.is_relevant(
                query_product,
                candidate_product
            ):
                relevant_products.append(index)

        if len(relevant_products) == 0:
            return None

        recommendations = (
            self.recommender.recommend(
                product_index,
                top_n
            )
        )

        relevant_retrieved = 0

        for index, score in recommendations:

            if index in relevant_products:
                relevant_retrieved += 1

        return (
            relevant_retrieved
            / len(relevant_products)
        )


    def evaluate_all(self, top_n=3):

        precisions = []
        recalls = []

        for product_index in range(
            len(self.recommender.products)
        ):

            precision = self.calculate_precision(
                product_index,
                top_n
            )

            recall = self.calculate_recall(
                product_index,
                top_n
            )

            precisions.append(precision)

            if recall is not None:
                recalls.append(recall)

        mean_precision = (
            sum(precisions)
            / len(precisions)
        )

        mean_recall = (
            sum(recalls)
            / len(recalls)
            if recalls
            else None
        )

        return mean_precision, mean_recall