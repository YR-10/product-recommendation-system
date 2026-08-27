from sqlalchemy import text

from src.database import get_engine


engine = get_engine()


with engine.connect() as connection:

    result = connection.execute(
        text("SELECT COUNT(*) FROM users")
    )

    count = result.scalar()

    print(
        "Jumlah user:",
        count
    )


engine.dispose()