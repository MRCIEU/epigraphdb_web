import io
from typing import Any, Dict, Optional

import requests
from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from app.models import EpigraphdbGraphsExtended, RequestMethods
from app.settings import api_url
from app.utils import api_request_headers
from app.utils.logging import log_args

router = APIRouter()


class ApiRequest(BaseModel):
    params: Dict[str, Any]
    endpoint: str
    method: RequestMethods = RequestMethods.get


@router.post("/api")
def post_api(data: ApiRequest):
    log_args(api="/api", kwargs=locals())
    url = f"{api_url}{data.endpoint}"
    if data.method == "GET":
        r = requests.get(url, params=data.params, headers=api_request_headers)
    elif data.method == "POST":
        r = requests.post(url, json=data.params, headers=api_request_headers)
    r.raise_for_status()
    return r.json()


@router.get("/api/schema-plot")
def get_schema_plot():
    log_args(api="/api", kwargs=locals())
    url = f"{api_url}/meta/schema"
    r = requests.get(
        url,
        params={"graphviz": True, "plot": True},
        headers=api_request_headers,
    )
    r.raise_for_status()
    return StreamingResponse(io.BytesIO(r.content), media_type="image/png")


@router.get("/api/cypher")
def get_api_cypher(
    query: str,
    db: EpigraphdbGraphsExtended = EpigraphdbGraphsExtended.epigraphdb,
    hostname: Optional[str] = None,
    bolt_port: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
):
    """A shorthand for the api /raw_cypher endpoint."""
    log_args(api="/api/cypher", kwargs=locals())
    url = f"{api_url}/raw_cypher/"
    params = {
        "query": query,
        "db": db.value,
        "hostname": hostname,
        "bolt_port": bolt_port,
        "user": user,
        "password": password,
    }
    r = requests.get(url, params=params, headers=api_request_headers)
    r.raise_for_status()
    res = r.json()
    return res
