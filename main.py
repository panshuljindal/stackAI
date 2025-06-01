import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.v1 import libraries, documents, search

load_dotenv()
app = FastAPI(
    title="Vector DB API",
    version="1.0.0",
    description="A containerized REST API to manage libraries, documents, chunks, and vector search."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(libraries.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": "Welcome to the Vector DB API. Go to /docs for Swagger UI."
    }
