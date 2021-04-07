from fastapi import APIRouter

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
    res = get_metrics(overwrite=overwrite)
    return res
