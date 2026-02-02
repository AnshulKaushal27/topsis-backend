from fastapi import FastAPI
from app.api import router as topsis_router

app = FastAPI(
    title="TOPSIS Web API",
    version="1.0.0"
)

# Include TOPSIS routes
app.include_router(topsis_router)

@app.get("/")
def root():
    return {"status": "Backend is running"}
