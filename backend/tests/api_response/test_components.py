from starlette.testclient import TestClient

from app.main import app


def test_melodi_presto_status():
    url = "/components/melodi-presto"
    payload = {
        "endpoint": "/status/",
        "method": "GET",
        "params": None,
    }
    with TestClient(app) as client:
        r = client.post(url, json=payload)
    r.raise_for_status()
    assert r.ok


def test_melodi_presto_sentence():
    url = "/components/melodi-presto"
    payload = {
        "endpoint": "/sentence/",
        "method": "POST",
        "params": {
            "pmid": "21782230",
        },
    }
    with TestClient(app) as client:
        r = client.post(url, json=payload)
    r.raise_for_status()
    assert r.ok
