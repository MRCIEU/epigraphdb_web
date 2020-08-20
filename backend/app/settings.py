from pathlib import Path

from epigraphdb_common_utils.backend_env_configs import env_configs

#############
# env configs
#############

# env configs
api_url = env_configs["api_url"]
api_key = env_configs["api_key"]

# mongodb
mongo_passwd = env_configs["mongo_passwd"]
mongo_host = env_configs["mongo_host"]
mongo_port = env_configs["mongo_port"]

# elasticsearch
es_host = env_configs["es_host"]
es_port = env_configs["es_port"]

#################
# general configs
#################

# directory configs
log_dir = Path("/tmp/epigraphdb_web/logs")
log_dir.mkdir(parents=True, exist_ok=True)

# general settings
docs_url = "https://docs.epigraphdb.org"
