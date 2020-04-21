import pytest
from loguru import logger
from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "exposure_trait, outcome_trait, pval_threshold",
    [
        ("Body mass index", None, None),
        (None, "Body mass index", None),
        ("Coronary heart disease", "Body mass index", None),
        ("Coronary heart disease", None, 1e-5),
        ("Coronary heart disease", None, 1e-8),
    ],
)
def test_mr_simple_responses(exposure_trait, outcome_trait, pval_threshold):
    logger.info(locals())
    params = {
        "exposure_trait": exposure_trait,
        "outcome_trait": outcome_trait,
        "pval_threshold": pval_threshold,
    }
    response = client.get(url="/mr-simple", params=params)
    assert response.status_code == 200


def test_mr_simple_ac():
    url = "/mr-simple/ac/trait"
    response = client.get(url=url)
    assert response.status_code == 200
    assert len(response.json()) > 1
