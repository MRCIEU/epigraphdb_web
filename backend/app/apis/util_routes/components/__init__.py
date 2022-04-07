from typing import Any, Dict, Optional

import requests
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

MELODI_PRESTRO_URL = "https://melodi-presto.mrcieu.ac.uk/api"


class MelodiPrestoRequest(BaseModel):
    endpoint: str
    params: Optional[Dict[str, Any]]
    method: str = "POST"


@router.post("/components/melodi-presto")
def query_melodi_presto(data: MelodiPrestoRequest):
    print("data: ", data)
    url = f"{MELODI_PRESTRO_URL}{data.endpoint}"
    print("url: ", url)
    if data.method == "GET":
        r = requests.get(url, params=data.params)
    elif data.method == "POST":
        r = requests.post(url, json=data.params)
    r.raise_for_status()
    return r.json()
