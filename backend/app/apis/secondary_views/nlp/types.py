from pydantic import BaseModel


class EncodeTextInput(BaseModel):
    text: str
    # limited to scispacy for now
    model: str = "scispacy"
    asis: bool = False


class EncodeEntInput(BaseModel):
    ent_id: str
    meta_ent: str


class SearchTextInput(BaseModel):
    text: str


class SearchEntInput(BaseModel):
    ent_id: str
    meta_ent: str
