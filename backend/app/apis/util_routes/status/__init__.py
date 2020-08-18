from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

from app.env_configs import env_configs
from app.models import TableDataResponse


router = APIRouter()

@router.get("/status/ping", summary="Ping services.")
async def get_ping() -> bool:
    """Ping services and return their status.
    Return True if they are running else False.
    """
    return True


@router.get("/status/env/table", response_model=TableDataResponse)
def get_env_table():
    """Get the current status of environment variables in web ui
    """
    table = {
        "table_titles": [
            {"key": _, "label": _, "sortable": True}
            for _ in ["name", "value", "secret"]
        ],
        "table_data": [
            {
                "name": (key if not value["secret"] else f"{key}[:5]"),
                "value": (
                    str(value["value"])
                    if not value["secret"]
                    else str(value["value"])[:5]
                ),
                "secret": value["secret"],
            }
            for key, value in env_configs.items()
        ],
    }
    return table
