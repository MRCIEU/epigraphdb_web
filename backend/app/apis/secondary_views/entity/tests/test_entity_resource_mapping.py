from typing import List, Set, Tuple

import pytest

from app.models.meta_graph import EpigraphdbMetaNodeFull, EpigraphdbMetaRelFull

from ..entity_resource_mapping import map_entity_resources

ent_params: List[Tuple[str, str, str, Set[str]]] = [
    (
        "Gwas",
        "ieu-a-2",
        "Body mass index",
        {
            "(Gwas)-[MR_EVE_MR]->(Gwas)",
            "(Gwas)<-[MR_EVE_MR]-(Gwas)",
            "(Gwas)-[PRS]->(Gwas)",
            "(Gwas)<-[PRS]-(Gwas)",
        },
    ),
]


@pytest.mark.parametrize(
    "meta_node, entity_id, entity_name, entity_triples", ent_params
)
def test_map_entity_resources_ent(
    meta_node,
    entity_id,
    entity_name,
    entity_triples,
):
    map_entity_resources(
        meta_node=meta_node,
        entity_triples=entity_triples,
        entity_id=entity_id,
        entity_name=entity_name,
        meta_ent_only=False,
    )


@pytest.mark.parametrize(
    "meta_node", [_.value for _ in EpigraphdbMetaNodeFull]
)
def test_map_entity_resources_meta_node(meta_node):
    map_entity_resources(
        meta_node=meta_node,
        meta_ent_only=True,
    )


@pytest.mark.parametrize("meta_rel", [_.value for _ in EpigraphdbMetaRelFull])
def test_map_entity_resources_meta_rel(meta_rel):
    map_entity_resources(
        meta_rel=meta_rel,
        meta_ent_only=True,
    )
