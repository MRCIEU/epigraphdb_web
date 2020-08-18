from colorama import Fore, Style

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


if __name__ == "__main__":
    check_env_configs()
