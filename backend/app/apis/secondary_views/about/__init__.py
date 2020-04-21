from fastapi import APIRouter

from .functions import get_metadata
from .schema import get_schema

router = APIRouter()


@router.get("/about/metadata")
def get_about_metadata(overwrite: bool = False):
    res = get_metadata(overwrite=overwrite)
    return res


@router.get("/about/schema")
def get_about_schema(overwrite: bool = False):
    res = get_schema(overwrite=overwrite)
    return res
