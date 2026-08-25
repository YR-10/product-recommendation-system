import pandas as pd

from src.recommender import ProductRecommender
from src.relevance import RelevanceEvaluator


csv_products = pd.read_csv(
    "data/products_v2.csv"
)

# Samakan makna 0 pada storage menjadi NULL
# untuk produk yang memang tidak memiliki storage.
csv_products["storage_gb"] = csv_products[
    "storage_gb"
].replace(0, pd.NA)


recommender = ProductRecommender()

db_products = recommender.products.copy()


evaluator = RelevanceEvaluator(
    threshold=2
)


differences = 0


for index_a in range(len(csv_products)):

    for index_b in range(len(csv_products)):

        csv_a = csv_products.iloc[index_a]
        csv_b = csv_products.iloc[index_b]

        db_a = db_products.iloc[index_a]
        db_b = db_products.iloc[index_b]

        csv_score = evaluator.calculate_score(
            csv_a,
            csv_b
        )

        db_score = evaluator.calculate_score(
            db_a,
            db_b
        )

        if csv_score != db_score:

            differences += 1

            print(
                csv_a["nama"],
                "vs",
                csv_b["nama"],
                "| CSV:",
                csv_score,
                "| DB:",
                db_score
            )


print(
    "\nJumlah perbedaan skor:",
    differences
)


recommender.close()