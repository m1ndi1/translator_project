from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])


class HealthcheckResponse(BaseModel):
    status: str


@router.get("/health", response_model=HealthcheckResponse)
async def healthcheck() -> HealthcheckResponse:
    return HealthcheckResponse(status="ok")
