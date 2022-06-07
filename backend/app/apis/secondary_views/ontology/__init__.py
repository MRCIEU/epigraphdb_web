from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from . import funcs

router = APIRouter()


class OntologyDataRequest(BaseModel):
    ent_id: str
    ent_term: str


class OntologyDataResponseItem(BaseModel):
    ent_id: str
    ent_term: str
    ref_ent_id: str
    ent_type: str
    ent_url: str


OntologyDataResponse = List[OntologyDataResponseItem]


@router.post(
    "/ontology/efo",
    response_model=OntologyDataResponse,
)
def get_efo_data(query: OntologyDataRequest):
    ent_id = query.ent_id
    res_df = funcs.get_efo_data(ent_id=ent_id)
    res = res_df.to_dict(orient="records")
    return res
