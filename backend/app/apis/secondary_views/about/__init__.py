from fastapi import APIRouter

from app.funcs.annotate_entity import annotate_meta_entity

from . import models
from .functions import get_metrics
from .schema import schema_info

router = APIRouter()


@router.get("/about/schema", response_model=models.AboutSchemaResponse)
def get_about_schema(overwrite: bool = False):
    """Schema data"""
    res = schema_info(overwrite=overwrite)
    return res


@router.get("/about/metrics", response_model=models.AboutSchemaMetrics)
def get_about_metrics(overwrite: bool = False):
    """Metrics data"""

    def _annotate_node(item):
        res = {
            "node_name": annotate_meta_entity(
                item["node_name"], meta_entity_type="meta_node"
            ),
            "count": item["count"],
        }
        return res

    def _annotate_rel(item):
        res = {
            "relationshipType": annotate_meta_entity(
                item["relationshipType"], meta_entity_type="meta_rel"
            ),
            "count": item["count"],
        }
        return res

    def _annotate_path(item):
        res = {
            "from_node": annotate_meta_entity(
                item["from_node"], meta_entity_type="meta_node"
            ),
            "to_node": annotate_meta_entity(
                item["to_node"], meta_entity_type="meta_node"
            ),
            "rel": annotate_meta_entity(
                item["rel"], meta_entity_type="meta_rel"
            ),
            "count": item["count"],
        }
        return res

    metrics = get_metrics(overwrite=overwrite)
    meta_node = metrics["meta_node"]
    meta_rel = metrics["meta_rel"]
    meta_path = metrics["meta_path"]
    meta_node_annotated = [_annotate_node(_) for _ in meta_node.values()]
    meta_rel_annotated = [_annotate_rel(_) for _ in meta_rel.values()]
    meta_path_annotated = [_annotate_path(_) for _ in meta_path.values()]
    res = {
        "meta_node": meta_node_annotated,
        "meta_rel": meta_rel_annotated,
        "meta_path": meta_path_annotated,
    }
    return res
