"""Overwrite cache."""

from loguru import logger
from starlette.testclient import TestClient

from app.main import app


def main():
    client = TestClient(app)
    logger.info("Drop cache")
    assert client.get("/utils/cache/drop", params={"all": True})
    logger.info("Index things.")
    assert client.get("/search/es/index", params={"overwrite": True})
    logger.info("Done.")


if __name__ == "__main__":
    main()
