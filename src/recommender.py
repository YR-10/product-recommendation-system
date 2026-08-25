import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.database import get_engine


class ProductRecommender:

    def __init__(self, feature_mode="combined"):

        self.feature_mode = feature_mode
        self.engine = get_engine()

        query = """
        SELECT
            p.id,
            p.nama,
            p.brand,
            p.jenis,
            c.nama AS kategori,
            p.deskripsi,
            p.ram_gb,
            p.storage_gb,
            p.harga
        FROM products p
        JOIN categories c
            ON p.kategori_id = c.id
        ORDER BY p.id
        """

        self.products = pd.read_sql(
            query,
            self.engine
        )

        self.products["combined_features"] = (
            self.products["nama"] + " "
            + self.products["deskripsi"] + " "
            + self.products["kategori"]
        )

        self.products["description_features"] = (
            self.products["deskripsi"]
        )

        if self.feature_mode == "combined":

            text_data = self.products[
                "combined_features"
            ]

        elif self.feature_mode == "description":

            text_data = self.products[
                "description_features"
            ]

        else:

            raise ValueError(
                "feature_mode harus 'combined' atau 'description'"
            )

        self.vectorizer = TfidfVectorizer()

        self.tfidf_matrix = (
            self.vectorizer.fit_transform(
                text_data
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


    def close(self):

        self.engine.dispose()