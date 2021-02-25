from colorama import Fore, Style

from app.utils import ping_endpoint
from app.utils.database import es_client_connected, mongo_client_connected
from epigraphdb_common_utils import backend_env_configs, docker_web_env_configs


def check_env_configs() -> None:
    print(
        Style.BRIGHT
        + Fore.GREEN
        + "\n# Check environment configs"
        + Style.RESET_ALL
    )
    print(
        Style.BRIGHT
        + Fore.GREEN
        + "\n## Check environment configs for "
        + Fore.RED
        + "backend server"
        + Style.RESET_ALL
    )
    print(
        Style.DIM + Fore.YELLOW + backend_env_configs.__doc__ + Style.RESET_ALL
    )
    print(backend_env_configs.env_configs)
    print(
        Style.BRIGHT
        + Fore.GREEN
        + "\n## Check environment configs for "
        + Fore.RED
        + "web app containers"
        + Style.RESET_ALL
    )
    print(
        Style.DIM
        + Fore.YELLOW
        + docker_web_env_configs.__doc__
        + Style.RESET_ALL
    )
    print(docker_web_env_configs.env_configs)


def format_status(status: bool) -> str:
    if status:
        status_str = Style.BRIGHT + Fore.GREEN + str(status) + Style.RESET_ALL
    else:
        status_str = Style.BRIGHT + Fore.RED + str(status) + Style.RESET_ALL
    return status_str


def check_component_connections() -> None:
    api_url = backend_env_configs.env_configs["api_url"]
    api_status = ping_endpoint(f"{api_url}/ping")
    api_status_str = format_status(api_status)
    mongo_host = backend_env_configs.env_configs["mongo_host"]
    mongo_port = backend_env_configs.env_configs["mongo_port"]
    mongo_status = mongo_client_connected()
    mongo_status_str = format_status(mongo_status)
    es_host = backend_env_configs.env_configs["es_host"]
    es_port = backend_env_configs.env_configs["es_port"]
    es_status = es_client_connected()
    es_status_str = format_status(es_status)
    print(
        Style.BRIGHT
        + Fore.GREEN
        + "\n# Check component connections"
        + Style.RESET_ALL
    )
    print(f"epigraphdb_api: {api_url}\tconnected: {api_status_str}")
    print(f"mongodb: {mongo_host}:{mongo_port}\tconnected: {mongo_status_str}")
    print(f"elasticsearch: {es_host}:{es_port}\tconnected: {es_status_str}")


if __name__ == "__main__":
    check_env_configs()
    check_component_connections()
