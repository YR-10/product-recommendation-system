from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text

from src.auth_routes import get_current_user
from src.database import get_engine


router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist"]
)


# =========================
# GET WISHLIST
# =========================

@router.get("")
def get_wishlist(
    current_user: dict = Depends(get_current_user)
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
                        p.harga,
                        w.created_at
                    FROM wishlist w
                    JOIN products p
                        ON w.product_id = p.id
                    JOIN categories c
                        ON p.kategori_id = c.id
                    WHERE w.user_id = :user_id
                    ORDER BY w.created_at DESC
                """),
                {
                    "user_id": current_user["id"]
                }
            ).mappings().all()

        return [dict(row) for row in rows]

    finally:

        engine.dispose()


# =========================
# ADD WISHLIST
# =========================

@router.post("/{product_id}")
def add_wishlist(
    product_id: int,
    current_user: dict = Depends(get_current_user)
):

    engine = get_engine()

    try:

        with engine.begin() as connection:

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

            existing = connection.execute(
                text("""
                    SELECT id
                    FROM wishlist
                    WHERE user_id = :user_id
                      AND product_id = :product_id
                    LIMIT 1
                """),
                {
                    "user_id": current_user["id"],
                    "product_id": product_id
                }
            ).first()

            if existing:

                return {
                    "message": "Product already in wishlist."
                }

            connection.execute(
                text("""
                    INSERT INTO wishlist
                    (
                        user_id,
                        product_id
                    )
                    VALUES
                    (
                        :user_id,
                        :product_id
                    )
                """),
                {
                    "user_id": current_user["id"],
                    "product_id": product_id
                }
            )

        return {
            "message": "Product added to wishlist."
        }

    finally:

        engine.dispose()


# =========================
# DELETE WISHLIST
# =========================

@router.delete("/{product_id}")
def delete_wishlist(
    product_id: int,
    current_user: dict = Depends(get_current_user)
):

    engine = get_engine()

    try:

        with engine.begin() as connection:

            result = connection.execute(
                text("""
                    DELETE FROM wishlist
                    WHERE user_id = :user_id
                      AND product_id = :product_id
                """),
                {
                    "user_id": current_user["id"],
                    "product_id": product_id
                }
            )

        if result.rowcount == 0:

            raise HTTPException(
                status_code=404,
                detail="Product is not in wishlist."
            )

        return {
            "message": "Product removed from wishlist."
        }

    finally:

        engine.dispose()