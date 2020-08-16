from typing import Dict, List, Tuple

import pytest
from loguru import logger
from starlette.testclient import TestClient

from app.apis.secondary_views.gallery.specs import GallerySpecName
from app.apis.topic_views.confounder import ConfounderType
from app.apis.topic_views.pqtl import pqtl_models
from app.apis.topic_views.xqtl import XqtlMrMethod, XqtlQtlType
from app.main import app
from app.models import EpigraphdbGraphs, TopicViewEndpoints
from app.utils import unittest_headers

client = TestClient(app)

# General functionalities
get_response_params_general = [
    # status
    ("/status/ping", None),
    # ("/status/components/table", None),
    # ("/status/components/plot", None),
    ("/status/env/table", None),
    # about
    ("/about/metadata", None),
    ("/about/schema", None),
    # metadata
    *[
        ("/metadata/meta_node/list", {"db": db})
        for db in [item.value for item in EpigraphdbGraphs]
    ],
    *[
        ("/metadata/meta_rel/list", {"db": db})
        for db in [item.value for item in EpigraphdbGraphs]
    ],
    ("/metadata/meta_path/list", None),
    # confounder diagrams
    *[
        (f"/confounder/query-diagram/plain/{confounder_type}", None)
        for confounder_type in [item.value for item in ConfounderType]
    ],
    # api
    ("/api/schema-plot", None),
    *[
        (
            "/api/cypher",
            {"query": """MATCH (n) RETURN (n) LIMIT 2""", "db": db},
        )
        for db in [item.value for item in EpigraphdbGraphs]
    ],
    *[
        (
            "/analysis/descriptive-stats",
            {"query": """MATCH (n) RETURN (n) LIMIT 2""", "db": db},
        )
        for db in [item.value for item in EpigraphdbGraphs]
    ],
]

# Gallery
get_response_params_gallery = [
    ("/gallery", {"spec": spec})
    for spec in [item.value for item in GallerySpecName]
]

# pqtl
get_response_params_pqtl = [
    *[
        ("/pqtl", {"query": query, "method": method})
        for method in [item.value for item in pqtl_models.PQTLMethod]
        for query in ["ADAM15", "Type 2 diabetes"]
    ],
    *[
        ("/pqtl/list", {"search_type": search_type})
        for search_type in [item.value for item in pqtl_models.PQTLSearchType]
    ],
    *[
        ("/pqtl/list/table", {"search_type": search_type})
        for search_type in [item.value for item in pqtl_models.PQTLSearchType]
    ],
    ("/pqtl/list/combined", None),
]

# explore
get_response_params_explore_node = [
    ("Disease", "influenza", None),
    ("Disease", None, "influenza"),
    ("Drug", "CODEINE", None),
    ("Drug", None, "CODEINE"),
    ("Efo", "http://www.orpha.net/ORDO/Orphanet_171866", None),
    ("Efo", None, "pathological myopia"),
    ("Event", "R-NUL-9005747", None),
    ("Event", None, "Phosphorylation and activation of CHEK2 by ATM"),
    ("Gene", "ENSG00000232163", None),
    ("Gene", None, "RPLP1P13"),
    ("Tissue", "Adrenal Gland", None),
    ("Tissue", None, "Adrenal Gland"),
    ("Gwas", "2", None),
    ("Gwas", None, "Body mass index"),
    ("Gwas", "1239", None),
    ("Gwas", None, "Years of schooling"),
    # NOTE: We should not search literature by name
    ("Literature", "22479202", None),
    # ("Literature", None, "22479202"),
    ("SemmedTerm", "aapp", None),
    ("SemmedTerm", None, "homocysteine"),
    ("Pathway", "R-HSA-68689", None),
    ("Pathway", None, "CDC6 association with the ORC:origin complex"),
    ("Protein", "A6NJS3", None),
    ("Protein", None, "A6NJS3"),
    ("Variant", "rs1347572", None),
    ("Variant", None, "rs1347572"),
]

# topics, autocompletion elasticsearch index
get_response_params_topics_index = [
    f"/{topics}/ac/index"
    for topics in [
        "mr",
        "obs-cor",
        "genetic-cor",
        "confounder",
        "drugs_risk_factors",
        "prs",
        "pathway",
        "xqtl",
        "literature_trait",
        "ontology_trait_disease",
    ]
]


