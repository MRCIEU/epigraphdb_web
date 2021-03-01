from fastapi import APIRouter

from .functions import get_metrics
from .schema import schema_info

router = APIRouter()


@router.get("/about/schema")
def get_about_schema(overwrite: bool = False):
    """Schema data
    """
    res = schema_info(overwrite=overwrite)
    return res


@router.get("/about/metrics")
def get_about_metrics(overwrite: bool = False):
    """Metrics data
    """
    res = get_metrics(overwrite=overwrite)
    return res
