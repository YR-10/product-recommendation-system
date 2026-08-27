from sqlalchemy import text

from src.database import get_engine


def test_database_connection():

    engine = get_engine()

    try:

        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT 1")
            )

            assert result.scalar() == 1

    finally:

        engine.dispose()