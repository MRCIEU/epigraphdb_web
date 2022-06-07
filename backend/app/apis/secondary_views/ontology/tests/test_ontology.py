from loguru import logger
from starlette.testclient import TestClient

from app.main import app
from app.utils import unittest_headers

client = TestClient(app)

ROUTE = "/ontology/efo"


def test_get_efo_data():
    payload = {
        "ent_id": "http://www.ebi.ac.uk/efo/EFO_0004340",
        "ent_term": "",
    }
    r = client.post(url=ROUTE, json=payload, headers=unittest_headers)
    assert r.ok
    r_res = r.json()
    logger.info(r_res)
    assert r_res
