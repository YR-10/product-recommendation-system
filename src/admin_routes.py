from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from pydantic import BaseModel

from sqlalchemy import text

from src.auth_routes import require_admin
from src.database import get_engine


# =========================
# ROUTER
# =========================

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


# =========================
# PRODUCT CREATE MODEL
# =========================

class AdminProductCreate(BaseModel):

    nama: str
    brand: str
    jenis: str
    kategori_id: int
    deskripsi: str

    ram_gb: int | None = None
    storage_gb: int | None = None

    harga: float

# =========================
# PRODUCT UPDATE MODEL
# =========================

class AdminProductUpdate(BaseModel):

    nama: str
    brand: str
    jenis: str
    kategori_id: int
    deskripsi: str
    ram_gb: int | None = None
    storage_gb: int | None = None
    harga: float

# =========================
# GET ADMIN PRODUCTS
# =========================

@router.get("/products")
def get_admin_products(
    current_admin: dict = Depends(
        require_admin
    )
):

    engine = get_engine()

    try:

        with engine.connect() as connection:

            rows = connection.execute(
                text("""
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
                    LEFT JOIN categories c
                        ON p.kategori_id = c.id
                    ORDER BY p.id ASC
                """)
            ).mappings().all()


        return {
            "admin": {
                "id": current_admin["id"],
                "username": current_admin["username"],
                "role": current_admin["role"]
            },
            "products": [
                dict(row)
                for row in rows
            ]
        }

    finally:

        engine.dispose()

# =========================
# UPDATE ADMIN PRODUCT
# =========================

@router.put("/products/{product_id}")
def update_admin_product(
    product_id: int,
    data: AdminProductUpdate,
    current_admin: dict = Depends(
        require_admin
    )
):

    nama = data.nama.strip()
    brand = data.brand.strip()
    jenis = data.jenis.strip()
    deskripsi = data.deskripsi.strip()


    if not nama:

        raise HTTPException(
            status_code=400,
            detail="Nama produk wajib diisi."
        )


    if not brand:

        raise HTTPException(
            status_code=400,
            detail="Brand wajib diisi."
        )


    if not jenis:

        raise HTTPException(
            status_code=400,
            detail="Jenis produk wajib diisi."
        )


    if data.harga < 0:

        raise HTTPException(
            status_code=400,
            detail="Harga tidak boleh negatif."
        )


    if (
        data.ram_gb is not None
        and data.ram_gb < 0
    ):

        raise HTTPException(
            status_code=400,
            detail="RAM tidak boleh negatif."
        )


    if (
        data.storage_gb is not None
        and data.storage_gb < 0
    ):

        raise HTTPException(
            status_code=400,
            detail="Storage tidak boleh negatif."
        )


    engine = get_engine()


    try:

        with engine.begin() as connection:

            # =========================
            # CHECK PRODUCT
            # =========================

            product = connection.execute(
                text("""
                    SELECT id
                    FROM products
                    WHERE id = :product_id
                    LIMIT 1
                """),
                {
                    "product_id": product_id
                }
            ).first()


            if not product:

                raise HTTPException(
                    status_code=404,
                    detail="Product not found."
                )


            # =========================
            # CHECK CATEGORY
            # =========================

            category = connection.execute(
                text("""
                    SELECT
                        id,
                        nama
                    FROM categories
                    WHERE id = :kategori_id
                    LIMIT 1
                """),
                {
                    "kategori_id":
                        data.kategori_id
                }
            ).mappings().first()


            if not category:

                raise HTTPException(
                    status_code=400,
                    detail="Kategori tidak ditemukan."
                )


            # =========================
            # UPDATE PRODUCT
            # =========================

            connection.execute(
                text("""
                    UPDATE products
                    SET
                        nama = :nama,
                        brand = :brand,
                        jenis = :jenis,
                        kategori_id = :kategori_id,
                        deskripsi = :deskripsi,
                        ram_gb = :ram_gb,
                        storage_gb = :storage_gb,
                        harga = :harga
                    WHERE id = :product_id
                """),
                {
                    "product_id": product_id,
                    "nama": nama,
                    "brand": brand,
                    "jenis": jenis,
                    "kategori_id":
                        data.kategori_id,
                    "deskripsi": deskripsi,
                    "ram_gb": data.ram_gb,
                    "storage_gb":
                        data.storage_gb,
                    "harga": data.harga
                }
            )


        return {
            "message":
                "Product updated successfully.",

            "product": {

                "id": product_id,

                "nama": nama,

                "brand": brand,

                "jenis": jenis,

                "kategori_id":
                    data.kategori_id,

                "kategori":
                    category["nama"],

                "deskripsi":
                    deskripsi,

                "ram_gb":
                    data.ram_gb,

                "storage_gb":
                    data.storage_gb,

                "harga":
                    data.harga
            }
        }


    finally:

        engine.dispose()


# =========================
# CREATE ADMIN PRODUCT
# =========================

