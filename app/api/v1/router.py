"""API v1 router: only the document-processing surface."""

from fastapi import APIRouter

from app.api.v1.endpoints import ai, auth, documents, jobs, ocr, reviews

api_v1_router = APIRouter()

api_v1_router.include_router(auth.router)
api_v1_router.include_router(documents.router)
api_v1_router.include_router(ocr.router)
api_v1_router.include_router(ai.router)
api_v1_router.include_router(jobs.router)
api_v1_router.include_router(reviews.router)
