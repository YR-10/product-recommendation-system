import pandas as pd

products = pd.read_csv("data/products.csv")

print (products)

print("\nNama Kolom:")
print(products.columns)

print("\nJumlah baris dan kolom:")
print(products.shape)

print("\nLima data pertama:")
print(products.head())

print("\nProduk pertama:")
print(products.iloc[0])

print("\nNama produk pertama:")
print(products.iloc[0]["nama"])

print("\nJumlah produk:")
print(len(products))

print("\nJumlah produk berdasarkan kategori:")
print(products["kategori"].value_counts())

