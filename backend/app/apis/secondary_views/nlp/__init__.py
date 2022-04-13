from fastapi import APIRouter

from . import processing, types

router = APIRouter()


@router.post("/nlp/encode/text")
def encode_text(input_data: types.EncodeTextInput):
    encode_results = processing.encode_text(
        text=input_data.text,
        asis=input_data.asis,
    )
    res = {
        "results": encode_results["results"],
        "metadata": {
            "model": input_data.model,
            "length": len(encode_results["results"]),
            "clean_text": encode_results["clean_text"],
        },
    }
    return res


@router.post("/nlp/encode/ent")
def encode_ent(input_data: types.EncodeEntInput):
    encode_results = processing.encode_ent(
        ent_id=input_data.ent_id,
        meta_ent=input_data.meta_ent,
    )
    res = {
        "results": encode_results,
        "metadata": {
            "length": len(encode_results),
        },
    }
    return res


# @router.post("/nlp/search/text")
# def encode_ent(input_data: types.SearchTextInput):
#     # search most similar ents
#     pass


# @router.post("/nlp/search/ent")
# def encode_ent(input_data: types.SearchEntInput):
#     # search most similar ents
#     pass
