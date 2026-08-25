# Experiment Results

## Dataset

- Number of products: 30
- Product attributes:
  - id
  - nama
  - brand
  - jenis
  - kategori
  - deskripsi
  - ram_gb
  - storage_gb
  - harga

## Recommendation Models

### Model A
TF-IDF menggunakan:
- deskripsi

### Model B
TF-IDF menggunakan:
- nama
- deskripsi
- kategori

## Ground Truth

Relevance score dihitung berdasarkan:
- jenis
- kategori
- RAM
- storage

### Threshold 2
Score >= 2 dianggap relevan.

### Threshold 3
Score >= 3 dianggap relevan.

## Results

| Threshold | Model | Precision@3 | Recall@3 |
|-----------|-------|-------------|----------|
| 2 | Model A | 0.789 | 0.353 |
| 2 | Model B | 0.878 | 0.472 |
| 3 | Model A | 0.522 | 0.327 |
| 3 | Model B | 0.578 | 0.589 |

## Initial Observation

Model B menghasilkan Precision@3 dan Recall@3 yang lebih tinggi
daripada Model A pada kedua threshold yang diuji.

Hasil ini masih merupakan eksperimen awal menggunakan dataset
simulasi dan ground truth berbasis atribut.

## Final Database-Based Evaluation

Untuk pipeline aplikasi final, database MySQL digunakan sebagai
sumber data utama. Atribut yang tidak berlaku untuk suatu produk
direpresentasikan sebagai NULL dan tidak memberikan kontribusi
terhadap relevance score.

Ground truth:
- jenis
- kategori
- RAM jika tersedia pada kedua produk
- storage jika tersedia pada kedua produk

Threshold:
- score >= 2 dianggap relevan

### Final Results

| Model | Features | Precision@3 | Recall@3 |
|-------|----------|-------------|----------|
| Model A | Deskripsi | 0.667 | 0.311 |
| Model B | Nama + Deskripsi + Kategori | 0.733 | 0.519 |

### Final Observation

Model B menghasilkan Precision@3 dan Recall@3 yang lebih tinggi
daripada Model A pada pipeline berbasis database.

Model B digunakan sebagai recommendation model utama aplikasi,
sedangkan Model A digunakan sebagai baseline pembanding.