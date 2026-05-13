from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import binders, cards, collection, health, profiles, scan

app = FastAPI(
    title="Pokemon Card Collector API",
    version="0.1.0",
    description=(
        "Scaffold API for a Pokemon card collection tracker. "
        "Uses mock in-memory data until schema and persistence decisions are finalized."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://localhost:19006",
        "http://127.0.0.1:19006",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(profiles.router)
app.include_router(cards.router)
app.include_router(binders.router)
app.include_router(collection.router)
app.include_router(scan.router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Pokemon Card Collector API scaffold is running.",
    }
