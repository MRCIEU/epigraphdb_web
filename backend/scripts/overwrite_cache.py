"""Overwrite cache."""

from loguru import logger
from starlette.testclient import TestClient

from app.main import app


def main():
    client = TestClient(app)
    logger.info("Drop cache")
    assert client.get("/utils/cache/drop", params={"all": True})
    assert client.get("/utils/es/drop", params={"all": True})

    logger.info("Regen ES indices")
    # NOTE: have dropped es indices, no need to overwrite
    assert client.get("/utils/es/index", params={"overwrite": False})

    logger.info("Regen metrics")
    client.get("/about/metrics", params={"overwrite": True})
    logger.info("Regen schema")
    client.get("/about/schema", params={"overwrite": True})
    logger.info("Done.")


if __name__ == "__main__":
    main()
