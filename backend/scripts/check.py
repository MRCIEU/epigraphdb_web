from colorama import Fore, Style

from app.utils import ping_endpoint
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


def check_api_connection() -> None:
    api_url = backend_env_configs.env_configs["api_url"]
    api_status = ping_endpoint(f"{api_url}/ping")
    if api_status:
        api_status_str = (
            Style.BRIGHT + Fore.GREEN + str(api_status) + Style.RESET_ALL
        )
    else:
        api_status_str = (
            Style.BRIGHT + Fore.RED + str(api_status) + Style.RESET_ALL
        )

    print(
        Style.BRIGHT
        + Fore.GREEN
        + "\n# Check API connection"
        + Style.RESET_ALL
    )
    print(f"epigraphdb_api: {api_url}\tconnected: {api_status_str}")


if __name__ == "__main__":
    check_env_configs()
    check_api_connection()
