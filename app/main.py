from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.services import router as services_router


app = FastAPI(
    title="Service Booking API",
    version="1.0.0",
)


app.include_router(auth_router)
app.include_router(services_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}