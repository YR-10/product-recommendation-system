import pandas as pd

from fastapi import FastAPI

from src.recommender import ProductRecommender

from fastapi import FastAPI, HTTPException, Query


app = FastAPI(
    title="Product Recommendation API",
    description="API untuk sistem rekomendasi produk",
    version="1.0.0"
)


@app.get("/health")
def health_check():

    return {
        "status": "ok"
    }


@app.get("/products")
def get_products():

    recommender = ProductRecommender(
        feature_mode="combined"
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

    recommender.close()

    products = products.astype(object).where(
        pd.notna(products),
        None
    )

    return products.to_dict(
        orient="records"
    )

@app.get("/products/{product_id}/recommendations")
def get_recommendations(
    product_id: int,
    top_n: int = Query(
        default=3,
        ge=1,
        le=10
    )
):

    recommender = ProductRecommender(
        feature_mode="combined"
    )

    products = recommender.products

    matching_rows = products.index[
        products["id"] == product_id
    ].tolist()

    if not matching_rows:

        recommender.close()

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product_index = matching_rows[0]

    recommendations = recommender.recommend(
        product_index,
        top_n
    )

    product = products.iloc[
        product_index
    ]

    result = []

    for index, similarity_score in recommendations:

        recommendation = products.iloc[index]

        result.append({
            "id": int(recommendation["id"]),
            "nama": recommendation["nama"],
            "brand": recommendation["brand"],
            "kategori": recommendation["kategori"],
            "harga": float(recommendation["harga"]),
            "similarity": round(
                float(similarity_score),
                3
            )
        })

    recommender.close()

    return {
        "product": {
            "id": int(product["id"]),
            "nama": product["nama"]
        },
        "recommendations": result
    }