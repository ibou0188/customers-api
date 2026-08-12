from fastapi import FastAPI

from app.api.routes.customers import router as customers_router

app = FastAPI(
    title="PayeTonKawa - Customers API",
    description="API REST de gestion des clients",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "PayeTonKawa Customers API is running"
    }


app.include_router(customers_router)
