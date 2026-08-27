from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from pydantic import (
    BaseModel,
    EmailStr
)

from sqlalchemy import text

from jwt.exceptions import InvalidTokenError

from src.auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password
)

from src.database import get_engine


# =========================
# ROUTER
# =========================

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================
# OAUTH2
# =========================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# =========================
# RESPONSE MODELS
# =========================

class RegisterRequest(BaseModel):

    username: str
    email: EmailStr
    password: str


class TokenResponse(BaseModel):

    access_token: str
    token_type: str


class UserResponse(BaseModel):

    id: int
    username: str
    email: str
    role: str


# =========================
# REGISTER
# =========================

@router.post("/register")
def register_user(
    data: RegisterRequest
):

    username = data.username.strip()
    email = data.email.strip().lower()


    if len(username) < 3:

        raise HTTPException(
            status_code=400,
            detail="Username minimal 3 karakter."
        )


    if len(data.password) < 8:

        raise HTTPException(
            status_code=400,
            detail="Password minimal 8 karakter."
        )


    engine = get_engine()


    try:

        with engine.begin() as connection:

            existing_user = connection.execute(
                text("""
                    SELECT id
                    FROM users
                    WHERE username = :username
                       OR email = :email
                    LIMIT 1
                """),
                {
                    "username": username,
                    "email": email
                }
            ).first()


            if existing_user:

                raise HTTPException(
                    status_code=409,
                    detail="Username atau email sudah digunakan."
                )


            password_hashed = hash_password(
                data.password
            )


            connection.execute(
                text("""
                    INSERT INTO users
                    (
                        username,
                        email,
                        password_hash
                    )
                    VALUES
                    (
                        :username,
                        :email,
                        :password_hash
                    )
                """),
                {
                    "username": username,
                    "email": email,
                    "password_hash": password_hashed
                }
            )


        return {
            "message": "Registrasi berhasil."
        }


    finally:

        engine.dispose()


# =========================
# LOGIN
# =========================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    username = form_data.username.strip()


    engine = get_engine()


    try:

        with engine.connect() as connection:

            user = connection.execute(
                text("""
                    SELECT
                        id,
                        username,
                        password_hash,
                        role
                    FROM users
                    WHERE username = :username
                    LIMIT 1
                """),
                {
                    "username": username
                }
            ).mappings().first()


        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username atau password salah.",
                headers={
                    "WWW-Authenticate": "Bearer"
                }
            )


        valid_password = verify_password(
            form_data.password,
            user["password_hash"]
        )


        if not valid_password:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username atau password salah.",
                headers={
                    "WWW-Authenticate": "Bearer"
                }
            )


        access_token = create_access_token(
            user_id=user["id"],
            username=user["username"],
            role=user["role"]
        )


        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


    finally:

        engine.dispose()


# =========================
# CURRENT USER
# =========================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = decode_access_token(
            token
        )


        user_id = payload.get(
            "sub"
        )


        if not user_id:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token tidak valid.",
                headers={
                    "WWW-Authenticate": "Bearer"
                }
            )


        user_id = int(user_id)


    except (
        InvalidTokenError,
        ValueError,
        TypeError
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau sudah kedaluwarsa.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    engine = get_engine()


    try:

        with engine.connect() as connection:

            user = connection.execute(
                text("""
                    SELECT
                        id,
                        username,
                        email,
                        role
                    FROM users
                    WHERE id = :user_id
                    LIMIT 1
                """),
                {
                    "user_id": user_id
                }
            ).mappings().first()


        if not user:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User tidak ditemukan.",
                headers={
                    "WWW-Authenticate": "Bearer"
                }
            )


        return dict(user)


    finally:

        engine.dispose()


# =========================
# REQUIRE ADMIN
# =========================

def require_admin(
    current_user: dict = Depends(
        get_current_user
    )
):

    if current_user["role"] != "admin":

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )


    return current_user


# =========================
# CURRENT USER ENDPOINT
# =========================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: dict = Depends(
        get_current_user
    )
):

    return current_user


# =========================
# ADMIN TEST ENDPOINT
# =========================

@router.get(
    "/admin-test"
)
def admin_test(
    current_admin: dict = Depends(
        require_admin
    )
):

    return {
        "message": "Admin access granted.",
        "user": {
            "id": current_admin["id"],
            "username": current_admin["username"],
            "role": current_admin["role"]
        }
    }