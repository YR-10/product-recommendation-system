import pandas as pd

from src.recommender import ProductRecommender


csv_products = pd.read_csv(
    "data/products_v2.csv"
)

recommender = ProductRecommender()

db_products = recommender.products.copy()


columns_to_compare = [
    "brand",
    "jenis",
    "kategori",
    "deskripsi",
    "ram_gb",
    "storage_gb",
    "harga"
]


print("Perbedaan data:\n")


differences_found = False


for index in range(len(csv_products)):

    for column in columns_to_compare:

        csv_value = csv_products.iloc[index][column]
        db_value = db_products.iloc[index][column]

        csv_missing = pd.isna(csv_value)
        db_missing = pd.isna(db_value)

        values_equal = (
            csv_missing and db_missing
        ) or (
            csv_value == db_value
        )

        if not values_equal:

            differences_found = True

            print(
                f"Produk: {csv_products.iloc[index]['nama']}"
            )

            print(
                f"Kolom : {column}"
            )

            print(
                f"CSV   : {csv_value!r}"
            )

            print(
                f"DB    : {db_value!r}"
            )

            print()


recommender.close()


if not differences_found:

    print("Tidak ada perbedaan nilai.")