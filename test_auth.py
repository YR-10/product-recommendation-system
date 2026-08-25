from src.auth import(
    hash_password,
    verify_password
)

password = "PasswordTes123!"

hashed = hash_password(
    password
)

print("Password asli:")
print(password)

print("\nHash:")
print(hashed)

print("\nPassword benar:")
print(
    verify_password(
        password,
        hashed
    )
)

print("\nPassword salah:")
print(
    verify_password(
        "PasswordSalah",
        hashed
    )
)