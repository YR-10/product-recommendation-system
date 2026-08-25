import pandas as pd

from src.recommender import ProductRecommender

csv_products = pd.read_csv(
    "data/products_v2.csv"
)

recommender = ProductRecommender()

db_products = recommender.products.copy()

print("Jumlah CSV:", len(csv_products))
print("Jumlah DB :", len(db_products))

print("\nKolom CSV:")
print(list(csv_products.columns))

print("\nPerbandingan produk:")

for index in range(len(csv_products)):

    csv_name = csv_products.iloc[index]["nama"]
    db_name = db_products.iloc[index]["nama"]

    print(
        index,
        "| CSV:",
        csv_name,
        "| DB:",
        db_name
    )

recommender.close()