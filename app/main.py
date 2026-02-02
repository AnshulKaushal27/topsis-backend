from fastapi import FastAPI
from app.api import router as topsis_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="TOPSIS Web API",
    description="API for running TOPSIS and emailing results",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins (safe for demo)
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, etc.
    allow_headers=["*"],        # all headers
)

app.include_router(topsis_router)


@app.get("/")
def health_check():
    return {"status": "Backend is running"}
