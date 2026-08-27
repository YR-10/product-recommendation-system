import pandas as pd

from src.database import get_engine


engine = get_engine()


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


products = pd.read_sql(
    query,
    engine
)


print("Jumlah produk:", len(products))

print("\nLima produk pertama:")
print(products.head())


engine.dispose()