# topics, autocompletion
get_response_params_topics_ac = [
    # trait
    *[
        (f"/{topics}/ac/trait", {"query": "body"})
        for topics in [
            "mr",
            "obs-cor",
            "genetic-cor",
            "confounder",
            "drugs_risk_factors",
            "pathway",
            "prs",
        ]
    ],
    # xqtl
    ("/xqtl/ac/exposure_gene", {"query": "PLAU"}),
    ("/xqtl/ac/outcome_trait", {"query": "Crohn"}),
    ("/xqtl/ac/variant", {"query": "rs12"}),
    # literature_trait
    ("/literature_trait/ac/trait", {"query": "body"}),
    ("/literature_trait/ac/semmed_predicate", {"query": "assoc"}),
    # ontology
    ("/ontology_trait_disease/ac/trait", {"query": "disease"}),
    ("/ontology_trait_disease/ac/disease", {"query": "disease"}),
    ("/ontology_trait_disease/ac/efo", {"query": "disease"}),
]


# topics, proper
# nested unpacking of a list comprehension :)
topics_params_nested = (
    [
        *[
            [
                # mr
                (
                    f"/mr{route}",
                    {
                        "exposure_trait": "Body mass index",
                        "outcome_trait": None,
                    },
                ),
                (
                    f"/mr{route}",
                    {
                        "exposure_trait": None,
                        "outcome_trait": "Body mass index",
                    },
                ),
                (
                    f"/mr{route}",
                    {
                        "exposure_trait": "Coronary heart disease",
                        "outcome_trait": "Body mass index",
                    },
                ),
                # obs-cor
                (f"/obs-cor{route}", {"trait": "Body mass index"}),
                # genetic-cor
                (f"/genetic-cor{route}", {"trait": "Whole body fat mass"}),
                (f"/prs{route}", {"trait": "Body mass index"}),
                # confounder
                # drugs_risk_factors
                (f"/drugs_risk_factors{route}", {"trait": "Body mass index"}),
                # pathway
                (f"/pathway{route}", {"trait": "Body mass index"}),
                # literature_trait
                (f"/literature_trait{route}", {"trait": "Body mass index"}),
                (
                    f"/literature_trait{route}",
                    {
                        "trait": "Body mass index",
                        "semmed_predicates": ["AFFECTS"],
                    },
                ),
                # ontology_trait_disease
                (f"/ontology_trait_disease{route}", {"trait": "disease"}),
                (f"/ontology_trait_disease{route}", {"efo_term": "disease"}),
                (
                    f"/ontology_trait_disease{route}",
                    {"disease_label": "disease"},
                ),
            ]
            for route in [
                "",
                *[f"/{item.value}" for item in TopicViewEndpoints],
            ]
        ]
    ]
    +
    # confounder
    [
        *[
            [  # type: ignore
                (
                    f"/confounder{route}",
                    {
                        "exposure_trait": "Body mass index",
                        "outcome_trait": "Coronary heart disease",
                        "confounder_type": confounder_type,
                    },
                ),
                (
                    f"/confounder{route}",
                    {
                        "exposure_trait": "Coronary heart disease",
                        "outcome_trait": "Body mass index",
                        "confounder_type": confounder_type,
                    },
                ),
            ]
            for route in [
                "",
                *[f"/{item.value}" for item in TopicViewEndpoints],
            ]
            for confounder_type in [item.value for item in ConfounderType]
        ]
    ]
    +
    # xqtl, multi snp mr
    [
        *[
            [  # type: ignore
                (
                    f"/xqtl{route}",
                    {
                        "xqtl_mode": "multi_snp_mr",
                        "exposure_gene": "PLAU",
                        "qtl_type": qtl_type,
                        "mr_method": mr_method,
                    },
                ),
                (
                    f"/xqtl{route}",
                    {
                        "xqtl_mode": "multi_snp_mr",
                        "outcome_trait": "Coronary heart disease",
                        "qtl_type": qtl_type,
                        "mr_method": mr_method,
                    },
                ),
                (
                    f"/xqtl{route}",
                    {
                        "xqtl_mode": "multi_snp_mr",
                        "exposure_gene": "PLAU",
                        "outcome_trait": "Coronary heart disease",
                        "qtl_type": qtl_type,
                        "mr_method": mr_method,
                    },
                ),
            ]
            for route in [
                "",
                *[f"/{item.value}" for item in TopicViewEndpoints],
            ]
            for qtl_type in [item.value for item in XqtlQtlType]
            for mr_method in [item.value for item in XqtlMrMethod]
        ]
    ]
    +
    # xqtl, single snp mr
    [
        *[
            [  # type: ignore
                (
                    f"/xqtl{route}",
                    {
                        "xqtl_mode": "single_snp_mr",
                        "exposure_gene": "PLAU",
                        "qtl_type": qtl_type,
                    },
                ),
                (
                    f"/xqtl{route}",
                    {
                        "xqtl_mode": "single_snp_mr",
                        "outcome_trait": "Coronary heart disease",
                        "qtl_type": qtl_type,
                    },
                ),
                (
                    f"/xqtl{route}",
                    {
                        "xqtl_mode": "single_snp_mr",
                        "variant": "rs10002427",
                        "qtl_type": qtl_type,
                    },
                ),
                (
                    f"/xqtl{route}",
                    {
                        "xqtl_mode": "single_snp_mr",
                        "exposure_gene": "PLAU",
                        "variant": "rs10002427",
                        "qtl_type": qtl_type,
                    },
                ),
                (
                    f"/xqtl{route}",
                    {
                        "xqtl_mode": "single_snp_mr",
                        "exposure_gene": "PLAU",
                        "outcome_trait": "Coronary heart disease",
                        "qtl_type": qtl_type,
                    },
                ),
            ]
            for route in [
                "",
                *[f"/{item.value}" for item in TopicViewEndpoints],
            ]
            for qtl_type in [item.value for item in XqtlQtlType]
        ]
    ]
)
get_response_params_topics: List[Tuple[str, object]] = [
    item for nested_item in topics_params_nested for item in nested_item
]


