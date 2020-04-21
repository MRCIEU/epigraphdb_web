from fastapi import APIRouter

from .functions import process_query
from .specs import GallerySpecName, gallery_specs

router = APIRouter()


@router.get("/gallery")
def get_gallery(spec: GallerySpecName, overwrite: bool = False):
    gallery_spec = gallery_specs[spec.value]
    graph_data = process_query(gallery_spec, overwrite=overwrite)
    res = {
        "spec": {
            "name": gallery_spec.name,
            "title": gallery_spec.title,
            "description": gallery_spec.description,
            "query": gallery_spec.query,
        },
        "graph_data": graph_data,
    }
    return res
