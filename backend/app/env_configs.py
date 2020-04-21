from typing import Any, Dict

from environs import Env

env_vars = [
    # common
    "DEBUG",
    "API_URL",
    "API_KEY",
    "MONGO_PASSWD",
    # graph
    "GRAPH_CONTAINER_NAME",
    "GRAPH_HTTP_PORT",
    "GRAPH_BOLT_PORT",
    "GRAPH_HTTPS_PORT",
    "GRAPH_PASSWD",
    # api
    "DOCKER_API_PORT_PRIVATE",
    "DOCKER_API_PORT_PUBLIC",
    "EPIGRAPHDB_DB_BROWSER",
    "EPIGRAPHDB_VERSION",
    "EPIGRAPHDB_SERVER",
    "EPIGRAPHDB_PORT",
    "EPIGRAPHDB_USER",
    "EPIGRAPHDB_PASSWD",
    "EPIGRAPHDB_DB_VERSION",
    "PQTL_SERVER",
    "PQTL_PORT",
    "PQTL_USER",
    "PQTL_PASSWD",
    "PQTL_DB_VERSION",
    # web
    "DOCKER_BACKEND_PORT",
    "DOCKER_FRONTEND_PORT",
    "DOCKER_DASHBOARD_PORT",
    # web, backend
    "BACKEND_FRONTEND_URL",
    "BACKEND_DASHBOARD_URL",
    "BACKEND_MONGO_HOST",
    "BACKEND_MONGO_PORT",
    "BACKEND_ES_HOST",
    "BACKEND_ES_PORT",
    # web, frontend
    "FRONTEND_BACKEND_URL",
    # utils: for utilities, mongodb, ELK
    "DOCKER_MONGO_PORT",
    "DOCKER_ADMIN_MONGO_PORT",
    "DOCKER_ES_PORT",
    "DOCKER_KIBANA_PORT",
    "DOCKER_MONGO_VOLUME",
    "DOCKER_ES_VOLUME",
]

# Loads environmental variables from .env
env = Env()
env.read_env()


def env_conf(name: str) -> Dict[str, Any]:
    """If there is "PASSWD", "PASSWORD", "KEY" in name,
    then treat it as a secret variable
    """
    value = env.str(name, None)
    secret = False
    pattern_found = [
        pattern in name for pattern in ["PASSWD", "PASSWORD", "KEY"]
    ]
    if sum(pattern_found) > 0:
        secret = True
    res = {"name": name, "value": value, "secret": secret}
    return res


env_configs = {
    item["name"]: {"value": item["value"], "secret": item["secret"]}
    for item in [env_conf(name) for name in env_vars]
}
