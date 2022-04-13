from loguru import logger
from starlette.testclient import TestClient

from app.main import app
from app.utils import unittest_headers

client = TestClient(app)

NEURAL_ROUTE = "/nlp/epigraphdb_neural"


def ping_neural():
    payload = {
        "route": "/ping",
        "method": "GET",
        "payload": {"dependencies": False},
    }
    r = client.post(url=NEURAL_ROUTE, json=payload, headers=unittest_headers)
    assert r.ok
    r_res = r.json()
    logger.info(r_res)
    assert r_res


def test_available_meta_ents():
    payload = {
        "route": "/query/meta-entity-list",
        "method": "GET",
        "payload": None,
    }
    r = client.post(url=NEURAL_ROUTE, json=payload, headers=unittest_headers)
    assert r.ok
    r_res = r.json()
    logger.info(r_res)
    assert r_res


def test_encode_text():
    payload = {
        "route": "/nlp/encode/text",
        "method": "GET",
        "payload": {"text": "body mass index", "asis": True},
    }
    r = client.post(url=NEURAL_ROUTE, json=payload, headers=unittest_headers)
    assert r.ok
    r_res = r.json()
    logger.info(r_res)
    assert len(r_res["results"]) > 0


def test_encode_ent():
    payload = {
        "route": "/query/entity/encode",
        "method": "GET",
        "payload": {"entity_id": "ieu-a-2", "meta_node": "Gwas"},
    }
    r = client.post(url=NEURAL_ROUTE, json=payload, headers=unittest_headers)
    assert r.ok
    r_res = r.json()
    logger.info(r_res)
    assert len(r_res) > 0


def test_search_by_text():
    payload = {
        "route": "/query/text",
        "method": "GET",
        "payload": {"text": "body mass index", "asis": True},
    }
    r = client.post(url=NEURAL_ROUTE, json=payload, headers=unittest_headers)
    assert r.ok
    r_res = r.json()
    logger.info(r_res)
    assert len(r_res) > 0


def test_search_by_ent():
    payload = {
        "route": "/query/entity",
        "method": "GET",
        "payload": {"entity_id": "ieu-a-2", "meta_node": "Gwas"},
    }
    r = client.post(url=NEURAL_ROUTE, json=payload, headers=unittest_headers)
    assert r.ok
    r_res = r.json()
    logger.info(r_res)
    assert len(r_res) > 0
