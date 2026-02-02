from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# IMPORT THE ROUTER
from app.api import router as topsis_router

app = FastAPI(
    title="TOPSIS API",
    version="1.0.0"
)

# CORS (important for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ THIS LINE WAS MISSING / NOT EFFECTIVE IN DEPLOYMENT
app.include_router(topsis_router)

# Simple root check
@app.get("/")
def root():
    return {"status": "Backend is running"}
