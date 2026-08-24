import pandas as pd

products = pd.read_csv("data/products_v2.csv")

products = products.iloc[0]

print("nama:", products["nama"])
print("Brand:", products["brand"])
print("Jenis:", products["jenis"])
print("Kategori:", products["kategori"])
print("RAM:", products["ram_gb"])
print("Storage:", products["storage_gb"])
print("Harga:", products["harga"])
