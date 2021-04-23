from app.models.entities import (
    AnnotatedMetaEntity,
    AnnotatedNodeId,
    AnnotatedProperty,
)
from app.utils.meta_graph import meta_node_doc_url, meta_rel_doc_url
from epigraphdb_common_utils import epigraphdb_schema


def annotate_meta_entity(
    meta_entity_name: str, meta_entity_type: str
) -> AnnotatedMetaEntity:
    if meta_entity_type == "meta_rel":
        url = meta_rel_doc_url(meta_entity_name)
        meta_dict = epigraphdb_schema.meta_rels_dict  # type: ignore
    else:
        url = meta_node_doc_url(meta_entity_name)
        meta_dict = epigraphdb_schema.meta_nodes_dict  # type: ignore
    doc = meta_dict[meta_entity_name].doc
    res: AnnotatedMetaEntity = {
        "name": meta_entity_name,
        "doc": doc,
        "url": url,
    }
    return res


def annotate_node_id(node_id: str, meta_node: str) -> AnnotatedNodeId:
    url = entity_id_match(meta_node=meta_node, id=node_id)
    res: AnnotatedNodeId = {"id": node_id, "url": url}
    return res


def annotate_property(
    prop_name: str, meta_entity: str, meta_entity_type: str
) -> AnnotatedProperty:
    if meta_entity_type == "meta_rel":
        prop_docs = epigraphdb_schema.meta_rels_property_docs
    else:
        prop_docs = epigraphdb_schema.meta_nodes_property_docs
    doc = prop_docs[meta_entity][prop_name]
    res: AnnotatedProperty = {"prop_name": prop_name, "doc": doc}
    return res


def entity_id_match(meta_node: str, id: str) -> str:
    """Returns the a url showing info regarding this entity."""
    url_template = "/entity?meta_node={meta_node}&id={id}"
    url = url_template.format(meta_node=meta_node, id=id)
    return url


def entity_name_match(meta_node: str, name: str) -> str:
    """Returns the a url showing info regarding this entity."""
    url_template = "/search?q={name}&meta_node={meta_node}"
    url = url_template.format(meta_node=meta_node, name=name)
    return url
