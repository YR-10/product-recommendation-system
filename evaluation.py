recommendations = [
    "Laptop Lenovo",
    "Laptop HP",
    "iPhone 15"
]

relevant_products = [
    "Laptop Lenovo",
    "Laptop HP",
    "Laptop Dell"
]

relevant_count = 0

for product in recommendations:
    if product in relevant_products:
        relevant_count += 1

precision = relevant_count / len(recommendations)

print("Jumlah rekomendasi:", len(recommendations))
print("Jumlah produk relevan:", relevant_count)
print("Precision@3:", round(precision, 3))