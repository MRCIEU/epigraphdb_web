from loguru import logger
from starlette.testclient import TestClient

from app.main import app
from app.utils import unittest_headers

client = TestClient(app)


def test_encode_text():
    url = "/nlp/encode/text"
    payload = {"text": "body mass index", "asis": True}
    r = client.post(url=url, json=payload, headers=unittest_headers)
    r.raise_for_status()
    assert r.ok
    r_res = r.json()
    logger.info(r_res)
    assert len(r_res["results"]) > 0


def test_encode_ent():
    url = "/nlp/encode/ent"
    payload = {
        "ent_id": "ieu-a-2",
        "meta_ent": "Gwas",
    }
    r = client.post(url=url, json=payload, headers=unittest_headers)
    r.raise_for_status()
    assert r.ok
    r_res = r.json()
    logger.info(r_res)
    assert len(r_res["results"]) > 0
