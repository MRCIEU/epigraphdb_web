from pathlib import Path

from loguru import logger

from .env_configs import env_configs

#############
# env configs
#############

# env configs
debug = bool(env_configs["DEBUG"]["value"])
api_url = env_configs["API_URL"]["value"]
api_key = env_configs["API_KEY"]["value"]

# frontend
frontend_url = env_configs["BACKEND_FRONTEND_URL"]["value"]
dashboard_url = env_configs["BACKEND_DASHBOARD_URL"]["value"]

# mongodb
mongo_passwd = env_configs["MONGO_PASSWD"]["value"]
mongo_host = env_configs["BACKEND_MONGO_HOST"]["value"] or "localhost"
mongo_port = env_configs["BACKEND_MONGO_PORT"]["value"] or "27017"

# elasticsearch
es_host = env_configs["BACKEND_ES_HOST"]["value"] or "localhost"
es_port = env_configs["BACKEND_ES_PORT"]["value"] or "9200"

#################
# general configs
#################

# directory configs
log_dir = Path("/tmp/epigraphdb_web/logs")
log_dir.mkdir(parents=True, exist_ok=True)

# general settings
docs_url = "http://docs.epigraphdb.org"

##############
# echo configs
##############

setting_configs = {
    "debug": {"value": debug, "secret": False},
    "api_url": {"value": api_url, "secret": False},
    "api_key": {"value": api_key, "secret": True},
    "frontend_url": {"value": frontend_url, "secret": False},
    "dashboard_url": {"value": dashboard_url, "secret": False},
    "mongo_passwd": {"value": mongo_passwd, "secret": True},
    "mongo_host": {"value": mongo_host, "secret": False},
    "mongo_port": {"value": mongo_port, "secret": False},
    "es_host": {"value": es_host, "secret": False},
    "es_port": {"value": es_port, "secret": False},
}

for name, config in setting_configs.items():
    if config["value"] is None:
        logger.error(f"Config {name} is None. Review your settings!")

config_status = (
    "EpiGraphDB Web configs\n\n"
    + "\n".join(
        [
            "- {name}: {config}".format(
                name=(
                    str(name)
                    if not config["secret"]
                    else "{name}[:5]".format(name=name)
                ),
                config=(
                    config["value"]
                    if not config["secret"]
                    else "{value}".format(value=config["value"][:5])
                ),
            )
            for name, config in setting_configs.items()
        ]
    )
    + "\n"
)
logger.info(config_status)
