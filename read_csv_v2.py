import pandas as pd

products = pd.read_csv("data/products_v2.csv")

print(products)

print("\nNama kolom:")
print(products.columns)

print("\nUkuran dataset:")
print(products.shape)