import requests
from fastapi import APIRouter

from app.settings import api_url, neural_url
from app.utils.database import es_client_connected, mongo_client_connected

router = APIRouter()


@router.get("/ping", response_model=bool, summary="Ping backend API")
def get_ping(dependencies: bool = True) -> bool:
    if not dependencies:
        return True
    else:
        api_ok = requests.get(f"{api_url}/ping").ok
        neural_ok = requests.get(f"{neural_url}/ping").ok
        es_ok = es_client_connected()
        mongo_ok = mongo_client_connected()
        all = [api_ok, neural_ok, es_ok, mongo_ok]
        all_ok = sum(all) == len(all)
        return all_ok
