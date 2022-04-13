from typing import Any, Dict, Optional

import requests
from fastapi import APIRouter
from pydantic import BaseModel

from app import settings

router = APIRouter()


class NeuralQuery(BaseModel):
    route: str
    method: str = "POST"
    payload: Optional[Dict[str, Any]] = None


# A pure redirect to epigraphdb neural
@router.post("/nlp/epigraphdb_neural")
def query_epigraphdb_neural(input_data: NeuralQuery):
    url = "{url}{route}".format(
        url=settings.neural_url, route=input_data.route
    )
    if input_data.method == "GET":
        r = requests.get(url=url, params=input_data.payload)
        r.raise_for_status()
        return r.json()
    elif input_data.method == "POST":
        r = requests.post(url=url, json=input_data.payload)
        r.raise_for_status()
        return r.json()
