from fastapi import APIRouter

router = APIRouter()


@router.get("/ping", summary="Ping backend API")
async def get_ping() -> bool:
    return True
