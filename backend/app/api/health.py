from typing import Annotated

from fastapi import APIRouter, Depends

from ..core.config import Settings, get_settings
from ..core.version import VERSION

router = APIRouter()


@router.get("/health")
def health(settings: Annotated[Settings, Depends(get_settings)]) -> dict:
    return {
        "status": "ok",
        "env": settings.app_env,
        "version": VERSION,
    }
