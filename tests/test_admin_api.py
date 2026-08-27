from fastapi.testclient import TestClient
from sqlalchemy import text

from src.api import app
from src.auth import create_access_token
from src.database import get_engine


client = TestClient(app)


def get_admin_token():
    return create_access_token(
        user_id=2,
        username="admin",
        role="admin"
    )


def get_user_token():
    return create_access_token(
        user_id=1,
        username="katarina",
        role="user"
    )


def test_admin_can_read_products():

    token = get_admin_token()

    response = client.get(
        "/admin/products",
        headers={
            "Authorization":
                f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "products" in data

    assert isinstance(
        data["products"],
        list
    )


def test_admin_can_read_categories():

    token = get_admin_token()

    response = client.get(
        "/admin/categories",
        headers={
            "Authorization":
                f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "categories" in data

    assert isinstance(
        data["categories"],
        list
    )


def test_admin_can_read_users():

    token = get_admin_token()

    response = client.get(
        "/admin/users",
        headers={
            "Authorization":
                f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "users" in data

    assert isinstance(
        data["users"],
        list
    )


def test_regular_user_cannot_access_admin():

    token = get_user_token()

    endpoints = [
        "/admin/products",
        "/admin/categories",
        "/admin/users"
    ]

    for endpoint in endpoints:

        response = client.get(
            endpoint,
            headers={
                "Authorization":
                    f"Bearer {token}"
            }
        )

        assert response.status_code == 403


def test_admin_can_create_update_delete_product():

    token = get_admin_token()

    product_name = (
        "Automated Test Product"
    )

    # =========================
    # CREATE
    # =========================

    create_response = client.post(
        "/admin/products",
        headers={
            "Authorization":
                f"Bearer {token}"
        },
        json={
            "nama": product_name,
            "brand": "TestBrand",
            "jenis": "Test Product",
            "kategori_id": 1,
            "deskripsi":
                "Product created by automated test.",
            "ram_gb": 8,
            "storage_gb": 256,
            "harga": 1000000
        }
    )

    assert create_response.status_code == 200

    created_data = create_response.json()

    product = created_data["product"]

    product_id = product["id"]

    try:

        assert product["nama"] == product_name

        # =========================
        # UPDATE
        # =========================

        update_response = client.put(
            f"/admin/products/{product_id}",
            headers={
                "Authorization":
                    f"Bearer {token}"
            },
            json={
                "nama":
                    "Automated Test Product Updated",
                "brand":
                    "TestBrand Updated",
                "jenis":
                    "Test Product",
                "kategori_id":
                    1,
                "deskripsi":
                    "Updated by automated test.",
                "ram_gb":
                    16,
                "storage_gb":
                    512,
                "harga":
                    1500000
            }
        )

        assert update_response.status_code == 200

        update_data = update_response.json()

        assert (
            update_data["product"]["nama"]
            ==
            "Automated Test Product Updated"
        )

        # =========================
        # DELETE
        # =========================

        delete_response = client.delete(
            f"/admin/products/{product_id}",
            headers={
                "Authorization":
                    f"Bearer {token}"
            }
        )

        assert delete_response.status_code == 200

        delete_data = delete_response.json()

        assert (
            delete_data["product"]["id"]
            ==
            product_id
        )

    finally:

        # =========================
        # SAFETY CLEANUP
        # =========================

        engine = get_engine()

        try:

            with engine.begin() as connection:

                connection.execute(
                    text("""
                        DELETE FROM products
                        WHERE id = :product_id
                    """),
                    {
                        "product_id":
                            product_id
                    }
                )

        finally:

            engine.dispose()