@router.post("/products")
def create_admin_product(
    data: AdminProductCreate,
    current_admin: dict = Depends(
        require_admin
    )
):

    nama = data.nama.strip()
    brand = data.brand.strip()
    jenis = data.jenis.strip()
    deskripsi = data.deskripsi.strip()


    # =========================
    # BASIC VALIDATION
    # =========================

    if not nama:

        raise HTTPException(
            status_code=400,
            detail="Nama produk wajib diisi."
        )


    if not brand:

        raise HTTPException(
            status_code=400,
            detail="Brand wajib diisi."
        )


    if not jenis:

        raise HTTPException(
            status_code=400,
            detail="Jenis produk wajib diisi."
        )


    if data.harga < 0:

        raise HTTPException(
            status_code=400,
            detail="Harga tidak boleh negatif."
        )


    if data.ram_gb is not None and data.ram_gb < 0:

        raise HTTPException(
            status_code=400,
            detail="RAM tidak boleh negatif."
        )


    if (
        data.storage_gb is not None
        and data.storage_gb < 0
    ):

        raise HTTPException(
            status_code=400,
            detail="Storage tidak boleh negatif."
        )


    engine = get_engine()


    try:

        with engine.begin() as connection:

            # =========================
            # CHECK CATEGORY
            # =========================

            category = connection.execute(
                text("""
                    SELECT
                        id,
                        nama
                    FROM categories
                    WHERE id = :kategori_id
                    LIMIT 1
                """),
                {
                    "kategori_id":
                        data.kategori_id
                }
            ).mappings().first()


            if not category:

                raise HTTPException(
                    status_code=400,
                    detail="Kategori tidak ditemukan."
                )


            # =========================
            # INSERT PRODUCT
            # =========================

            result = connection.execute(
                text("""
                    INSERT INTO products
                    (
                        nama,
                        brand,
                        jenis,
                        kategori_id,
                        deskripsi,
                        ram_gb,
                        storage_gb,
                        harga
                    )
                    VALUES
                    (
                        :nama,
                        :brand,
                        :jenis,
                        :kategori_id,
                        :deskripsi,
                        :ram_gb,
                        :storage_gb,
                        :harga
                    )
                """),
                {
                    "nama": nama,
                    "brand": brand,
                    "jenis": jenis,
                    "kategori_id":
                        data.kategori_id,
                    "deskripsi": deskripsi,
                    "ram_gb": data.ram_gb,
                    "storage_gb":
                        data.storage_gb,
                    "harga": data.harga
                }
            )


            product_id = result.lastrowid


        return {
            "message":
                "Product created successfully.",

            "product": {

                "id": product_id,

                "nama": nama,

                "brand": brand,

                "jenis": jenis,

                "kategori_id":
                    data.kategori_id,

                "kategori":
                    category["nama"],

                "deskripsi":
                    deskripsi,

                "ram_gb":
                    data.ram_gb,

                "storage_gb":
                    data.storage_gb,

                "harga":
                    data.harga
            }
        }


    finally:

        engine.dispose()

# =========================
# DELETE ADMIN PRODUCT
# =========================

@router.delete("/products/{product_id}")
def delete_admin_product(
    product_id: int,
    current_admin: dict = Depends(
        require_admin
    )
):

    engine = get_engine()

    try:

        with engine.begin() as connection:

            # =========================
            # CHECK PRODUCT
            # =========================

            product = connection.execute(
                text("""
                    SELECT
                        id,
                        nama
                    FROM products
                    WHERE id = :product_id
                    LIMIT 1
                """),
                {
                    "product_id": product_id
                }
            ).mappings().first()


            if not product:

                raise HTTPException(
                    status_code=404,
                    detail="Product not found."
                )


            # =========================
            # DELETE PRODUCT
            # =========================

            connection.execute(
                text("""
                    DELETE FROM products
                    WHERE id = :product_id
                """),
                {
                    "product_id": product_id
                }
            )


        return {
            "message":
                "Product deleted successfully.",

            "product": {
                "id":
                    product["id"],

                "nama":
                    product["nama"]
            }
        }


    finally:

        engine.dispose()

# =========================
# GET ADMIN CATEGORIES
# =========================

@router.get("/categories")
def get_admin_categories(
    current_admin: dict = Depends(
        require_admin
    )
):

    engine = get_engine()

    try:

        with engine.connect() as connection:

            rows = connection.execute(
                text("""
                    SELECT
                        id,
                        nama
                    FROM categories
                    ORDER BY id ASC
                """)
            ).mappings().all()


        return {
            "categories": [
                dict(row)
                for row in rows
            ]
        }

    finally:

        engine.dispose()

# =========================
# GET ADMIN USERS
# =========================

@router.get("/users")
def get_admin_users(
    current_admin: dict = Depends(
        require_admin
    )
):

    engine = get_engine()

    try:

        with engine.connect() as connection:

            rows = connection.execute(
                text("""
                    SELECT
                        id,
                        username,
                        email,
                        role
                    FROM users
                    ORDER BY id ASC
                """)
            ).mappings().all()


        return {
            "users": [
                dict(row)
                for row in rows
            ]
        }

    finally:

        engine.dispose()