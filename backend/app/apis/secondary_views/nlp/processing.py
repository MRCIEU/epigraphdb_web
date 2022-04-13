import requests

from app import settings


def encode_text(text: str, asis: bool = False):
    url = "{url}/nlp/encode/text".format(url=settings.neural_url)
    # TODO: model
    payload = {
        "text": text,
        "asis": asis,
    }
    r = requests.get(url, params=payload)
    r.raise_for_status()
    res = r.json()
    return res


def encode_ent(ent_id: str, meta_ent: str):
    url = "{url}/query/entity/encode".format(url=settings.neural_url)
    # TODO: model
    payload = {
        "entity_id": ent_id,
        "meta_node": meta_ent,
    }
    r = requests.get(url, params=payload)
    r.raise_for_status()
    res = r.json()
    return res
