# Product Recommendation System

Sistem rekomendasi produk berbasis **content-based filtering** yang dilengkapi dengan REST API menggunakan FastAPI, database MySQL, autentikasi JWT, wishlist per-user, serta Admin Dashboard untuk mengelola produk.

---

## Overview

Project ini merupakan sistem rekomendasi produk yang menggunakan informasi produk untuk mencari produk lain yang memiliki karakteristik serupa.

Sistem menggunakan kombinasi:

- Nama produk
- Deskripsi produk
- Kategori produk

untuk menghitung kemiripan antarproduk dan menghasilkan rekomendasi.

Aplikasi juga menyediakan:

- User registration dan login
- JWT authentication
- Role-based authorization
- Wishlist per-user
- Product management
- Admin Dashboard
- Search dan filtering
- Pagination
- Explainable recommendation

---

## Features

### Recommendation System

Sistem menghasilkan rekomendasi berdasarkan similarity antarproduk.

Contoh:

```text
Query:
Laptop ASUS

Recommendations:
Laptop Lenovo -> 0.795
Laptop HP     -> 0.678
Laptop Dell   -> 0.610