from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.recommender import ProductRecommender
from src.relevance import RelevanceEvaluator

from src.auth_routes import router as auth_router
from src.wishlist_routes import router as wishlist_router

from src.auth_routes import router as auth_router
from src.wishlist_routes import router as wishlist_router

from src.admin_routes import router as admin_router

# =========================
# PATH
# =========================

BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = BASE_DIR / "frontend"


# =========================
# RESPONSE MODELS
# =========================

class ProductResponse(BaseModel):

    id: int
    nama: str
    brand: str
    jenis: str
    kategori: str
    deskripsi: str
    ram_gb: int | None
    storage_gb: int | None
    harga: float


class RecommendationResponse(BaseModel):

    id: int
    nama: str
    brand: str
    kategori: str
    harga: float
    similarity: float
    reasons: list[str]


class RecommendationResult(BaseModel):

    product: dict
    recommendations: list[RecommendationResponse]


# =========================
# APP LIFESPAN
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):

    recommender = ProductRecommender(
        feature_mode="combined"
    )

    relevance_evaluator = RelevanceEvaluator(
        threshold=2
    )

    app.state.recommender = recommender
    app.state.relevance_evaluator = (
        relevance_evaluator
    )

    app.state.product_index = {
        int(product_id): index
        for index, product_id
        in enumerate(
            recommender.products["id"]
        )
    }

    yield

    recommender.close()


# =========================
# FASTAPI
# =========================

app = FastAPI(
    title="Product Recommendation API",
    description="API untuk sistem rekomendasi produk",
    version="1.0.0",
    lifespan=lifespan
)
app.include_router(auth_router)
app.include_router(wishlist_router)
app.include_router(admin_router)

# =========================
# STATIC FILES
# =========================

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return FileResponse(
        FRONTEND_DIR / "index.html"
    )

# =========================
# ADMIN PAGE
# =========================

@app.get("/admin")
def admin_page():

    return FileResponse(
        FRONTEND_DIR / "admin.html"
    )

# =========================
# HEALTH
# =========================

@app.get("/health")
def health_check():

    return {
        "status": "ok"
    }


# =========================
# PRODUCTS
# =========================

@app.get(
    "/products",
    response_model=list[ProductResponse]
)
def get_products(request: Request):

    recommender = (
        request.app.state.recommender
    )

    products = recommender.products[
        [
            "id",
            "nama",
            "brand",
            "jenis",
            "kategori",
            "deskripsi",
            "ram_gb",
            "storage_gb",
            "harga"
        ]
    ].copy()

    products = products.astype(object).where(
        pd.notna(products),
        None
    )

    return products.to_dict(
        orient="records"
    )


# =========================
# RECOMMENDATIONS
# =========================

@app.get(
    "/products/{product_id}/recommendations",
    response_model=RecommendationResult
)
def get_recommendations(
    product_id: int,
    request: Request,
    top_n: int = Query(
        default=3,
        ge=1,
        le=10
    )
):

    recommender = (
        request.app.state.recommender
    )

    relevance_evaluator = (
        request.app.state.relevance_evaluator
    )

    product_index = (
        request.app.state.product_index.get(
            product_id
        )
    )

    if product_index is None:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    recommendations = recommender.recommend(
        product_index,
        top_n
    )

    product = recommender.products.iloc[
        product_index
    ]

    result = []

    for index, similarity_score in recommendations:

        recommendation = (
            recommender.products.iloc[index]
        )

        reasons = (
            relevance_evaluator.get_reasons(
                product,
                recommendation
            )
        )

        result.append({
            "id": int(
                recommendation["id"]
            ),
            "nama": (
                recommendation["nama"]
            ),
            "brand": (
                recommendation["brand"]
            ),
            "kategori": (
                recommendation["kategori"]
            ),
            "harga": float(
                recommendation["harga"]
            ),
            "similarity": round(
                float(similarity_score),
                3
            ),
            "reasons": reasons
        })

    return {
        "product": {
            "id": int(product["id"]),
            "nama": product["nama"]
        },
        "recommendations": result
    }