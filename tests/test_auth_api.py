import uuid

from fastapi.testclient import TestClient
from sqlalchemy import text

from src.api import app
from src.database import get_engine


client = TestClient(app)


def test_register_login_and_me():

    username = (
        f"test_api_{uuid.uuid4().hex[:10]}"
    )

    email = (
        f"{username}@example.com"
    )

    password = "PasswordTest123!"

    try:

        # =========================
        # REGISTER
        # =========================

        response = client.post(
            "/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )

        assert response.status_code == 200

        data = response.json()

        assert data["message"] == (
            "Registrasi berhasil."
        )


        # =========================
        # LOGIN
        # =========================

        response = client.post(
            "/auth/login",
            data={
                "username": username,
                "password": password
            }
        )

        assert response.status_code == 200

        token_data = response.json()

        assert "access_token" in token_data

        assert (
            token_data["token_type"]
            == "bearer"
        )

        token = token_data["access_token"]


        # =========================
        # /AUTH/ME
        # =========================

        response = client.get(
            "/auth/me",
            headers={
                "Authorization":
                    f"Bearer {token}"
            }
        )

        assert response.status_code == 200

        user = response.json()

        assert user["username"] == username

        assert user["email"] == email

        assert user["role"] == "user"


    finally:

        # =========================
        # CLEANUP
        # =========================

        engine = get_engine()

        try:

            with engine.begin() as connection:

                connection.execute(
                    text("""
                        DELETE FROM users
                        WHERE username = :username
                    """),
                    {
                        "username": username
                    }
                )

        finally:

            engine.dispose()


def test_invalid_login():

    response = client.post(
        "/auth/login",
        data={
            "username":
                "username_that_should_not_exist",
            "password":
                "WrongPassword123!"
        }
    )

    assert response.status_code == 401


def test_invalid_token():

    response = client.get(
        "/auth/me",
        headers={
            "Authorization":
                "Bearer abc.def.ghi"
        }
    )

    assert response.status_code == 401