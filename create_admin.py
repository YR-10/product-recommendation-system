from sqlalchemy import text

from src.auth import hash_password
from src.database import get_engine


USERNAME = "admin"
EMAIL = "admin@productrec.local"

PASSWORD = input(
    "Masukkan password admin: "
)


password_hash = hash_password(
    PASSWORD
)


engine = get_engine()


try:

    with engine.begin() as connection:

        existing = connection.execute(
            text("""
                SELECT id
                FROM users
                WHERE username = :username
                   OR email = :email
                LIMIT 1
            """),
            {
                "username": USERNAME,
                "email": EMAIL
            }
        ).first()


        if existing:

            print(
                "Akun admin sudah ada."
            )

        else:

            connection.execute(
                text("""
                    INSERT INTO users
                    (
                        username,
                        email,
                        password_hash,
                        role
                    )
                    VALUES
                    (
                        :username,
                        :email,
                        :password_hash,
                        'admin'
                    )
                """),
                {
                    "username": USERNAME,
                    "email": EMAIL,
                    "password_hash": password_hash
                }
            )

            print(
                "Akun admin berhasil dibuat."
            )

finally:

    engine.dispose()