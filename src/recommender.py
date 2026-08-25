import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ProductRecommender:

    def __init__(self, data_path):

        self.products = pd.read_csv(data_path)

        self.products["combined_features"] = (
            self.products["nama"] + " "
            + self.products["deskripsi"] + " "
            + self.products["kategori"]
        )

        self.vectorizer = TfidfVectorizer()

        self.tfidf_matrix = (
            self.vectorizer.fit_transform(
                self.products["combined_features"]
            )
        )

        self.similarity = cosine_similarity(
            self.tfidf_matrix
        )

    def recommend(self, product_index, top_n=3):

        similarity_scores = list(
            enumerate(
                self.similarity[product_index]
            )
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