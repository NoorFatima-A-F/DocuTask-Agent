"""
System Health Monitoring Endpoint.
"""

from fastapi import APIRouter, status
from app.schemas.response import APIResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=APIResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="System Health Check",
    description="Returns current operational status of the platform backend."
)
async def health_check() -> APIResponse[dict]:
    """Health check endpoint confirming service status."""
    return APIResponse.success_response(
        data={"status": "healthy", "service": "AI Document Processing Platform API"},
        message="System operating normally"
    )
