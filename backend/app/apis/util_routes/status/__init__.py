from typing import Dict

from fastapi import APIRouter

from app.settings import api_url
from app.utils import ping_endpoint
from epigraphdb_common_utils import (
    api_env_configs,
    backend_env_configs,
    docker_api_env_configs,
    docker_compose_extra_env_configs,
    docker_web_env_configs,
)

router = APIRouter()


@router.get("/status/ping", summary="Ping connected services.")
async def get_status_ping():
    """Ping services and return their status.
    Return True if they are running else False.
    """
    res = {"epigraphdb_api": False}
    res["epigraphdb_api"] = ping_endpoint(f"{api_url}/ping")
    return res


@router.get("/status/env/table")
def get_env_table():
    """Get the current status of environment variables for all components"""
    res = {
        env_configs_name: {
            "name": env_configs_name,
            "desc": env_configs.__doc__,
            "table": env_configs_to_table(env_configs.env_configs),
        }
        for env_configs_name, env_configs in [
            ("api", api_env_configs),
            ("docker_api", docker_api_env_configs),
            ("backend", backend_env_configs),
            ("docker_web", docker_web_env_configs),
            ("docker_compose_extra", docker_compose_extra_env_configs),
        ]
    }
    return res


def env_configs_to_table(env_configs) -> Dict:
    table = {
        "table_titles": [
            {"key": _, "label": _, "sortable": True}
            for _ in ["name", "value_display", "default", "desc"]
        ],
        "table_data": [
            {
                "name": value["name"],
                "value_display": value["value_display"],
                "default": value["default"],
                "desc": value["desc"],
            }
            for key, value in env_configs.items()
        ],
    }
    return table