@pytest.mark.parametrize("url, params", get_response_params_general)
def test_get_responses(url: str, params: Dict[str, object]):
    logger.info(locals())
    response = client.get(url, params=params, headers=unittest_headers)
    assert response.status_code == 200


@pytest.mark.parametrize("url, params", get_response_params_pqtl)
def test_get_responses_pqtl(url: str, params: Dict[str, object]):
    logger.info(locals())
    response = client.get(url, params=params, headers=unittest_headers)
    assert response.status_code == 200


@pytest.mark.parametrize("url, params", get_response_params_gallery)
def test_get_responses_gallery(url: str, params: Dict[str, object]):
    logger.info(locals())
    response = client.get(url, params=params, headers=unittest_headers)
    assert response.status_code == 200
    assert response.json()["graph_data"] is not None


@pytest.mark.parametrize(
    "meta_node, id, name", get_response_params_explore_node
)
def test_get_responses_explore_node(meta_node: str, id: str, name: str):
    logger.info(locals())
    params = {"meta_node": meta_node, "id": id, "name": name}
    response = client.get(
        url="/explore/search/node", params=params, headers=unittest_headers
    )
    assert response.status_code == 200


@pytest.mark.parametrize(
    "meta_node_source, id_source, meta_node_target, id_target, max_path_length, limit",
    [
        ("Gwas", "1", "Gwas", "361", 1, 2),
        ("Variant", "rs10781543", "Gwas", "12", 1, 2),
    ],
)
def test_get_responses_explore_path(
    meta_node_source,
    id_source,
    meta_node_target,
    id_target,
    max_path_length,
    limit,
):
    logger.info(locals())
    url = "/explore/search/path"
    params = {
        "meta_node_source": meta_node_source,
        "id_source": id_source,
        "meta_node_target": meta_node_target,
        "id_target": id_target,
        "max_path_length": max_path_length,
        "limit": limit,
    }
    response = client.get(url, params=params, headers=unittest_headers)
    assert response.status_code == 200


@pytest.mark.parametrize("url", get_response_params_topics_index)
def test_get_responses_topics_index(url: str):
    logger.info(locals())
    response = client.get(url=url, headers=unittest_headers)
    assert response.status_code == 200


@pytest.mark.parametrize("url, params", get_response_params_topics_ac)
def test_get_responses_topics_ac(url: str, params: Dict[str, object]):
    logger.info(locals())
    response = client.get(url=url, params=params, headers=unittest_headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.parametrize("url, params", get_response_params_topics)
def test_get_responses_topics(url: str, params: Dict[str, object]):
    logger.info(locals())
    response = client.get(url=url, params=params, headers=unittest_headers)
    assert response.status_code == 200
