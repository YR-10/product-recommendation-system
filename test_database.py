from src.database import get_connection

connection = get_connection()

print("koneksi MySQL berhasil!")

connection.close()