from typing import Any, Dict, List, Optional, Tuple

import pytest
from loguru import logger
from starlette.testclient import TestClient

from app.apis.util_routes.models import get_meta_nodes_non_code_name
from app.main import app
from app.models.meta_graph import EpigraphdbMetaNodeFull, EpigraphdbMetaRelFull
from app.utils import unittest_headers

client = TestClient(app)

meta_nodes_non_code_name = get_meta_nodes_non_code_name()

response_params: List[Tuple[str, Optional[Dict[str, Any]]]] = [
    # entity explore
    ("/meta-ent/list", None),
    ("/meta-ent/api-endpoints-list", None),
    ("/meta-ent/rpkg-funcs-list", None),
    # meta ents
    *[
        ("/meta-ent/node", {"meta_node": _.value})
        for _ in EpigraphdbMetaNodeFull
    ],
    *[
        ("/meta-ent/node/search", {"meta_node": _.value, "size": 5})
        for _ in EpigraphdbMetaNodeFull
    ],
    *[("/meta-ent/rel", {"meta_rel": _.value}) for _ in EpigraphdbMetaRelFull],
    # meta rel search, individual cases
    (
        "/meta-ent/rel/search",
        {
            "source_meta_node": "Gwas",
            "target_meta_node": "Gwas",
            "meta_rel": "MR_EVE_MR",
            "size": 5,
        },
    ),
    (
        "/meta-ent/rel/search",
        {
            "source_meta_node": "Gwas",
            "target_meta_node": "Gwas",
            "meta_rel": "PRS",
            "size": 5,
        },
    ),
]

ent_params: List[Tuple[str, str, str]] = [
    # meta_node, _id, _name
    ("Disease", "http://purl.obolibrary.org/obo/MONDO_0005812", "influenza"),
    ("Drug", "DANUSERTIB", "DANUSERTIB"),
    ("Efo", "http://www.ebi.ac.uk/efo/EFO_0000378", "coronary artery disease"),
    ("Gene", "ENSG00000086570", "FAT2"),
    ("Gwas", "ieu-a-2", "Body mass index"),
    ("Literature", "19667083", "19667083"),
    ("LiteratureTerm", "C0005893", "Body mass index"),
    (
        "LiteratureTriple",
        "C0000970:AFFECTS:C1305855",
        "Acetaminophen AFFECTS Body mass index",
    ),
    ("Pathway", "R-HSA-5619084", "ABC transporter disorders"),
    ("Protein", "O43298", "O43298"),
    ("Tissue", "Adrenal Gland", "Adrenal Gland"),
    ("Variant", "rs34712273", "rs34712273"),
]


@pytest.mark.parametrize("url, params", response_params)
def test_response(url: str, params: Optional[Dict[str, Any]]):
    logger.info(locals())
    r = client.get(url=url, params=params, headers=unittest_headers)
    r.raise_for_status()
    assert r.status_code == 200
    assert len(r.json()) > 0


@pytest.mark.parametrize("meta_node, ent_id, ent_name", ent_params)
def test_entity_node(meta_node: str, ent_id: str, ent_name: str):
    logger.info(locals())
    url = "/entity/node"
    params = {"meta_node": meta_node, "id": ent_id}
    r = client.get(url=url, params=params, headers=unittest_headers)
    r.raise_for_status()
    assert r.status_code == 200
    assert len(r.json()) > 0


@pytest.mark.parametrize("meta_node, ent_id, ent_name", ent_params)
def test_entity_meta_neighbours(meta_node: str, ent_id: str, ent_name: str):
    logger.info(locals())
    url = "/entity/meta-neighbours"
    params = {"meta_node": meta_node, "id": ent_id, "name": ent_name}
    r = client.get(url=url, params=params, headers=unittest_headers)
    r.raise_for_status()
    assert r.status_code == 200
    assert len(r.json()) > 0


@pytest.mark.parametrize("meta_node, ent_id, ent_name", ent_params)
def test_entity_neighbours(meta_node: str, ent_id: str, ent_name: str):
    logger.info(locals())
    url = "/entity/neighbours"
    params = {"meta_node": meta_node, "id": ent_id}
    r = client.get(url=url, params=params, headers=unittest_headers)
    r.raise_for_status()
    assert r.status_code == 200
    assert len(r.json()) > 0


@pytest.mark.parametrize("meta_node, ent_id, ent_name", ent_params)
def test_entity_similarity_names(meta_node: str, ent_id: str, ent_name: str):
    logger.info(locals())
    url = "/entity/similar-entities/names"
    params = {
        "meta_node": meta_node,
        "id": ent_id,
        "name": ent_name,
        "size": 5,
    }
    r = client.get(url=url, params=params, headers=unittest_headers)
    r.raise_for_status()
    assert r.status_code == 200
    r_data = r.json()
    if meta_node in meta_nodes_non_code_name:
        assert len(r_data) > 0
    else:
        assert r_data is None


@pytest.mark.parametrize("meta_node, ent_id, ent_name", ent_params)
def test_entity_similarity_neural(meta_node: str, ent_id: str, ent_name: str):
    logger.info(locals())
    url = "/entity/similar-entities/neural"
    params = {
        "meta_node": meta_node,
        "id": ent_id,
        "name": ent_name,
        "size": 5,
    }
    r = client.get(url=url, params=params, headers=unittest_headers)
    r.raise_for_status()
    r_data = r.json()
    if meta_node in meta_nodes_non_code_name:
        assert len(r_data) > 0
    else:
        assert r_data is None
